from fastapi import APIRouter,Depends,UploadFile,File

from sqlalchemy.orm import Session


from app.db.session import get_db
from app.schemas.chat import ChatRequest,ChatResponse
from app.schemas.repository import RepositoryCreate,RepoUpdate
from app.services.repository_service import RepositoryService
from app.services.rag_service import RAGService

router=APIRouter(prefix="/repositories",tags=["Repositories"])
service=RepositoryService()
rag_service = RAGService()

@router.post("/")
def create_repository(
    repository: RepositoryCreate,
    db:Session=Depends(get_db),
):
    return service.create_repo(db,repository)

@router.get("/")
def getrepo(
    db:Session=Depends(get_db),

):
    return service.get_repos(db)

@router.get("/{repository_id}")
def get_repo(
    repository_id:int,
    db:Session=Depends(get_db)
):
    return service.get_repo_by_id(db,repository_id)

@router.delete("/{repository_id}")
def delete_repo(
    repository_id:int,
    db:Session=Depends(get_db)
):
    return service.delete_repo(db,repository_id)

@router.put("/{repository_id}")
def update_repo(
    repository_id:int,
    repository: RepoUpdate,
    db:Session=Depends(get_db)
):
    return service.update_repo(db,repository_id,repository)

@router.post("/upload")
def upload_repo(db:Session=Depends(get_db),file:UploadFile=File(...)):
    return service.upload_repo(db,file)



@router.post("/{repository_id}/chat",response_model=ChatResponse)
def chat_with_repo(
    repository_id:int,
    request:ChatRequest

):
    answer=rag_service.ask(
        repository_id=repository_id,
        question=request.question,
    )
    return ChatResponse(answer=answer)