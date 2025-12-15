# Alex AI - LangGraph Chatbot 🤖

**Alex** is an intelligent, conversational AI assistant built using **Streamlit**, **LangGraph**, and **Google Gemini**. 

Designed with a distinct personality (bold, decisive, and persuasive), Alex leverages a ReAct (Reasoning + Acting) agent architecture. This allows the bot to maintain conversation context (memory) and perform real-time Google searches to answer current queries.

## 🌟 Features

* **Personality Driven:** Speaks in a distinct, bold style (Trump-like persona).
* **Powered by Gemini:** Uses Google's `gemini-2.5-flash` model for high-speed, intelligent responses.
* **ReAct Agent:** Capable of reasoning and using tools (Google Search) to fetch up-to-date information.
* **Context Aware:** Uses `MemorySaver` to remember previous parts of the conversation.
* **Streamlit UI:** A clean, responsive web interface.
* **Robust Parsing:** Includes custom logic to handle complex API response structures.

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **LLM Integration:** [LangChain Google GenAI](https://python.langchain.com/docs/integrations/chat/google_generative_ai/)
* **Agent Framework:** [LangGraph](https://langchain-ai.github.io/langgraph/)
* **Search Tool:** Google Programmable Search Engine

## 📂 Project Structure

```text
├── app.py           # Main Streamlit application entry point
├── chatbot.py       # Logic for agent setup, tools, and LLM configuration
├── .streamlit/
│   └── secrets.toml # Configuration file for API keys (Not included in repo)
└── README.md        # Project documentation
