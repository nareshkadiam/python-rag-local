from chunking import chunk_text
from semantic_retrieval import build_index, retrieve_semantic_chunks


def main() -> None:
    document = (
        "Employees must submit leave requests two weeks in advance. "
        "Managers review leave requests based on team staffing needs. "
        "Employees claim travel expenses through the company finance portal. "
        "Contact the support team to reset your account password."
    )

    chunks = chunk_text(document, chunk_size=10, overlap=0)
    index = build_index(chunks)

    while True:
        question = input("\nAsk a question, or enter 'exit': ").strip()

        if question.lower() == "exit":
            break

        if not question:
            print("Please enter a question.")
            continue

        results = retrieve_semantic_chunks(
            question=question,
            index=index,
            top_k=2,
        )

        for result in results:
            print(
                f"\nChunk {result['chunk_id']} "
                f"— similarity {result['score']:.4f}"
            )
            print(result["text"])


if __name__ == "__main__":
    main()