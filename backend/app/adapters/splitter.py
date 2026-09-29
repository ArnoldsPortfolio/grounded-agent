def split_text(text: str, size: int = 400) -> list[str]:
    words = text.split()
    if not words:
        return []
    chunks, buf = [], []
    for word in words:
        buf.append(word)
        if len(" ".join(buf)) >= size:
            chunks.append(" ".join(buf))
            buf = buf[-20:]
    if buf:
        chunks.append(" ".join(buf))
    return chunks
