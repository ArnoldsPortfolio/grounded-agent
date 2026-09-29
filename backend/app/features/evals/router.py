from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.deps import get_db, get_user_id
from app.features.evals.service import EvalService
router = APIRouter(prefix="/evals", tags=["evals"])
@router.post("/run")
def run_evals(user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return EvalService(db).run_suite(user_id)
