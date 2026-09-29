POLICY = "Refund policy. Customers may request a refund within 14 days of purchase. After 14 days the sale is final. Contact billing@example.com for refunds."
def auth(client):
    res = client.post("/auth/sign-up", json={"email": "a@b.com", "password": "password1"})
    return {"Authorization": f"Bearer {res.json()['access_token']}"}
def test_health(client):
    assert client.get("/health").json()["status"] == "ok"
def test_ask_cites_or_refuses(client):
    headers = auth(client)
    indexed = client.post("/documents/text", json={"title": "policy.txt", "text": POLICY}, headers=headers)
    assert indexed.status_code == 200
    hit = client.post("/ask", json={"question": "What is the refund window?"}, headers=headers)
    assert hit.status_code == 200, hit.text
    body = hit.json()
    assert body["grounded"] is True
    assert "14" in body["answer"] or any("14" in c["quote"] for c in body["citations"])
    miss = client.post("/ask", json={"question": "What topping is on the pizza?"}, headers=headers)
    assert miss.status_code == 200
    assert miss.json()["grounded"] is False
def test_agent_and_evals(client):
    headers = auth(client)
    client.post("/documents/text", json={"title": "policy.txt", "text": POLICY}, headers=headers)
    run = client.post("/agent/run", json={"question": "What is the refund window?"}, headers=headers)
    assert run.status_code == 200
    assert run.json()["final"]["grounded"] is True
    scores = client.post("/evals/run", headers=headers)
    assert scores.status_code == 200
