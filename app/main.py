from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="Verified Intelligence Layer",
    description="Deterministic signal scoring, verification, routing, and audit records.",
    version="1.0.0",
)

app.include_router(router)
