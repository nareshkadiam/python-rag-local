from citation_validation import validate_citations


chunks = [
    {
        "chunk_id": 4,
        "text": "Contact support to reset your password.",
    }
]

answers = [
    "Contact support. [Chunk 4]",
    "Contact support. [Chunk 99]",
    "The supplied passages do not provide this information.",
]

for answer in answers:
    print(f"\nAnswer: {answer}")
    print(validate_citations(answer, chunks))