from embedding_service import create_embeddings, cosine_similarity


def main() -> None:
    question = "How do I recover my login credentials?"

    passages = [
        "Contact the support team to reset your account password.",
        "Employees must submit leave requests two weeks in advance.",
        "Employees claim travel expenses through the finance portal.",
    ]

    texts = [question] + passages
    embeddings = create_embeddings(texts)

    question_embedding = embeddings[0]
    passage_embeddings = embeddings[1:]

    print(f"Embedding dimensions: {len(question_embedding)}")

    for passage, embedding in zip(passages, passage_embeddings):
        score = cosine_similarity(question_embedding, embedding)

        print(f"\nSimilarity: {score:.4f}")
        print(f"Passage: {passage}")


if __name__ == "__main__":
    main()