from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.repository import Repository
from app.schemas.repository import RepositoryCreate,RepoUpdate

router=APIRouter(prefix="/repositories",tags=["Repositories"])

@router.post("/")
def create_repository(
    repository: RepositoryCreate,
    db:Session=Depends(get_db),
):
    new_repository=Repository(
        name=repository.name,
        github_url=str(repository.github_url),
    )
    db.add(new_repository)
    db.commit()
    db.refresh(new_repository)
    return new_repository

@router.get("/")
def getrepo(
    db:Session=Depends(get_db),

):
    repositories=db.execute(
        select(Repository)
    ).scalars().all()

    return repositories

@router.get("/{repository_id}")
def get_repo(
    repository_id:int,
    db:Session=Depends(get_db)
):
    repository=db.get(Repository,repository_id)
    if repository is None:
        raise HTTPException(
            status_code=404,
            detail="Repository Not Found!"
        )


    return repository

@router.delete("/{repository_id}")
def delete_repo(
    repository_id:int,
    db:Session=Depends(get_db)
):
    repository=db.get(Repository,repository_id)
    if repository is None:
        raise HTTPException(status_code=404,detail="Repository Not Found!")
    db.delete(repository)
    db.commit()

    return {"message": "Repository deleted successfully"}

@router.put("/{repository_id}")
def updateRepo(
    repository_id:int,
    repository: RepoUpdate,
    db:Session=Depends(get_db)
):
    repo=db.get(Repository,repository_id)
    if repo is None:
        raise HTTPException(status_code=404,detail="Repository Not Found!")
    repo.name=repository.name
    repo.github_url=str(repository.github_url)

    db.commit()
    db.refresh(repo)

    return repo
