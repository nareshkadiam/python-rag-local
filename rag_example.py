from chunking import chunk_text
from rag_service import answer_with_retrieval
from semantic_retrieval import build_index
from chunking import chunk_by_paragraph

def main() -> None:
    """
    document = (
        "Employees must submit leave requests two weeks in advance. "
        "Managers review leave requests based on team staffing needs. "
        "Employees claim travel expenses through the company finance portal. "
        "Contact the support team to reset your account password."
    )

    chunks = chunk_text(
        document,
        chunk_size=10,
        overlap=0,
    )
    """
    document = (
        "Employees must submit leave requests two weeks in advance.\n\n"
        "Managers review leave requests based on team staffing needs.\n\n"
        "Employees claim travel expenses through the company finance portal.\n\n"
        "Contact the support team to reset your account password."
    )

    chunks = chunk_by_paragraph(document)
    index = build_index(chunks)

    index = build_index(chunks)

    while True:
        question = input("\nAsk a question, or enter 'exit': ").strip()

        if question.lower() == "exit":
            break

        if not question:
            print("Please enter a question.")
            continue

        result = answer_with_retrieval(
            question=question,
            index=index,
            top_k=2,
        )

        print(f"\nAnswer: {result['answer']}")
        print("\nPassages supplied to the model:")

        for chunk in result["retrieved_chunks"]:
            print(
                f"\nChunk {chunk['chunk_id']} "
                f"— similarity {chunk['score']:.4f}"
            )
            print(chunk["text"])


if __name__ == "__main__":
    main()