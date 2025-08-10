import streamlit as st
import requests
import streamlit as st
import json     
import time
import os
import logging


    
st.set_page_config(page_title="RAG AGENT", layout="centered")


# Get current script directory
log_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(log_dir, "app.log")

# Configure logging
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,  # You can use DEBUG, WARNING, ERROR
    format="%(asctime)s [%(levelname)s] %(message)s"
)
APP_NAME = "RAG_AGENT"
API_BASE_URL = "http://localhost:8000"

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = f"session-{int(time.time())}"

if "user_id" not in st.session_state:
    st.session_state.user_id = "user"

def create_session():
    """Create a new session with the speaker agent."""
    response = requests.post(
        f"{API_BASE_URL}/apps/{APP_NAME}/users/{st.session_state.user_id}/sessions/{st.session_state.session_id}",
        headers={"Content-Type": "application/json"},
        data=json.dumps({})
    )
    
    if response.status_code == 200:
        logging.info(f"Session created successfully: {response.json()}")
        return True
    else:
        logging.error(f"Failed to create session: {response.status_code} - {response.text}")
        st.error("Failed to create session. Please try again.")
        return False



def send_message(message):
    
    # Add user message to chat
    messages={"role": "user", "content": message}
    
    # Send message to API
    response = requests.post(
        f"{API_BASE_URL}/run",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "app_name": APP_NAME,
            "user_id": st.session_state.user_id,
            "session_id": st.session_state.session_id,
            "new_message": {
                "role": "user",
                "parts": [{"text": message}]
            }
        })
    )
    
    if response.status_code == 200:
        events = response.json()
        for event in events:
            for part in event.get("content", {}).get("parts", []):
                if "text" in part:
                    output = part["text"]
                    break
        st.session_state.messages.append({"role": "assistant", "content": output})  

        







st.title("RAG CHATBOT")
# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(message["content"])

# Input box for new user message

if "flag" not in st.session_state:
    st.session_state.flag = False
if "start" not in st.session_state:
    st.session_state.start = True
if st.session_state.start:
    st.session_state.start = False
    st.session_state.flag=create_session()  # Ensure session is created before sending message

if st.session_state.flag:
    prompt = st.chat_input("Type your message here...")
    if prompt :
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        send_message(prompt)
        st.rerun()
