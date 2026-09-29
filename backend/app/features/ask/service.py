import json
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.adapters.embedder import cosine, embed, load
from app.adapters.extractive import answer_from_chunks
from app.contracts.answers import CitedAnswer
from app.features.usage.service import UsageService
from app.kernel.ids import new_id
from app.models import ChunkRow, DocumentRow, TraceRow
class AskService:
    def __init__(self, db: Session):
        self.db = db
    def ask(self, owner_id: str, question: str) -> CitedAnswer:
        run_id = new_id()
        hits = self.retrieve(owner_id, question)
        self._trace(run_id, owner_id, "retrieve", {"n": len(hits), "top": hits[0]["score"] if hits else 0})
        result = answer_from_chunks(question, hits, run_id)
        UsageService(self.db).record(owner_id, result.tokens)
        self._trace(run_id, owner_id, "answer", {"grounded": result.grounded})
        return result
    def retrieve(self, owner_id: str, question: str, k: int = 5) -> list[dict]:
        q = embed(question)
        rows = list(self.db.scalars(select(ChunkRow).where(ChunkRow.owner_id == owner_id)))
        scored = [self._hit(row, cosine(q, load(row.embedding))) for row in rows]
        scored.sort(key=lambda h: h["score"], reverse=True)
        return [h for h in scored if h["score"] > 0][:k]
    def _hit(self, row: ChunkRow, score: float) -> dict:
        doc = self.db.get(DocumentRow, row.document_id)
        return {"id": row.id, "document_id": row.document_id, "title": doc.title if doc else "doc", "text": row.text, "score": score}
    def _trace(self, run_id: str, owner_id: str, kind: str, detail: dict) -> None:
        self.db.add(TraceRow(id=new_id(), run_id=run_id, owner_id=owner_id, kind=kind, detail=json.dumps(detail)))
        self.db.commit()
