from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.db import Base
from app.deps import engine
from app.features.agent.router import router as agent_router
from app.features.ask.router import router as ask_router
from app.features.ask.traces import router as traces_router
from app.features.evals.router import router as evals_router
from app.features.identity.router import router as identity_router
from app.features.ingest.router import router as ingest_router
from app.features.usage.router import router as usage_router
from app.kernel.errors import DomainError

app = FastAPI(title="Grounded Agent API", version="0.1.0", redirect_slashes=False)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_origin_regex=".*", allow_credentials=False, allow_methods=["*"], allow_headers=["*"])

@app.exception_handler(DomainError)
async def domain_error(_, exc: DomainError):
    return JSONResponse({"code": exc.code, "message": exc.message}, status_code=exc.status)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(identity_router)
app.include_router(ingest_router)
app.include_router(ask_router)
app.include_router(agent_router)
app.include_router(evals_router)
app.include_router(usage_router)
app.include_router(traces_router)
