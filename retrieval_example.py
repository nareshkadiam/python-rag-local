from chunking import chunk_text
from retrieval import retrieve_chunks

def test() -> None:
    sample_document = (
        "Employees must submit leave requests at least two weeks in advance. "
        "Managers approve requests based on staffing needs and department coverage. "
        "Employees receive twenty days of annual leave per calendar year. "
        "Unused annual leave can be rolled over up to a maximum of five days. "
        "Sick leave requires a medical certificate if extending beyond three consecutive days."
    )

    chunks = chunk_text(sample_document, chunk_size=12, overlap=3)
    question = "How many days of annual leave do employees get?"

    print(f"Question: {question}\n")
    print("Generated Chunks:")
    for idx, chunk in enumerate(chunks, start=1):
        print(f"  [{idx}] {chunk}")

    results = retrieve_chunks(question, chunks, top_k=2)

    print(f"\nTop {len(results)} Retrieved Chunks:")
    for result in results:
        print(f"- Chunk ID: {result['chunk_id']}")
        print(f"  Score: {result['score']}")
        print(f"  Matched Words: {result['matched_words']}")
        print(f"  Text: {result['text']}")

if __name__ == "__main__":
    test()