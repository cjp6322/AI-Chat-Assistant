# AI Chat Assistant Project Report

## 1. Base System Functionality (30 pts)

The AI Chat Assistant mod provides seamless in-game Q&A support for Minecraft players. It supports the following scenarios:

- **Crafting Recipe Lookup**: Users ask `?ask How do I craft a beacon?` and receive step-by-step crafting instructions.
- **Mob Behavior Explanation**: Users ask about mob mechanics, e.g., `?ask How do Endermen teleport?`.
- **Block Property Description**: Users request block attributes, e.g., `?ask What does a slime block do?`.
- **Biome Information Retrieval**: Users query biome characteristics: `?ask What mobs spawn in a Crimson Forest?`.
- **Enchantment Effect Summary**: e.g., `?ask What does the Mending enchantment do?`.
- **Command Usage Guidance**: e.g., `?ask How to use /fill command?`.
- **Structure Location Tips**: e.g., `?ask Where to find a Nether Fortress?`.
- **Potion Brewing Steps**: e.g., `?ask How to brew a Potion of Leaping?`.
- **Server Configuration Help**: e.g., `?ask How to set up a Bukkit plugin?`.

These scenarios demonstrate fundamental AI concepts (LO1) and modular system operation (LO3).

## 2. Prompt Engineering and Model Parameter Choice (10 pts)

- **System Prompts**:  
  - _Refinement Prompt_: Guides the LLM to extract concise search terms.  
  - _Answer Prompt_: Instructs the model to use only the wiki excerpt and answer as a Minecraft expert.  
- **Parameter Settings**:  
  - `temperature=0.2` for balanced creativity and factual consistency.  
  - `max_tokens=512` to limit response length and ensure performance.  
  - `top_p=1.0` (default) to allow the full probability distribution.  
- **Rationale**:  
  - Low temperature reduces hallucinations while permitting varied phrasing.  
  - Token limit prevents overly verbose outputs and reduces latency.  
- **Example Prompts**:  
  - `"You are a Minecraft expert... Use only the provided wiki excerpt... If the excerpt does not contain the information, reply "I don’t know."".`  
  - `"From the user’s question below, pull out only the concise phrase you’d plug into the Wiki’s search box...".`

This shows clear mastery of LO1 by shaping model behavior.

## 3. Tools Usage (15 pts)

- **Ollama LLM**: Uses the local LLaMA 3 model via Ollama for inference (`http://localhost:11434/v1/chat/completions`).
- **Minecraft Fandom Wiki API**: Retrieves page titles and extracts plaintext summaries.
- **FastAPI**: Serves as a lightweight Python proxy for chat messages.
- **Java HTTP Client**: `java.net.http.HttpClient` for sending JSON payloads asynchronously.
- **Gson**: Parses JSON in the Java mod.

These integrations demonstrate LO2 by leveraging Python and Java ecosystems and external APIs.

## 4. Planning & Reasoning (15 pts)

- **Multi-step Pipeline**:  
  1. **Refine Search Term** via LLM.  
  2. **Search Wiki** for best-matching page.  
  3. **Fetch Summary** with plaintext extraction.  
  4. **Invoke Ollama** with context and instructions.  
- **Chain of Thought**: The refinement prompt encourages the model to internally isolate key phrases.  
- **Conversation Coherence**: Contextual history is passed to the model for follow-up questions.  
- **Example**: A two-part question (“How do I get a totem of undying and where to find its ingredients?”) is split, refined, and answered sequentially.

This planning aligns with LO1 by implementing reasoning workflows.

## 5. Retrieval-Augmented Generation (RAG) Implementation (10 pts)

- **Data Source**: Minecraft Fandom Wiki, ensuring factual grounding.  
- **Approach**: Embeds the retrieved extract directly in the LLM prompt to reduce hallucination.  
- **Caching Strategy** (future work): Can cache popular pages to speed up repeat queries.  
- **Demonstration**: In “Crafting Recipe Lookup”, the bot fetches the “Beacon” wiki page and uses its extract verbatim.

This reinforces LO1 and LO2 via advanced AI techniques.

## 6. Additional Tools / Innovation (10 pts)

This project leverages the existing Minecraft mod itself as the primary “innovation”:

- **In-Game Chat Hook**: Uses Fabric’s `ClientSendMessageEvents` API to intercept chat messages prefixed with `?ask`, routing them to the AI backend and displaying results seamlessly in the Minecraft HUD.
- **Non-blocking Asynchronous Calls**: Implements asynchronous HTTP requests via `CompletableFuture.runAsync` in Java so that in-game performance remains smooth while waiting for AI responses.
- **Custom Chat Formatting**: Applies Minecraft text formatting codes (e.g., `§6` for gold) to clearly distinguish AI responses from player chat.
- **Modular Event Handling**: Encapsulates all logic in `ClientChatEventHandler` and `OllamaService`, making it easy to extend with additional commands or features.

By building directly on Fabric’s modding framework and Minecraft’s chat system, this approach showcases creative use of the modding API and solidifies our base AI integration (LO2).

## 7. Code Quality & Modular Design (10 pts)

- **Python Code**:  
  - Modular functions (`refine_search_term`, `search_wiki_page`, `fetch_wiki_summary`, `chat_endpoint`).  
  - PEP-8 compliant with docstrings and type hints.  
  - Dependency management via `requirements.txt`.  
- **Java Mod**:  
  - Clear separation (`AIChatAssistantClientMod`, `ClientChatEventHandler`, `OllamaService`).  
  - Non-blocking I/O with `CompletableFuture`.  
- **Version Control**:  
  - GitHub repository with branched feature development.  
  - `main` branch protected; pull requests for new scenarios.  
- **Documentation**:  
  - `Project.md`, `README.txt`, and in-code comments.

This demonstrates LO2 and LO3 through structured, maintainable code.
