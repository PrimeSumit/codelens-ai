from openai import OpenAI,APITimeoutError,APIConnectionError,RateLimitError,InternalServerError
from app.core.config import settings
import time,logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.NVIDIA_API_KEY,
            base_url="https://integrate.api.nvidia.com/v1",
            timeout=30.0,
        )
        self.models = [
            settings.PRIMARY_LLM_MODEL,
            settings.FALLBACK_LLM_MODEL,
        ]
        self.max_retries = 2

    def _generate(self, model: str, question: str) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
        )

        return response.choices[0].message.content

    def chat(self, question: str) -> str:
        
        for model in self.models:
            logger.info("Trying model: %s", model)

            for attempt in range(self.max_retries):
                try:
                    logger.info("Attempt %d/%d",attempt + 1,self.max_retries,)

                    answer = self._generate(model, question)

                    logger.info("Model %s generated the response successfully.", model)

                    return answer

                except (APITimeoutError,APIConnectionError,RateLimitError,InternalServerError) as e:
                    logger.warning("Model %s failed with %s: %s",model,type(e).__name__,e,)
                    if attempt < self.max_retries - 1:
                        logger.info("Retrying in 2 seconds...")
                        time.sleep(2)

            logger.warning("Switching to fallback model.")

        raise RuntimeError(
            "Unable to generate a response. All configured LLM models failed."
        )