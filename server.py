from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Literal, Optional
import requests

# API endpoints
WIKI_API = "https://minecraft.fandom.com/api.php"
OLLAMA_API_URL = "http://localhost:11434"

# clean user question into fallback search keywords
PREFIXES = [
    "what is", "what are", "what's", "what're",
    "who is", "who's",
    "where is", "where are", "where can i find", "where do i",
    "how do i", "how do i get", "how can i", "how can one", "how do you",
    "how should i", "how to",
    "define", "explain",
    "list", "show me",
    "give me", "provide",
    "instructions for", "steps to",
    "tell me about", "tell me how",
    "why is", "why are",
    "when is", "when did",
    "example of", "examples of", "sample",
    "recommend", "suggest",
    "can you", "could you", "can you explain", "could you explain"
]

def clean_search_query(question: str) -> str:
    q = question.strip().lower()
    for p in PREFIXES:
        if q.startswith(p + " "):
            q = q[len(p) + 1:]
            break
    q = q.rstrip("?!. ")
    return q

# use Ollama to refine search phrase
def refine_search_term(question: str, model: str = "llama3") -> str:
    prompt = (
        "You’re a Minecraft helper. From the user’s question below, pull out only the concise phrase "
        "you’d plug into the Wiki’s search box (e.g., \"Totem of Undying\").\n"
        f"Question: {question}\n"
        "Search phrase:"
    )
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": prompt}],
        "temperature": 0.0
    }
    try:
        r = requests.post(f"{OLLAMA_API_URL}/v1/chat/completions", json=payload, timeout=5)
        r.raise_for_status()
        phrase = r.json()["choices"][0]["message"]["content"].strip().strip('"')
        return phrase
    except Exception:
        return clean_search_query(question)

# sarch minecraft wiki for best-matching page title
def search_wiki_page(query: str) -> str:
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "srlimit": 1,
        "srprop": ""
    }
    resp = requests.get(WIKI_API, params=params)
    resp.raise_for_status()
    hits = resp.json().get("query", {}).get("search", [])
    if not hits:
        raise ValueError(f"No Wiki pages found matching '{query}'")
    title = hits[0]["title"]
    return title

# fetch plaintext summary | full extract if sentences=none
def fetch_wiki_summary(page_title: str, sentences: Optional[int] = None) -> str:
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "explaintext": True,
        "redirects": True,
        "titles": page_title
    }
    if sentences is not None:
        params["exsentences"] = sentences
    resp = requests.get(WIKI_API, params=params)
    resp.raise_for_status()
    pages = resp.json().get("query", {}).get("pages", {})
    page = next(iter(pages.values()))
    extract = page.get("extract", "").strip()
    if not extract:
        raise ValueError(f"Couldn't extract content for '{page_title}'")
    return extract

# FastAPI setup + data models
class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    messages: List[Message] = Field(..., description="Conversation history")

class ChatResponse(BaseModel):
    role: Literal["assistant"]
    content: str

app = FastAPI(
    title="AI Chat Assistant",
    description="Minecraft Q&A using Ollama + Wiki with LLM-driven search term extraction"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    user_q = request.messages[-1].content

    # use LLM to refine search term
    search_term = refine_search_term(user_q)

    # 1) Search wiki and fetch summary
    try:
        title = search_wiki_page(search_term)
        summary = fetch_wiki_summary(title, sentences=None)
    except Exception:
        summary = ""

    # prepare messages and ask Ollama
    messages = [
        {"role": "system", "content": (
            "You are a Minecraft expert. "
            "Use **only** the provided wiki excerpt for your answers, but do not mention or quote it. "
            "Answer directly as if you already know the game. "
            "If the excerpt does not contain the information, reply exactly \"I don’t know.\""
        )},
        {"role": "system", "content": (
            f"Relevant wiki excerpt:\n{summary}" if summary else
            "No wiki article found; if you cannot answer from the excerpt, reply \"I don’t know.\""
        )},
        *[m.dict() for m in request.messages]
    ]
    try:
        resp = requests.post(
            f"{OLLAMA_API_URL}/v1/chat/completions",
            json={"model": "llama3", "messages": messages, "temperature": 0.2},
            timeout=15
        )
        resp.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Ollama error: {e}")

    data = resp.json()
    choice = data["choices"][0]["message"]
    return ChatResponse(role=choice["role"], content=choice["content"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)