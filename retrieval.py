"""Lexical retrieval module for document chunks.

This module implements a basic keyword/lexical search mechanism based on
set overlap of word tokens between a query and document chunks, excluding
frequently used English stop words.
"""

import re

# Common functional and question words filtered out to emphasize substantive terms.
STOP_WORDS = {
    "a", "an", "the", "is", "are", "do", "does",
    "i", "we", "you", "my", "to", "of", "in",
    "and", "or", "for", "how", "what", "when", "who",
}

def tokenize(text: str) -> set[str]:
    """Extract unique, lowercase word tokens and exclude stop words.

    Args:
        text: The raw string to tokenize.

    Returns:
        A set of unique normalized words excluding predefined stop words.
    """
    words = re.findall(r"\b\w+\b", text.lower())
    return set(words) - STOP_WORDS

def retrieve_chunks(question: str, chunks: list[str], top_k: int = 2) -> list[dict]:
    """Find the top-k most relevant chunks matching the question.

    Relevance is scored by the count of overlapping unique keyword tokens
    between the question and each chunk.

    Args:
        question: The user query string.
        chunks: A list of text segments to search across.
        top_k: Maximum number of relevant chunks to return (must be > 0).

    Returns:
        A list of dictionaries representing the matching chunks, sorted
        by score in descending order.

    Raises:
        ValueError: If top_k is not a positive integer.
    """
    if top_k <= 0:
        raise ValueError("top_k must be a positive integer.")

    question_words = tokenize(question)
    results = []

    for chunk_id, chunk in enumerate(chunks, start=1):
        chunk_words = tokenize(chunk)
        # Find common tokens between the query and the current chunk
        matched_words = question_words & chunk_words
        score = len(matched_words)

        # Only include chunks with at least one matching keyword
        if score > 0:
            results.append({
                "chunk_id": chunk_id,
                "text": chunk,
                "score": score,
                "matched_words": sorted(matched_words),
            })

    # Sort primarily by match count descending
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]