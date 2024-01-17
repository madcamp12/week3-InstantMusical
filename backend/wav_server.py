from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

app = FastAPI()
# CORS 설정
origins = [
    "http://localhost",
    "http://172.10.5.175",
    "https://172.10.5.175"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],           # 모든 HTTP 메소드를 허용
    allow_headers=["*"],           # 모든 HTTP 헤더를 허용
)
app.mount("/static", StaticFiles(directory=Path("wavs")), name="static")