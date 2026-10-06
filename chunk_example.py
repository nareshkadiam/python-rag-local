from chunking import chunk_text

def test() -> None:
    text = "This is for testing the chunking we created just now, doesn't have anything specific. Try asking for one two three four five six seven eight nine ten"
    chunks = chunk_text(text, chunk_size=5, overlap=2)
    for number, chunk in enumerate(chunks, start=1):
        print(f"Chunk {number}: {chunk}")

if __name__ == "__main__":
    test()