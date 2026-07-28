from app.services.embedding_services import EmbeddingServices

embedding_service = EmbeddingServices()

texts = [
    "def login(username, password):\n    return True",
    "class User:\n    pass",
    "def logout():\n    return True",
]

embeddings = embedding_service.passage(texts)

print(f"Number of embeddings: {len(embeddings)}")

for i, embedding in enumerate(embeddings, start=1):
    print(f"Embedding {i}:")
    print(f"  Dimension: {len(embedding)}")
    print(f"  First 5 values: {embedding[:5]}")