from math import sqrt
from openai import OpenAI

EMBEDDING_MODEL = "text-embedding-3-small"

def create_embeddings(texts: list[str]) -> list[list[float]]:

    if not texts:
        return []

    for text in texts:
        if not text.strip():
            raise ValueError("Emedding input cannot be empty.")
        
    with OpenAI(timeout=30, max_retries=0) as client:
        response = client.embeddings.create(
            model = EMBEDDING_MODEL,
            input = texts,
            encoding_format = "float"
        )

        #print(f"response:: {response.data}")

        ordered_items = sorted(
            response.data,
            key=lambda item: item.index
        )

        embeddings = []
        for item in ordered_items:
            embeddings.append(item.embedding)

        return embeddings

def cosine_similarity(a: list[float], b: list[float]) -> float:
    if not a or len(a) != len(b):
        raise ValueError("Vectors must be non-empty and of the same length.")

    dot_product = 0.0
    squared_length_a = 0.0
    squared_length_b = 0.0

    for value_a, value_b in zip(a, b):
        dot_product += value_a * value_b
        squared_length_a += value_a ** 2
        squared_length_b += value_b ** 2

    length_a = sqrt(squared_length_a)
    length_b = sqrt(squared_length_b)

    if length_a == 0.0 or length_b == 0.0:
        raise ValueError("Vectors cannot be zero length.")

    return dot_product / (length_a * length_b)
