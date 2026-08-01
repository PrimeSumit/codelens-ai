from fastapi import FastAPI
from app.core.logging import setup_logging
from app.models import Repository
from app.db.db import Base,engine
from app.api.repository import router as repository_router
from app.services.qdrant_service import QdrantService

setup_logging()

Base.metadata.create_all(bind=engine)

qdrant = QdrantService()
qdrant.create_collection()

app=FastAPI()

app.include_router(repository_router)

@app.get("/")
def root():
    with engine.connect() as connection:
        return {"message":"database connect sucessfully"}