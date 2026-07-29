from qdrant_client import QdrantClient
from qdrant_client.models import Distance,VectorParams,PointStruct
from app.core.config import settings
from uuid import uuid4
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

    def upsert_chunks(self,repository_id:int,chunks:list[dict],embeddings:list[list[float]]):
        if len(chunks)!=len(embeddings):
            raise ValueError("Number of chunks and embeddings must be equal.")

        points=[]
        for chunk,embedding in zip(chunks,embeddings):
            point=PointStruct(
                id=str(uuid4()),
                vector=embedding,
                payload={
                    "repository_id": repository_id,
                    "file_path": chunk["file_path"],
                    "type": chunk["type"],
                    "name": chunk["name"],
                    "start_line": chunk["start_line"],
                    "end_line": chunk["end_line"],
                    "code": chunk["code"]
                }
                
            )
            points.append(point)
        self.client.upsert(collection_name=settings.QDRANT_COLLECTION,
                               points=points)
        return len(points)