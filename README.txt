AI Chat Assistant

This project consists of two main components:

1. Python FastAPI Backend: A proxy server that forwards chat messages to a locally hosted Ollama LLaMA 3 model and returns AI-generated responses.
2. Minecraft Fabric Mod: A client-side mod built with Fabric for Minecraft 1.21.5 that hooks into the in-game chat to provide GPT-style answers.

---

🧠 Prerequisites

Python Backend
1. Install Python 3.11 or newer:

   https://www.python.org/downloads/
2. Install required Python packages:
   pip install fastapi uvicorn requests

3. Install Ollama (for LLaMA 3 model support):
   https://ollama.com/download

4. Start the Ollama server:
   ollama serve

5. Run the FastAPI proxy server:
   python server.py

---

🧪 Installing the Minecraft Mod
1. Install Minecraft Java Edition 1.21.5 via the official launcher.

2. Download the Fabric Mod Loader installer:
   https://fabricmc.net/use/

3. Run the Fabric installer and select version 1.21.5.

4. Download the Fabric API JAR matching 1.21.5:
   https://www.curseforge.com/minecraft/mc-mods/fabric-api

5. Copy JARs to the Minecraft mods folder:
   - `AIChatAssistantClientMod.jar` (compiled mod)
   - `fabric-api-<version>.jar`
   %appdata%/.minecraft/mods/

---

💬 Using the Mod

1. Ensure both Ollama (`ollama serve`) and the FastAPI server (`python server.py`) are running on `localhost:8000`.

2. Launch the Minecraft Launcher, select the Fabric profile for 1.21.5, and click Play.

3. In-game, open chat and type:
   ?ask How do I get a Totem of Undying?

4. Watch for the response prefixed with:
   [AI Chat Assistant] <answer>

---

🛠 Troubleshooting

- No response or errors in chat:
  - Verify `ollama serve` is running and the `llama3` model is downloaded.
  - Confirm `server.py` is active and accessible at `http://localhost:8000`.
  - Ensure your Fabric Loader and Fabric API versions match Minecraft 1.21.5.
  - Check that both `AIChatAssistantClientMod.jar` and the Fabric API JAR are in the correct `mods` folder.
