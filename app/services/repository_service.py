from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.repository import Repository
from app.schemas.repository import RepositoryCreate,RepoUpdate
class RepositoryService:
    def create_repo(self,db:Session,repository:RepositoryCreate):
        repo=Repository( name=repository.name,
        github_url=str(repository.github_url),
    )
        db.add(repo)
        db.commit()
        db.refresh(repo)
        return repo

    def get_repos(self,db:Session):
        repos=db.execute(
            select(Repository)
            ).scalars().all()

        return repos

    def get_repo_by_id(self,db:Session,repo_id:int):
        repo=db.get(Repository,repo_id)
        if repo is None:
            raise HTTPException(
                status_code=404,
                detail="Repository Not Found!"
            )


        return repo


    def update_repo(self,db:Session,repo_id:int,repository:RepoUpdate):
        repo=db.get(Repository,repo_id)
        if repo is None:
            raise HTTPException(status_code=404,detail="Repository Not Found!")
        repo.name=repository.name
        repo.github_url=str(repository.github_url)

        db.commit()
        db.refresh(repo)

        return repo

    def delete_repo(self,db:Session,repo_id:int):
        repo=db.get(Repository,repo_id)
        if repo is None:
            raise HTTPException(status_code=404,detail="Repository Not Found!")
        db.delete(repo)
        db.commit()

        return {"message": "Repository deleted successfully"}