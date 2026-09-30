from dotenv import load_dotenv
import os
load_dotenv()

from fastapi import Body, FastAPI
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()
HTML_FILE = Path(__file__).parent / "index.html"

# RESTAPI
@app.get("/")
def read_root():
    return FileResponse(HTML_FILE)

@app.post("/submit")
def submit_message(message: str = Body(..., embed=True)):
    return {"message": message}
