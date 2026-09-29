from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.deps import get_db, get_user_id
from app.features.ask.service import AskService
router = APIRouter(prefix="/ask", tags=["ask"])
class AskBody(BaseModel):
    question: str = Field(min_length=2, max_length=500)
@router.post("")
def ask(body: AskBody, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return AskService(db).ask(user_id, body.question)
