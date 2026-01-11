from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.analyze import router

app = FastAPI(
    title="Elder Risk MVP",
    description="30–60s video → face + voice → risk label",
    version="0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
