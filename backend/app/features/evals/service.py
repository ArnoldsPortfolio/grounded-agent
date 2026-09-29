from sqlalchemy import select
from sqlalchemy.orm import Session
from app.contracts.answers import EvalScore
from app.features.ask.service import AskService
from app.kernel.ids import new_id
from app.models import EvalRow
DEFAULTS = [("What is the refund window?", "14 days", 0), ("What topping is on the pizza?", "", 1)]
class EvalService:
    def __init__(self, db: Session):
        self.db = db
    def seed(self, owner_id: str) -> None:
        if self.db.scalar(select(EvalRow.id).where(EvalRow.owner_id == owner_id)):
            return
        self.db.add_all([EvalRow(id=new_id(), owner_id=owner_id, question=q, must_cite=cite, expect_refuse=ref) for q, cite, ref in DEFAULTS])
        self.db.commit()
    def run_suite(self, owner_id: str) -> list[EvalScore]:
        self.seed(owner_id)
        cases = list(self.db.scalars(select(EvalRow).where(EvalRow.owner_id == owner_id)))
        return [self._score(owner_id, case) for case in cases]
    def _score(self, owner_id: str, case: EvalRow) -> EvalScore:
        result = AskService(self.db).ask(owner_id, case.question)
        if case.expect_refuse:
            ok = not result.grounded
            reason = "refused" if ok else "answered when it should refuse"
        else:
            blob = (result.answer + " " + " ".join(c.quote for c in result.citations)).lower()
            ok = result.grounded and case.must_cite.lower() in blob
            reason = "cited expected span" if ok else "missed expected span"
        return EvalScore(case_id=case.id, question=case.question, passed=ok, reason=reason, grounded=result.grounded)
