from fastapi import FastAPI
from app.mcpserver import orchestrate
from typing import Optional
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = ["*","http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get_llm_response/{message}")
def read_root(
    message: str,
    username: str = Query(...),
    download_summary: bool = Query(False),
    email: Optional[str] = Query(None)
):
    return orchestrate(message, username, download_summary, email)