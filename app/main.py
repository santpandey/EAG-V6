from fastapi import FastAPI
from app.mcpserver import orchestrate
from typing import Optional
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi import UploadFile, File, Form
import os

load_dotenv()
app = FastAPI()

origins = ["*","http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/get_llm_response/{message}")
def read_root(
    message: str,
    username: str = Form(...),
    download_summary: bool = Form(False),
    send_email: bool = Form(False),
    email: Optional[str] = Form(None),
    image: UploadFile = File(None)
):
    return orchestrate(message, username, download_summary, send_email, email, image)