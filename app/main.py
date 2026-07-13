from fastapi import FastAPI
from app.db.db import engine
app=FastAPI()

@app.get("/")
def root():
    with engine.connect() as connection:
        return {"message":"database connect sucessfully"}