from app.services.qdrant_service import QdrantService

qdrant = QdrantService()

collections = qdrant.client.get_collections()

print(collections)