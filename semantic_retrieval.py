from embedding_service import create_embeddings, cosine_similarity

def build_index(chunks: list[str]) -> list[dict]:
    embeddings = create_embeddings(chunks)
    index = []

    for chunk_id, (chunk, embedding) in enumerate(
        zip(chunks, embeddings, strict=True), start=1
        ):
        index.append({
            "chunk_id": chunk_id,
            "text": chunk,
            "embedding": embedding
        })

    return index

def retrieve_semantic_chunks(question: str, index: list[dict], top_k: int = 2) -> list[dict]:

    if not question.strip():
        raise ValueError("Question must not be blank")

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero")

    if not index:
        return []
    question_embedding = create_embeddings([question])[0]
    results = []

    for item in index:
        score = cosine_similarity(question_embedding, item["embedding"])

        results.append({
            "chunk_id": item["chunk_id"],
            "text": item["text"],
            "score": score
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]