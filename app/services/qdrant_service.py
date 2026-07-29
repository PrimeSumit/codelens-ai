from qdrant_client import QdrantClient
from qdrant_client.models import Distance,VectorParams
from app.core.config import settings

class QdrantService:
    def __init__(self):
        self.client=QdrantClient(
            url=settings.QDRANT_URL,api_key=settings.QDRANT_API_KEY
        )

    def create_collection(self)->bool:
        if self.client.collection_exists(
            collection_name=settings.QDRANT_COLLECTION
        ):
            return False
        
        self.client.create_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=settings.VECTOR_DIMENSION,
                distance=Distance.COSINE
            )
        )
        return True