from fastapi import HTTPException,UploadFile
from pathlib import Path
import shutil,zipfile,tempfile
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.repository import Repository
from app.schemas.repository import RepositoryCreate,RepoUpdate
from app.utils.file_scanner import scan_repo
from app.utils.file_chunking import chunk_file

from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService

class RepositoryService:
    def __init__(self):
        self.embedding_service=EmbeddingService()
        self.qdrant_service=QdrantService()

    def create_repo(self,db:Session,repository:RepositoryCreate):
        repo=Repository( name=repository.name,
        github_url=repository.github_url,
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
            raise HTTPException(status_code=404,detail="Repository Not Found.")
        repo.name=repository.name
        repo.github_url=repository.github_url

        db.commit()
        db.refresh(repo)

        return repo

    def delete_repo(self,db:Session,repo_id:int):
        repo=db.get(Repository,repo_id)
        if repo is None:
            raise HTTPException(status_code=404,detail="Repository Not Found.")
        db.delete(repo)
        db.commit()

        return {"message": "Repository deleted successfully"}
    
    def upload_repo(self,db:Session,file:UploadFile):
        if not file.filename.lower().endswith(".zip"):
            raise HTTPException(
                status_code=400,
                detail="Only ZIP files are allowed."
            )

        
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            zip_path = temp_path / file.filename

            with zip_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            extract_path = temp_path / zip_path.stem
            extract_path.mkdir(exist_ok=True)
            try:
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(extract_path)
                zip_path.unlink()
            except zipfile.BadZipFile:
                raise HTTPException(
                status_code=400,
                detail="Invalid ZIP file."
                )
            files=scan_repo(extract_path)
            print("\nScanned files:")
            for file in files:
                print(file)

            if not files:
                
                return {
                    "message": "No supported files found.",
                    "files": 0,
                    "chunks": 0,
                    }
            all_chunks=[]
            for file_path in files:
                chunks=chunk_file(
                    file_path=file_path,
                    repo_root=extract_path,)
                
                all_chunks.extend(chunks)
            if not all_chunks:
                return {
                        "message": "No chunks found.",
                        "files": len(files),
                        "chunks": 0,
                        }
            repo = Repository(
                name=zip_path.stem,
                github_url=None,
            )

            db.add(repo)
            db.commit()
            db.refresh(repo)

            texts = [chunk["code"] for chunk in all_chunks]

            embeddings = self.embedding_service.passage(texts)

            print("\nChunks to upload:")
            for chunk in all_chunks:
                if "auth" in chunk["file_path"]:
                    print(chunk["file_path"], chunk["name"])
            self.qdrant_service.upsert_chunks(
                repository_id=repo.id,
                chunks=all_chunks,
                embeddings=embeddings
            )
        return {
            "message": "Repository uploaded and indexed successfully.",
            "repository_id": repo.id,
            "files": len(files),
            "chunks": len(all_chunks),
        }
    
    # def process_repo(self,db:Session,repo_id:int):
    #     repo=db.get(Repository,repo_id)
    #     if repo is None:
    #         raise HTTPException(
    #             status_code=404,
    #             detail="Repository Not found."
    #         )
    #     repo_path=Path(repo.local_path)
    #     if not repo_path.exists():
    #         raise HTTPException(
    #             status_code=404,
    #             detail="Repository directory not found."
    #         )
    #     files=scan_repo(repo_path)
    #     if not files:
    #         return {
    #         "message": "No supported files found.",
    #         "repository_id": repo_id,
    #         "files": 0,
    #         "chunks": 0,
    #         }

    #     all_chunks=[]

    #     for file_path in files:
    #         chunks=chunk_file(file_path)
    #         all_chunks.extend(chunks)

    #     if not all_chunks:
    #         return {
    #         "message": "No chunks found.",
    #         "repository_id": repo_id,
    #         "files": len(files),
    #         "chunks": 0,
    #         }

    #     embeddings=self.embedding_service.passage(
    #         [chunk["code"] for chunk in all_chunks]
    #     )
    #     self.qdrant_service.upsert_chunks(
    #         repository_id=repo_id,
    #         chunks=all_chunks,
    #         embeddings=embeddings
    #     )
    #     return {
    #     "message": "Repository indexed successfully.",
    #     "repository_id": repo_id,
    #     "files": len(files),
    #     "chunks": len(all_chunks),
    #     }
