import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional

from ai.agent import main as run_agent
from ai.schema import AgentResponse

app = FastAPI(
    title="Vibeflix Agentic API",
    description="Backend server for a film-bro movie recommender powered by Gemini and TMDB.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    query: str = Field(description="The natural language prompt from the user")
    thread_id: str = Field(description="Unique identifier for user's chat sessions")


@app.get("/")
def health_check():
    """Verify the server is running or not"""
    return {"status": "healthy"}


@app.post("/chat")
async def chat_with_agent(payload: ChatRequest):
    """
    Calls agent
    """

    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        agent_output = run_agent(payload.query, payload.thread_id)
        return agent_output

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occured : {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", port="3000", reload=True)
