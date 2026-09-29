from fastapi import APIRouter, Depends, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.deps import get_db, get_user_id
from app.features.ingest.service import IngestService
router = APIRouter(prefix="/documents", tags=["ingest"])
class TextBody(BaseModel):
    title: str
    text: str
@router.get("")
def list_documents(user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return IngestService(db).list_docs(user_id)
@router.post("/text")
def ingest_text(body: TextBody, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return IngestService(db).index(user_id, body.title, body.text)
@router.post("/upload")
async def ingest_file(file: UploadFile, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    raw = (await file.read()).decode("utf-8", errors="ignore")
    return IngestService(db).index(user_id, file.filename or "upload.txt", raw)
