from dotenv import load_dotenv
import os
load_dotenv()

from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def read_root():
    return { 
        "message": "Hello, How are you doing today?"
        }

