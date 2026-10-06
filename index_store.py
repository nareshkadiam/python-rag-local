"""Persistent index storage and cache management.

This module manages the caching of semantic search indices on disk.
It avoids redundant OpenAI embedding calls by checking whether an index
already exists and remains valid according to three criteria:
1. Document content (verified via SHA-256 hash).
2. The embedding model name (e.g., text-embedding-3-small).
3. The index structure version (in case the schema or chunk format changes).
"""

import hashlib
import json
from pathlib import Path

from chunking import chunk_by_paragraph
from embedding_service import EMBEDDING_MODEL
from semantic_retrieval import build_index

# Schema version for cache invalidation when indexing logic or fields change.
INDEX_VERSION = 1


def load_or_build_index(
    document_text: str,
    cache_path: Path,
) -> list[dict]:
    """Load an existing index from disk or build and persist a new one.

    Checks the target `cache_path` for a previously cached index. If the file
    exists and its metadata matches the current document contents, embedding
    model, and index version, the cached index is loaded directly from disk.

    Otherwise, the document is chunked, embeddings are generated via the
    embedding API, and the new index is serialized to JSON on disk.

    Args:
        document_text: The complete raw document string to index.
        cache_path: The file path where the JSON index should be stored or read from.

    Returns:
        A list of chunk dictionaries, each containing 'chunk_id', 'text',
        and 'embedding'.

    Raises:
        ValueError: If `document_text` contains no valid paragraphs.
    """
    # Compute a unique fingerprint of the source text using SHA-256.
    # If even a single character in the document changes, the hash changes.
    document_hash = hashlib.sha256(
        document_text.encode("utf-8")
    ).hexdigest()

    # Metadata snapshot required to consider a cached file valid.
    expected_metadata = {
        "document_hash": document_hash,
        "embedding_model": EMBEDDING_MODEL,
        "index_version": INDEX_VERSION,
    }

    # 1. Attempt to load from disk if cache file exists
    if cache_path.is_file():
        try:
            with cache_path.open("r", encoding="utf-8") as file:
                cached = json.load(file)

        except (json.JSONDecodeError, UnicodeDecodeError):
            # Trigger rebuild if file is corrupt or unreadable
            print("Index cache could not be decoded; rebuilding.")

        else:
            # Validate metadata match and ensure index list is not empty
            print(f"Current metadata: {expected_metadata}", flush=True)

            if (
                isinstance(cached, dict)
                and cached.get("metadata") == expected_metadata
                and isinstance(cached.get("index"), list)
                and cached["index"]
            ):
                print("Loaded document index from disk")
                return cached["index"]

    # 2. Cache miss or invalid: Generate index from scratch
    chunks = chunk_by_paragraph(document_text)

    if not chunks:
        raise ValueError("The document must contain at least one paragraph")

    # Call the embedding service to generate vector representations
    index = build_index(chunks)

    # 3. Persist the generated index and its metadata to disk
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    with cache_path.open("w", encoding="utf-8") as file:
        json.dump(
            {
                "metadata": expected_metadata,
                "index": index,
            },
            file,
            indent=2,
        )

    print("Built and saved document index")
    return index