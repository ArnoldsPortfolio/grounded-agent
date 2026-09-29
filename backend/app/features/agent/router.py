from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.deps import get_db, get_user_id
from app.features.agent.service import AgentService
router = APIRouter(prefix="/agent", tags=["agent"])
class AgentBody(BaseModel):
    question: str = Field(min_length=2, max_length=500)
@router.post("/run")
def run_agent(body: AgentBody, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return AgentService(db).run(user_id, body.question)
