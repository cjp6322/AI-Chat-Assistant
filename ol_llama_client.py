import requests
from typing import List, Dict

class OllamaClientHTTP:
    def __init__(self, host: str = "http://127.0.0.1", port: int = 8000):
        # Point to FastAPI proxy instead of Ollama endpoint
        self.base_url = f"{host}:{port}"

    def chat(self, messages: List[Dict[str, str]]) -> Dict[str, str]:
        """
        Sends a list of messages to the FastAPI proxy and returns the assistant reply.
        Expects proxy to return a flat JSON: {"role": "assistant", "content": "..."}
        """
        url = f"{self.base_url}/chat"
        response = requests.post(url, json={"messages": messages})
        response.raise_for_status()
        # Proxy returns {'role': 'assistant', 'content': '...'}
        return response.json()

# Example usage:
# client = OllamaClientHTTP()
# reply = client.chat([{"role": "user", "content": "Hello, Ollama!"}])
# print(reply.get("content"))
