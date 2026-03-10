import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Get API key securely
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OpenAI API key not found. Please set it in the .env file.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Streamlit page configuration
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

st.title("🤖 AI Chatbot Application")
st.write("Chat with an AI powered by OpenAI GPT-3.5-turbo")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to session
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            temperature=0.7,
        )

        ai_response = response.choices[0].message.content

        # Add assistant response to session
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

        with st.chat_message("assistant"):
            st.markdown(ai_response)

    except Exception as e:
        st.error(f"Error: {str(e)}")