from app.core.config import settings
from openai import OpenAI
client=OpenAI(api_key=settings.NVIDIA_API_KEY,
               base_url="https://integrate.api.nvidia.com/v1")

response = client.embeddings.create(
    input="def login(username, password):\n    return True",
    model=settings.EMBEDDING_MODEL,
    encoding_format="float",
    extra_body={
        "input_type": "passage",
        "truncate": "NONE"
    }
)

embedding = response.data[0].embedding

print(type(embedding))
print(len(embedding))
print(embedding[:10])