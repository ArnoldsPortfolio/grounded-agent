from sqlalchemy.orm import Session
from app.kernel.errors import BudgetExceeded, NotFound
from app.models import UserRow
from app.settings import Settings
class UsageService:
    def __init__(self, db: Session):
        self.db = db
    def record(self, user_id: str, tokens: int) -> int:
        user = self._user(user_id)
        if user.tokens_used + tokens > Settings().daily_token_budget:
            raise BudgetExceeded()
        user.tokens_used += tokens
        self.db.commit()
        return user.tokens_used
    def snapshot(self, user_id: str) -> dict:
        user = self._user(user_id)
        cap = Settings().daily_token_budget
        return {"used": user.tokens_used, "cap": cap, "left": cap - user.tokens_used}
    def _user(self, user_id: str) -> UserRow:
        user = self.db.get(UserRow, user_id)
        if not user:
            raise NotFound("User not found")
        return user
