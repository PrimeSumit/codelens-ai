import logging

from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)


class RAGService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.qdrant_service = QdrantService()
        self.llm_service = LLMService()

    def ask(self, repository_id: int, question: str) -> str:
        query_embedding = self.embedding_service.query(question)

        chunks = self.qdrant_service.search(
            repository_id=repository_id,
            query_embedding=query_embedding,
        )

        if not chunks:
            return (
                "I couldn't find any relevant code in this repository "
                "to answer your question."
            )

        prompt = self._build_prompt(question, chunks)

        answer = self.llm_service.chat(prompt)

        return answer
    def _build_prompt(self, question: str, chunks: list) -> str:
        context = ""

        for chunk in chunks:
            payload = chunk.payload

            context += (
                f"File: {payload['file_path']}\n"
                f"Type: {payload['type']}\n\n"
                f"{payload['code']}\n"
                f"{'-' * 60}\n\n"
            )

        prompt = f"""
            You are an AI assistant that answers questions about a software repository.

            Use ONLY the repository context below.

            If the answer is not present in the context, say you don't have enough information.

            Repository Context:
                {context}

            Question:
                {question}

            Answer:
        """

        return prompt
        