import streamlit as st
from chatbot import setup_agent

st.set_page_config(page_title="LangGraph Chatbot", page_icon="ud83eudd46")

st.title("Alex AI Chatbot")

#  ---  Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    # For simplicity, using a static thread ID. In production, generate unique IDs per user/session.
    st.session_state.thread_id = "user_session_1" 

if "agent" not in st.session_state:
    st.session_state.agent = setup_agent()
#  ---  Intro Message from Alex ---
if "alex_intro" not in st.session_state:
    intro_message = "Hey 👋 I’m **Alex**, an AI assistant. How can I help you today?"

    st.session_state.messages.append({
        "role": "assistant",
        "content": intro_message
    })

    st.session_state.alex_intro = True

# chatbot interface that displays messages and takes user input
for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])
    else:
        with st.chat_message("user"):
            st.markdown(message["content"])


# user input is handled  here and response is generated
if prompt := st.chat_input("Ask me anything..."):

    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})


    with st.chat_message("assistant"):
        with st.spinner("I'm Alex Searching and thinking..."):
            try:
               
                config = {"configurable": {"thread_id": st.session_state.thread_id}}
# Invoke the agent with the user prompt and thread ID for context
                
                response = st.session_state.agent.invoke(
                    {"messages": [("user", prompt)]}, 
                    config=config
                                )
                if response["messages"] and hasattr(response["messages"][-1], 'content'):
                    ai_response = response["messages"][-1].content
                else:
                    ai_response = "Sorry, no response generated."
# Extract the AI's response content from the response               
                

                st.markdown(ai_response)
                
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
            except Exception as e:
                st.error(f"An error occurred: {e}")