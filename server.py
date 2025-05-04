from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Literal
import requests

WIKI_API = "https://minecraft.fandom.com/api.php"

def fetch_wiki_summary(query: str, sentences: int = 3) -> str:
    # search wiki for page titles
    resp = requests.get(WIKI_API, params={
        "action":   "query",
        "list":     "search",
        "srsearch": query,
        "srlimit":  1,
        "format":   "json"
    })
    data = resp.json()
    hits = data.get("query", {}).get("search", [])
    if not hits:
        return ""

    pageid = hits[0]["pageid"]

    # get intros of pages
    resp2 = requests.get(WIKI_API, params={
        "action":     "query",
        "pageids":    pageid,
        "prop":       "extracts",
        "explaintext": True,
        "exsentences": sentences,
        "exintro":     True,
        "format":      "json"
    })
    pages = resp2.json().get("query", {}).get("pages", {})
    return pages[str(pageid)].get("extract", "")

OLLAMA_API_URL = "http://localhost:11434"

class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    messages: List[Message] = Field(..., description="Conversation history")

class ChatResponse(BaseModel):
    role: Literal["assistant"]
    content: str

app = FastAPI(
    title="MinecraftGPT Server",
    description="Receives chat from Minecraft mod and replies via LLaMA 3"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = (
    "You are a Minecraft expert.  "
    "Always answer in 1 short paragraph (≤4 sentences), "
    "focus only on Minecraft mechanics or lore, and be 100% factually correct."
)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # extract user question
    user_q = request.messages[-1].content

    # fetch wiki snippet
    wiki_snip = fetch_wiki_summary(user_q)
    wiki_msg = (
        f"Relevant wiki excerpt:\n{wiki_snip}"
        if wiki_snip else
        "No wiki article found; answer from your internal knowledge only."
    )

    # build full prompt list
    messages = [
        {"role": "system",    "content": SYSTEM_PROMPT},
        {"role": "system",    "content": wiki_msg},
        *[m.dict() for m in request.messages]
    ]

    # call ollama
    try:
        resp = requests.post(
            f"{OLLAMA_API_URL}/v1/chat/completions",
            json={"model": "llama3", "messages": messages},
            timeout=15
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        # fail with a 502 but return the HTTPException so FastAPI sees it
        raise HTTPException(status_code=502, detail=f"Ollama error: {e}")

    # parse and return
    data = resp.json()
    choice = data["choices"][0]["message"]
    return ChatResponse(role=choice["role"], content=choice["content"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="localhost", port=8000, reload=True)
