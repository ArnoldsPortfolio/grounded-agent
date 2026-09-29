import re
from app.adapters.embedder import cosine, embed, tokens
from app.contracts.answers import Citation, CitedAnswer
from app.settings import Settings
SENT = re.compile(r"(?<=[.!?])\s+")
def answer_from_chunks(question: str, hits: list[dict], run_id: str) -> CitedAnswer:
    if not hits or hits[0]["score"] < Settings().min_grounding_score:
        return _refuse(run_id)
    cites = [_cite(h) for h in hits[:3]]
    text = _pick_sentence(question, hits[0]["text"])
    return CitedAnswer(grounded=True, answer=text, citations=cites, run_id=run_id, tokens=_cost(question, text))
def _refuse(run_id: str) -> CitedAnswer:
    return CitedAnswer(grounded=False, refusal="Not in the uploaded documents.", run_id=run_id, tokens=8)
def _cite(hit: dict) -> Citation:
    return Citation(document_id=hit["document_id"], chunk_id=hit["id"], title=hit["title"], quote=hit["text"][:280], score=round(hit["score"], 4))
def _pick_sentence(question: str, chunk: str) -> str:
    q = embed(question)
    parts = SENT.split(chunk) or [chunk]
    return max(parts, key=lambda s: cosine(q, embed(s))).strip() or chunk[:240]
def _cost(question: str, answer: str) -> int:
    return len(tokens(question)) + len(tokens(answer))
