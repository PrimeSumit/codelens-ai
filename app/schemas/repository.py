from pydantic import BaseModel,HttpUrl

class RepositoryCreate(BaseModel):
    name:str
    github_url: HttpUrl

class RepoUpdate(RepositoryCreate):
    pass