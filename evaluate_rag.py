from pathlib import Path

from chunking import chunk_by_paragraph
from document_io import save_analysis_to_json as save_analysis
from rag_service import answer_with_retrieval
from semantic_retrieval import build_index


DOCUMENT = (
    "Employees must submit leave requests two weeks in advance.\n\n"
    "Managers review leave requests based on team staffing needs.\n\n"
    "Employees claim travel expenses through the company finance portal.\n\n"
    "Contact the support team to reset your account password."
)

CASES = [
    {
        "name": "Password recovery",
        "question": "How do I recover my login credentials?",
        "expected_chunk_id": 4,
        "expected_answer": "Contact the support team to reset the password.",
    },
    {
        "name": "Travel reimbursement",
        "question": "How can I get reimbursed for business travel?",
        "expected_chunk_id": 3,
        "expected_answer": "Claim travel expenses through the finance portal.",
    },
    {
        "name": "Missing information",
        "question": "What food does the cafeteria serve?",
        "expected_chunk_id": None,
        "expected_answer": "States that the supplied information is insufficient.",
    },
]

def collect_review() -> dict:
    allowed_ratings = {"pass", "fail", "na"}

    while True:
        rating = input(
            "Citation support — pass, fail, or na: "
        ).strip().lower()

        if rating in allowed_ratings:
            break

        print("Please enter pass, fail, or na.")

    notes = input("Review notes: ").strip()

    return {
        "citation_support": rating,
        "notes": notes,
    }

def main() -> None:
    chunks = chunk_by_paragraph(DOCUMENT)
    index = build_index(chunks)
    results = []

    for case in CASES:
        response = answer_with_retrieval(
            question=case["question"],
            index=index,
            top_k=2,
        )

        retrieved_ids = []

        for chunk in response["retrieved_chunks"]:
            retrieved_ids.append(chunk["chunk_id"])

        expected_id = case["expected_chunk_id"]

        if expected_id is None:
            retrieval_pass = None
        else:
            retrieval_pass = expected_id in retrieved_ids

        print(f"\nCase: {case['name']}")
        print(f"Question: {case['question']}")
        print(f"Expected: {case['expected_answer']}")
        print(f"Actual: {response['answer']}")
        print(f"Retrieval pass: {retrieval_pass}")
        print(f"Citation checks: {response['citation_check']}")

        print("\nRetrieved passages:")

        for chunk in response["retrieved_chunks"]:
            print(f"[Chunk {chunk['chunk_id']}] {chunk['text']}")

        review = collect_review()

        result = {
            "name": case["name"],
            "question": case["question"],
            "expected_answer": case["expected_answer"],
            "actual_answer": response["answer"],
            "retrieved_chunk_ids": retrieved_ids,
            "retrieval_pass": retrieval_pass,
            "retrieved_chunks": response["retrieved_chunks"],
            "citation_check": response["citation_check"],
            "manual_review": review,
        }

        results.append(result)

    output_path = Path(__file__).parent / "documents" / "rag_evaluation_results.json"

    save_analysis({"results": results}, output_path)
    print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()