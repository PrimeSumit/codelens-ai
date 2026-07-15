from fastapi import FastAPI

from app.models import Repository
from app.db.db import Base,engine
from app.api.repository import router as repository_router
Base.metadata.create_all(bind=engine)
app=FastAPI()

app.include_router(repository_router)

@app.get("/")
def root():
    with engine.connect() as connection:
        return {"message":"database connect sucessfully"}