from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.deps import get_db, get_user_id
from app.features.usage.service import UsageService
router = APIRouter(prefix="/usage", tags=["usage"])
@router.get("")
def usage(user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return UsageService(db).snapshot(user_id)
