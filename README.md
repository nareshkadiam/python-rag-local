# Document Assistant v0.1

A Python API that answers questions using relevant passages from a local
handbook. Answers include chunk references for inspection.

## Stack

- Python 3.14
- FastAPI and Pydantic
- OpenAI SDK
- Local JSON index cache
- unittest with mocked model calls

## How it works

At startup:
1. Read documents/rag_handbook.txt.
2. Compare the document hash and embedding configuration with the saved cache.
3. Load a matching index, or split the document into paragraphs and embed them.
4. Keep the index in memory for incoming requests.

For each question:
1. Validate the request.
2. Generate a question embedding.
3. Rank chunks using cosine similarity.
4. Send the top two passages and question to the generation model.
5. Check that cited chunk IDs were among the supplied passages.
6. Return the answer, retrieved chunks, citation checks, request ID, and timings.

## Setup — Windows PowerShell

Create an environment:

```powershell
py -3.14 -m venv .venv
```

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Set your API key in the terminal session:

```powershell
$env:OPENAI_API_KEY = "your-api-key"
```

Do not commit the real key.

Start the API:

```powershell
.\.venv\Scripts\python.exe -m uvicorn api:app
```

Open http://127.0.0.1:8000/docs.

## Example request

POST /ask

```json
{
  "question": "How do I reset my password?"
}
```

The response includes:

- answer
- retrieved_chunks
- citation_check
- request_id
- timings

## Updating the handbook

Edit documents/rag_handbook.txt and save it.

Use blank lines between paragraphs. Restart the server to load changes.
A changed document hash triggers rebuilding and saving the index.

Changes made while the server is running do not automatically update
the in-memory index.

## Automated API tests

```powershell
.\.venv\Scripts\python.exe -m unittest test_api -v
```

These tests mock the RAG function and make no paid API calls.
They check valid requests, invalid requests, and malformed responses.
They do not test application startup or model quality.

## RAG evaluation

```powershell
.\.venv\Scripts\python.exe evaluate_rag.py
```

This makes real API calls and asks for manual citation-support ratings.
It saves results to rag_evaluation_results.json.

The evaluation uses its own fixed document, independently of the handbook
loaded by the API.

## Main modules

| Module | Responsibility |
|---|---|
| api.py | Routes, startup, request validation, HTTP error mapping |
| chunking.py | Split document text |
| embedding_service.py | Create embeddings and calculate similarity |
| semantic_retrieval.py | Build and search an in-memory index |
| index_store.py | Load or rebuild the persisted index |
| ai_service.py | Generate answers from supplied context |
| rag_service.py | Coordinate retrieval, generation, checks, and logging |
| citation_validation.py | Check cited IDs against retrieved IDs |
| response_models.py | Define the successful API response |
| logging_config.py | Configure application logging |

## Current limitations

- Designed for local use with a small, trusted text document.
- Paragraph chunks have no maximum token-size enforcement.
- Retrieval scans all chunk vectors in memory.
- Top-two retrieval can include irrelevant passages.
- Citation checks validate IDs, not whether claims are supported.
- Model answers can still be incorrect or incomplete.
- The index cache is intended for a single-process learning setup.
- No authentication, per-user access controls, or request rate limiting.
- Request IDs cover RAG operations, not complete distributed traces.

## API usage

Building a new index makes document-embedding requests.
A matching cache avoids those requests at startup.

Each normal question makes a question-embedding request and an
answer-generation request. API usage is billed separately.