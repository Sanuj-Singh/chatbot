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
                if response["messages"]:
                    last_message = response["messages"][-1]
                    
                    # Get the raw content
                    if hasattr(last_message, 'content'):
                        raw_content = last_message.content
                        
                        # FIX: Check if it's that specific list structure you are seeing
                        if isinstance(raw_content, list) and len(raw_content) > 0:
                            # Grab just the 'text' field, ignore 'extras' and 'signature'
                            ai_response = raw_content[0].get('text', '')
                        else:
                            # If it's just a normal string, use it as is
                            ai_response = str(raw_content)
                    else:
                        ai_response = "Sorry, no content attribute found."
                else:
                    ai_response = "Sorry, no response generated."
    # Extract the AI's response content from the response               
                

                st.markdown(ai_response)
                
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
            except Exception as e:
                st.error(f"An error occurred: {e}")