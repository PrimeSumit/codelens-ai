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
        print("\nRetrieved chunks:")
        for chunk in chunks:
            payload = chunk.payload
            print(
                payload["file_path"],
                payload["name"],
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
                f"Type: {payload['type']}\n"
                f"Name: {payload['name']}\n"
                f"Lines: {payload.get('start_line', '-')}-{payload.get('end_line', '-')}\n\n"
                f"{payload['code']}\n"
                f"{'-' * 80}\n\n"
            )

        prompt = f"""
    You are CodeLens AI, an expert software engineer specializing in understanding and explaining software repositories.

    Answer ONLY using the repository context below.

    ## Rules

    - Never invent code or functionality.
    - Use only the provided repository context.
    - If the context is insufficient, clearly say so.
    - Keep explanations concise and technically accurate.
    - Mention relevant file names.
    - Prefer production code over tests unless the question is about tests.

    ## Response Format

    Write the answer in Markdown.

    Start with a short summary.

    Use headings and bullet points.

    If explaining a file, include:

    # File Overview

    ## Purpose

    ## Main Components

    ## How It Works

    ## Related Files

    ## Sources

    If explaining a function, include:

    # Function Overview

    ## Location

    ## Purpose

    ## Parameters

    ## Returns

    ## How It Works

    ## Related Components

    ## Sources

    If explaining a workflow, include:

    # Workflow

    ## Overview

    ## Step-by-Step Flow

    ## Files Involved

    ## Summary

    ## Sources

    Repository Context:

    {context}

    User Question:

    {question}

    Answer:
    """

        return prompt