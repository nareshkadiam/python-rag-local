import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from api import app


def sample_response() -> dict:
    return {
        "request_id": "test-request-001",
        "answer": "Contact the support team. [Chunk 4]",
        "retrieved_chunks": [
            {
                "chunk_id": 4,
                "text": "Contact the support team to reset your password.",
                "score": 0.43,
            }
        ],
        "citation_check": {
            "cited_chunk_ids": [4],
            "unknown_chunk_ids": [],
            "has_citations": True,
            "all_cited_ids_available": True,
        },
        "timings": {
            "retrieval_seconds": 0.1,
            "generation_seconds": 0.2,
            "total_seconds": 0.3,
        },
    }


class AskApiTests(unittest.TestCase):
    def setUp(self) -> None:
        app.state.document_index = []

        self.client = TestClient(
            app,
            raise_server_exceptions=False,
        )

    def tearDown(self) -> None:
        self.client.close()

    @patch("api.answer_with_retrieval")
    def test_valid_request_returns_answer(self, mock_rag):
        mock_rag.return_value = sample_response()

        response = self.client.post(
            "/ask",
            json={"question": "How do I reset my password?"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["answer"],
            "Contact the support team. [Chunk 4]",
        )
        mock_rag.assert_called_once_with(
            question="How do I reset my password?",
            index=[],
            top_k=2,
        )

    @patch("api.answer_with_retrieval")
    def test_missing_question_returns_422(self, mock_rag):
        response = self.client.post("/ask", json={})

        self.assertEqual(response.status_code, 422)
        mock_rag.assert_not_called()

    @patch("api.answer_with_retrieval")
    def test_blank_question_returns_422(self, mock_rag):
        response = self.client.post(
            "/ask",
            json={"question": "   "},
        )

        self.assertEqual(response.status_code, 422)
        mock_rag.assert_not_called()

    @patch("api.answer_with_retrieval")
    def test_missing_answer_returns_500(self, mock_rag):
        result = sample_response()
        del result["answer"]
        mock_rag.return_value = result

        response = self.client.post(
            "/ask",
            json={"question": "How do I reset my password?"},
        )

        self.assertEqual(response.status_code, 500)


if __name__ == "__main__":
    unittest.main()