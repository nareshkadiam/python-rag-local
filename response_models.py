from pydantic import BaseModel, Field


class RetrievedChunk(BaseModel):
    chunk_id: int = Field(ge=1)
    text: str
    score: float


class CitationCheck(BaseModel):
    cited_chunk_ids: list[int]
    unknown_chunk_ids: list[int]
    has_citations: bool
    all_cited_ids_available: bool


class RequestTimings(BaseModel):
    retrieval_seconds: float = Field(ge=0)
    generation_seconds: float = Field(ge=0)
    total_seconds: float = Field(ge=0)


class RagAnswerResponse(BaseModel):
    request_id: str
    answer: str = Field(min_length=1)
    retrieved_chunks: list[RetrievedChunk]
    citation_check: CitationCheck
    timings: RequestTimings