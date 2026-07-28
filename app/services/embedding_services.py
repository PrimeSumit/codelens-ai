from openai import OpenAI
from app.core.config import settings

class EmbeddingServices:
    def __init__(self):
        self.client=OpenAI(api_key=settings.NVIDIA_API_KEY,base_url="https://integrate.api.nvidia.com/v1")

    def passage(self,texts:list[str])->list[list[float]]:
        response=self.client.embeddings.create(
            input=texts,
            model=settings.EMBEDDING_MODEL,
            encoding_format="float",
            extra_body={
                "input_type": "passage",
                "truncate": "NONE",
            },
        )
        return [item.embedding for item in response.data]

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