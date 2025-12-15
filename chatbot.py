from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_community import GoogleSearchAPIWrapper
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

def setup_agent(api_key,GOOGLE_SEARCH_API_KEY,GOOGLE_CSE_ID):
    tools = []
    try:
# 1. Initialize the LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            temperature=0,
            google_api_key=api_key
        )
        tools.append(llm)
    # setup search tool
        search = GoogleSearchAPIWrapper(
            google_api_key=GOOGLE_SEARCH_API_KEY,
            google_cse_id=GOOGLE_CSE_ID)
        tools.append(search)
    except Exception as e:
        raise RuntimeError(f"Error setting up tools or LLM: {e}")
   
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