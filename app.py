import streamlit as st
from chatbot import setup_agent

st.set_page_config(page_title="LangGraph Chatbot", page_icon="🤖")

st.title("🤖 AI Chatbot with Google & Search")

# --- 1. API Key Handling ---
# Try to get from secrets, otherwise ask user
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter Google API Key", type="password")

if not api_key:
    st.warning("Please provide a Google API Key to proceed.")
    st.stop()

# --- 2. Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    # Unique ID for the conversation memory in LangGraph
    st.session_state.thread_id = "user_session_1" 

if "agent" not in st.session_state:
    st.session_state.agent = setup_agent(api_key)
# --- 2.5. AI Introduction (runs once) ---
if "alex_intro" not in st.session_state:
    intro_message = "Hey 👋 I’m **Alex**, an AI assistant. How can I help you today?"

    st.session_state.messages.append({
        "role": "assistant",
        "content": intro_message
    })

    st.session_state.alex_intro = True

# --- 3. Display Chat History ---
for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])
    else:
        with st.chat_message("user"):
            st.markdown(message["content"])


# --- 4. Chat Input & Processing ---
if prompt := st.chat_input("Ask me anything..."):
    # A. Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # B. Generate Response
    with st.chat_message("assistant"):
        with st.spinner("I'm Alex Searching and thinking..."):
            try:
                # Configuration for memory (connects to specific thread_id)
                config = {"configurable": {"thread_id": st.session_state.thread_id}}
                
                # Invoke the agent
                # LangGraph inputs require a "messages" key
                response = st.session_state.agent.invoke(
                    {"messages": [("user", prompt)]}, 
                    config=config
                )

                # Extract the last message content (the AI's final answer)
                content = response["messages"][-1].content
                ai_response = " ".join(
                part["text"] for part in content if part["type"] == "text"
                )

                st.markdown(ai_response)
                # Save to UI history
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
            except Exception as e:
                st.error(f"An error occurred: {e}")