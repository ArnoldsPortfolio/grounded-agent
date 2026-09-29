import json
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.deps import get_db, get_user_id
from app.models import TraceRow
router = APIRouter(prefix="/traces", tags=["traces"])
@router.get("/{run_id}")
def traces(run_id: str, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    rows = list(db.scalars(select(TraceRow).where(TraceRow.run_id == run_id, TraceRow.owner_id == user_id)))
    return [{"kind": r.kind, "detail": json.loads(r.detail)} for r in rows]
