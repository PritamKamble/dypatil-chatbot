from dotenv import load_dotenv
import os
from pathlib import Path
from typing import Literal
load_dotenv()

from fastapi import Body, FastAPI, HTTPException
from fastapi.responses import FileResponse
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

app = FastAPI()
HTML_FILE = Path(__file__).parent / "index.html"
GEMINI_MODEL = "gemini-3-flash-preview"


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]

# RESTAPI
@app.get("/")
def read_root():
    return FileResponse(HTML_FILE)

@app.post("/submit")
def submit_message(request: ChatRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not configured")
    if not request.messages or request.messages[-1].role != "user":
        raise HTTPException(status_code=400, detail="The conversation must end with a user message")

    try:
        agent = create_agent(
            model=ChatGoogleGenerativeAI(
                model=GEMINI_MODEL,
                google_api_key=api_key,
                temperature=0.7,
            ),
            tools=[],
            system_prompt="You are a helpful assistant.",
        )
        result = agent.invoke({"messages": [message.model_dump() for message in request.messages]})
    except Exception as error:
        detail = str(error).replace(api_key, "[redacted]")[:300]
        raise HTTPException(status_code=502, detail=f"Gemini API request failed: {detail}") from error

    reply = result["messages"][-1].content
    if isinstance(reply, list):
        reply = "".join(part.get("text", "") for part in reply if isinstance(part, dict))
    if not reply:
        raise HTTPException(status_code=502, detail="Gemini returned an empty response")

    return {"message": reply}
