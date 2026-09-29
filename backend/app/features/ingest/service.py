from sqlalchemy import select
from sqlalchemy.orm import Session
from app.adapters.embedder import dump, embed
from app.adapters.splitter import split_text
from app.contracts.answers import IngestResult
from app.kernel.ids import new_id
from app.models import ChunkRow, DocumentRow
class IngestService:
    def __init__(self, db: Session):
        self.db = db
    def index(self, owner_id: str, title: str, text: str) -> IngestResult:
        doc = DocumentRow(id=new_id(), owner_id=owner_id, title=title[:200], source_name=title[:200])
        parts = split_text(text)
        rows = [_chunk(doc, owner_id, i, part) for i, part in enumerate(parts)]
        self.db.add_all([doc, *rows])
        self.db.commit()
        return IngestResult(document_id=doc.id, title=doc.title, chunks=len(rows))
    def list_docs(self, owner_id: str) -> list[dict]:
        rows = list(self.db.scalars(select(DocumentRow).where(DocumentRow.owner_id == owner_id)))
        return [{"id": r.id, "title": r.title} for r in rows]
def _chunk(doc: DocumentRow, owner_id: str, position: int, text: str) -> ChunkRow:
    return ChunkRow(id=new_id(), document_id=doc.id, owner_id=owner_id, text=text, position=position, embedding=dump(embed(text)))
