from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.analyze import router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

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

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join("frontend", "index.html"))

app.include_router(router)
