import hashlib, json, math, re
DIM = 64
WORD = re.compile(r"[a-z0-9]{2,}")
def tokens(text: str) -> list[str]:
    return WORD.findall(text.lower())
def embed(text: str) -> list[float]:
    vec = [0.0] * DIM
    for tok in tokens(text):
        slot = int(hashlib.md5(tok.encode()).hexdigest(), 16) % DIM
        vec[slot] += 1.0
    return _norm(vec)
def dump(vec: list[float]) -> str:
    return json.dumps(vec)
def load(raw: str) -> list[float]:
    return json.loads(raw or "[]")
def cosine(a: list[float], b: list[float]) -> float:
    if not a or not b:
        return 0.0
    return sum(x * y for x, y in zip(a, b))
def _norm(vec: list[float]) -> list[float]:
    n = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / n for x in vec]
