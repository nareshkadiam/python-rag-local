from pydantic import BaseModel, Field, field_validator
from analyser import analyse_document
from ai_service import answer_question
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request

from chunking import chunk_by_paragraph
from document_io import read_document
from rag_service import answer_with_retrieval
from semantic_retrieval import build_index
from index_store import load_or_build_index

from logging_config import configure_logging
from response_models import RagAnswerResponse

from openai import APIConnectionError, APIError, APITimeoutError, AuthenticationError, RateLimitError

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    project_directory = Path(__file__).parent

    document_path = (
        project_directory / "documents" / "rag_handbook.txt"
    )
    cache_path = project_directory / "data" / "document_index.json"

    document_text = read_document(document_path)

    print(f"Reading document: {document_path.resolve()}", flush=True)
    print(f"Document content: {document_text!r}", flush=True)
    print(f"Cache location: {cache_path.resolve()}", flush=True)

    app.state.document_index = load_or_build_index(
    document_text=document_text,
    cache_path=cache_path,
)

    print(f"Reading file: {document_path.resolve()}", flush=True)
    print(f"Loaded chunks: {len(app.state.document_index)}", flush=True)

    for chunk in app.state.document_index:
        print(
            f"Chunk {chunk['chunk_id']}: {chunk['text']}",
            flush=True,
        )

    try:
        yield
    finally:
        app.state.document_index = []

app = FastAPI(
    title="Document Assistant API",
    lifespan=lifespan,
)

class AnalyseRequest(BaseModel):
    text: str = Field
    keywords: list[str] = Field(min_length=1)

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Text cannot be empty.")
        return value

    @field_validator("keywords")
    @classmethod
    def validate_keywords(cls, value: list[str]) -> list[str]:
        cleaned_keywords = []
        for keyword in value:
            cleaned_keyword = keyword.strip()
            if not cleaned_keyword:
                raise ValueError("Keywords cannot be empty.")
            
            cleaned_keywords.append(cleaned_keyword)
        return cleaned_keywords

class AskRequest(BaseModel):
    document_text: str = Field(min_length=1, max_length=10000)
    question: str = Field(min_length=1, max_length=1000)

    @field_validator("document_text", "question")
    @classmethod
    def validate_document_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Document text cannot be empty.")
        return value
    
class RagAskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        cleaned_question = value.strip()

        if not cleaned_question:
            raise ValueError("Question must not be blank")

        return cleaned_question

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.post("/analyse")
def analyse(request: AnalyseRequest) -> dict:
    return analyse_document(request.text, request.keywords)
"""
@app.post("/ask")
def ask(request: AskRequest) -> dict:
    try:
        
        answer = answer_question(
            document_text=request.document_text, 
            question=request.question
        ) 
        return {"answer": answer}
"""
@app.post("/ask", response_model=RagAnswerResponse)
def ask(body: RagAskRequest, request: Request) -> dict:
    try:
        return answer_with_retrieval(
            question=body.question,
            index=request.app.state.document_index,
            top_k=2,
        )
        """
        raise APITimeoutError(
            request=httpx.Request("POST", "https://api.openai.com/v1/responses",)
        )
        """
    except APITimeoutError as error:
        raise HTTPException(status_code=504, detail="Request timed out. Please try again.") from error
    except AuthenticationError as error:
        raise HTTPException(status_code=401, detail="Authentication failed. Please check your API credentials.") from error
    except RateLimitError as error:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.") from error
    except APIConnectionError as error:
        raise HTTPException(status_code=503, detail="Service unavailable. Please try again later.") from error
    except APIError as error:
        raise HTTPException(status_code=502, detail="Internal server error.") from error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

