from fastapi import HTTPException,UploadFile
from pathlib import Path
import shutil,zipfile
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.repository import Repository
from app.schemas.repository import RepositoryCreate,RepoUpdate
from app.utils.file_scanner import scan_repo

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
    
    def upload_repo(self,file:UploadFile):
        if not file.filename.lower().endswith(".zip"):
            raise HTTPException(
                status_code=400,
                detail="Only ZIP files are allowed."
            )

        storage_path=Path("storage")
        storage_path.mkdir(exist_ok=True)
        
        zip_path=storage_path / file.filename

        with zip_path.open("wb") as buffer:
            shutil.copyfileobj(file.file,buffer)
        
        extract_path=storage_path / zip_path.stem
        extract_path.mkdir(exist_ok=True)

        with zipfile.ZipFile(zip_path,"r") as zip_ref:
            zip_ref.extractall(extract_path)

        files = scan_repo(extract_path)

        return {
            "message": "Repository scanned successfully",
            "files": [str(file) for file in files]
        }