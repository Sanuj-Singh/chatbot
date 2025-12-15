from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_community import GoogleSearchAPIWrapper
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import Tool
import streamlit as st
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
GOOGLE_SEARCH_API_KEY = st.secrets["GOOGLE_SEARCH_API_KEY"]
GOOGLE_CSE_ID = st.secrets["GOOGLE_CSE_ID"]
def tools_setup(GOOGLE_API_KEY, GOOGLE_SEARCH_API_KEY, GOOGLE_CSE_ID):

    try:
# 1. Initialize the LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            temperature=0,
            google_api_key=GOOGLE_API_KEY
        )

        search = GoogleSearchAPIWrapper(
            google_api_key=GOOGLE_SEARCH_API_KEY,
            google_cse_id=GOOGLE_CSE_ID)
        search_tool = Tool(
            name="google_search",
            description="Search Google for current information and recent events. Use for questions needing up-to-date answers.",
            func=search.run
        )
        
        return [search_tool], llm
    except Exception as e:
        print("Error setting up tools or LLM: {e}")
        return [], None
def setup_agent():
    tools, llm = tools_setup(GOOGLE_API_KEY, GOOGLE_SEARCH_API_KEY, GOOGLE_CSE_ID)

# saves the conversation history
    memory = MemorySaver()

# create the agent with a custom prompt style giving Alex a Donald Trump–like personality
    agent_graph = create_react_agent(
        model=llm, 
        tools=tools, 
        checkpointer=memory,
        prompt="You are Alex, an AI assistant." \
        " You speak in a Donald Trump–like style: very confident, bold, dramatic,short punchy sentences, superlatives, and persuasive tone," \
        " No political advocacy or policy opinions.Be entertaining, decisive, and concise."
        )

    return agent_graph