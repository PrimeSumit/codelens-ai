from qdrant_client import QdrantClient
from qdrant_client.models import Distance,VectorParams,PointStruct,Filter,FieldCondition,MatchValue
from app.core.config import settings
from uuid import uuid4
from qdrant_client.models import PayloadSchemaType



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
        self.client.create_payload_index(
            collection_name=settings.QDRANT_COLLECTION,
            field_name="repository_id",
            field_schema=PayloadSchemaType.INTEGER,
        )
        
        return True

    def upsert_chunks(self,repository_id:int,chunks:list[dict],embeddings:list[list[float]]):
        if len(chunks)!=len(embeddings):
            raise ValueError("Number of chunks and embeddings must be equal.")

        points=[]
        for chunk,embedding in zip(chunks,embeddings):
            payload = {
                "repository_id": repository_id,
                "file_path": chunk["file_path"],
                "file_category": chunk["file_category"],
                "type": chunk["type"],
                "name": chunk["name"],
                "code": chunk["code"],
            }

            if "start_line" in chunk:
                payload["start_line"] = chunk["start_line"]
                payload["end_line"] = chunk["end_line"]

            point=PointStruct(
                id=str(uuid4()),
                vector=embedding,
                payload=payload
                
            )
            points.append(point)
        
        self.client.upsert(
            collection_name=settings.QDRANT_COLLECTION,
            points=points,
        )

        return len(points)

    def search(self,repository_id:int,query_embedding:list[float],limit:int=20):
        
        query_filter=Filter(
            must=[FieldCondition(key="repository_id",match=MatchValue(value=repository_id))]
        )
        result=self.client.query_points(
            collection_name=settings.QDRANT_COLLECTION,
            query=query_embedding,
            query_filter=query_filter,
            limit=limit
        )
        return result.points
