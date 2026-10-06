import re

def validate_citations( answers: str, retrieved_chunks: list[dict]) -> dict:

    matches = re.findall(r"\[Chunk \d+\]", answers)
    cited_ids = set()

    for match in matches:
        chunk_id = int(re.search(r'\d+', match).group())
        cited_ids.add(chunk_id)

    available_ids = set()

    for chunk in retrieved_chunks:
        available_ids.add(chunk['chunk_id'])

    unknown_ids = cited_ids - available_ids

    return {
        "cited_chunk_ids": sorted(cited_ids),
        "unknown_chunk_ids": sorted(unknown_ids),
        "has_citations": bool(cited_ids),
        "all_cited_ids_available": not unknown_ids,
    }