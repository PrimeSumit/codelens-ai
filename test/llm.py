from app.core.logging import setup_logging
from app.services.llm_service import LLMService

setup_logging()
llm = LLMService()

answer = llm.chat("Explain what FastAPI is in one sentence.")

print("\nFinal Answer:")
print(answer)