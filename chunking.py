def chunk_text(text: str, chunk_size: int = 100, overlap: int = 20) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("Chunk size must be a positive integer.")
    if overlap < 0:
        raise ValueError("Overlap must be a non-negative integer.")
    if overlap >= chunk_size:
        raise ValueError("Overlap must be less than chunk size.")

    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size

        chunk_words = words[start:end]
        chunk = " ".join(chunk_words)
        chunks.append(chunk)

        if end >= len(words):
            break

        start = end - overlap
    return chunks

def chunk_by_paragraph(text: str) -> list[str]:
    normalised_text = text.replace("\r\n", "\n")
    paragraphs = normalised_text.split("\n\n")
    chunks = []

    for paragraph in paragraphs:
        cleaned_paragraph = paragraph.strip()

        if cleaned_paragraph:
            chunks.append(cleaned_paragraph)

    return chunks