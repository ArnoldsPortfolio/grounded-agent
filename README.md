# Grounded Agent

Document-grounded answers plus a tool-using agent with traces and evals.

The app may only answer from files you uploaded. If the docs do not support an answer, it refuses.

## Run locally

API on **8020**, UI on **3020** (so Live Board can keep 8010 / 3010).

```bash
cd ~/grounded-agent/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8020
```

```bash
cd ~/grounded-agent/frontend
npm install
npm run dev
```

Open http://localhost:3020 — sign up, upload a `.txt` or `.md` file, ask.
