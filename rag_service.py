import logging
from time import perf_counter
from uuid import uuid4

from ai_service import answer_question
from citation_validation import validate_citations
from semantic_retrieval import retrieve_semantic_chunks


logger = logging.getLogger(__name__)


def answer_with_retrieval(
    question: str,
    index: list[dict],
    top_k: int = 2,
) -> dict:
    request_id = str(uuid4())
    started = perf_counter()
    stage = "retrieval"

    logger.info("request_id=%s event=started", request_id)

    try:
        retrieval_started = perf_counter()

        retrieved_chunks = retrieve_semantic_chunks(
            question=question,
            index=index,
            top_k=top_k,
        )

        retrieval_seconds = perf_counter() - retrieval_started

        chunk_ids = []

        for chunk in retrieved_chunks:
            chunk_ids.append(chunk["chunk_id"])

        logger.info(
            "request_id=%s event=retrieved chunk_ids=%s duration=%.3f",
            request_id,
            chunk_ids,
            retrieval_seconds,
        )

        generation_seconds = 0.0

        if not retrieved_chunks:
            answer = "No document passages are available to answer this question."

        else:
            context_parts = []

            for chunk in retrieved_chunks:
                context_parts.append(
                    f"[Chunk {chunk['chunk_id']}]\n{chunk['text']}"
                )

            context = "\n\n".join(context_parts)
            stage = "generation"
            generation_started = perf_counter()

            answer = answer_question(
                document_text=context,
                question=question,
                cite_sources=True,
            )

            generation_seconds = perf_counter() - generation_started

        stage = "citation_validation"

        citation_check = validate_citations(
            answers=answer,
            retrieved_chunks=retrieved_chunks,
        )

        if citation_check["unknown_chunk_ids"]:
            logger.warning(
                "request_id=%s event=unknown_citations chunk_ids=%s",
                request_id,
                citation_check["unknown_chunk_ids"],
            )

        total_seconds = perf_counter() - started

        logger.info(
            "request_id=%s event=completed generation=%.3f total=%.3f",
            request_id,
            generation_seconds,
            total_seconds,
        )

        return {
            "request_id": request_id,
            "answer": answer,
            "retrieved_chunks": retrieved_chunks,
            "citation_check": citation_check,
            "timings": {
                "retrieval_seconds": round(retrieval_seconds, 3),
                "generation_seconds": round(generation_seconds, 3),
                "total_seconds": round(total_seconds, 3),
            },
        }

    except Exception as error:
        logger.error(
            "request_id=%s event=failed stage=%s error_type=%s",
            request_id,
            stage,
            type(error).__name__,
        )
        raise