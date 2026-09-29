from pydantic import BaseModel, Field
class Citation(BaseModel):
    document_id: str
    chunk_id: str
    title: str
    quote: str
    score: float
class CitedAnswer(BaseModel):
    grounded: bool
    answer: str = ""
    refusal: str | None = None
    citations: list[Citation] = Field(default_factory=list)
    run_id: str
    tokens: int = 0
class IngestResult(BaseModel):
    document_id: str
    title: str
    chunks: int
class AgentStep(BaseModel):
    thought: str
    tool: str | None = None
    tool_input: str | None = None
    tool_output: str | None = None
class AgentRunResult(BaseModel):
    run_id: str
    steps: list[AgentStep]
    final: CitedAnswer
class EvalScore(BaseModel):
    case_id: str
    question: str
    passed: bool
    reason: str
    grounded: bool
