from openai import OpenAI
from app.core.config import settings

class EmbeddingService:
    def __init__(self):
        self.client=OpenAI(api_key=settings.NVIDIA_API_KEY,base_url="https://integrate.api.nvidia.com/v1")

    def passage(self,texts:list[str])->list[list[float]]:
        embeddings = []

        batch_size = 32

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            response=self.client.embeddings.create(
                input=batch,
                model=settings.EMBEDDING_MODEL,
                encoding_format="float",
                extra_body={
                    "input_type": "passage",
                    "truncate": "NONE",
                },
            )
            embeddings.extend(
                item.embedding for item in response.data
            )
            
        return embeddings

    def query(self,text:str)->list[float]:
        response=self.client.embeddings.create(
            input=[text],
            model=settings.EMBEDDING_MODEL,
            encoding_format="float",
            extra_body={
                "input_type": "query",
                "truncate": "NONE",
            },

        )
        return response.data[0].embedding