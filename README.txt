MinecraftGPT Mod

This project is a Minecraft Fabric mod that connects to a locally hosted AI (LLaMA 3 via Ollama) to provide in-game GPT-style chat responses. It includes both a FastAPI backend and a Minecraft client mod.

---

🧠 Prerequisites

Python Backend (FastAPI + Ollama)
1. Install Python 3.11+  
   https://www.python.org/downloads/

2. Install dependencies  
   In the project folder, run:
   pip install fastapi uvicorn requests

3. Install Ollama  
   https://ollama.com/download

4. Start the Ollama server  
   In a terminal:
   ollama serve

5. Run the FastAPI proxy server  
   In a separate terminal:
   python server.py

---

🧪 Testing the Minecraft Mod

1. Install IntelliJ IDEA
   https://www.jetbrains.com/idea/download

2. Install Minecraft Development Plugin
   In IntelliJ:
   - Go to File > Settings > Plugins
   - Search for Minecraft Development
   - Install it and restart the IDE

3. Open the project
   - Open the folder fabric-example-mod-1.21 (or your project root) in IntelliJ.

4. Run the Minecraft Client
   Open the IntelliJ terminal (Alt + F12) and run:
   .\gradlew.bat runClient

This will compile and launch the modded Minecraft client with your GPT-powered chat mod enabled.

---

💬 Using the Mod

In-game, open the chat and type:
?ask How do I make a crafting table?

You’ll receive a short, accurate response from the AI—powered by LLaMA 3, grounded in Minecraft knowledge.

---

🛠 Troubleshooting

- If you see 422 or 502 errors, ensure that:
  - Ollama is running (ollama serve)
  - llama3 is downloaded (ollama run llama3)
  - server.py is active and reachable on http://localhost:8000
