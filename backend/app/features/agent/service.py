from sqlalchemy.orm import Session
from app.contracts.answers import AgentRunResult, AgentStep
from app.features.ask.service import AskService
from app.kernel.ids import new_id
class AgentService:
    def __init__(self, db: Session):
        self.db = db
    def run(self, owner_id: str, question: str) -> AgentRunResult:
        run_id = new_id()
        asker = AskService(self.db)
        search = AgentStep(thought="Search the indexed documents.", tool="search_docs", tool_input=question)
        hits = asker.retrieve(owner_id, question)
        search.tool_output = f"{len(hits)} chunks"
        result = asker.ask(owner_id, question)
        result.run_id = run_id
        stop = AgentStep(thought="Stop: grounded." if result.grounded else "Stop: refuse.")
        return AgentRunResult(run_id=run_id, steps=[search, stop], final=result)
