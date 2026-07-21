import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Page Config (Sets up the browser tab)
st.set_page_config(
    page_title="Student help ai",
    page_icon="🤖",
    layout="centered"
)

load_dotenv()

# Environment variables
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# Define Avatars (Emojis work great, or replace with URLs/local image paths)
USER_AVATAR = "D:\chatbot project\pngtree-man-avatar-image-for-profile-png-image_9197908.png"
BOT_AVATAR = "D:\chatbot project\Robot-featured.png"

# 2. Enhanced Header Layout
col1, col2 = st.columns([0.15, 0.85], vertical_alignment="center")
with col1:
    # Top header logo icon
    st.image("D:\chatbot project\92cb6ece120dde64c4abaf5a4c3b97a0.jpg", width=65)
with col2:
    st.title("AI Help Desk")
    st.caption("Powered by Gemini Flash & LangChain")

st.divider()

# LangChain Chatbot Prompt Setup
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please provide responses to the user queries."),
    ("user", "Question:{question}")
])

llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    temperature=0.7
)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# 3. Session State Management (Keeps the chat history alive)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your AI assistant. How can I help you today?"}
    ]

# Render existing conversation history on rerun
for message in st.session_state.messages:
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 4. Modern Modern Chat Input Box
if user_query := st.chat_input("Ask me anything..."):
    
    # Render user message instantly
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Generate bot response using your LangChain chain
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        with st.spinner("Thinking..."):
            response = chain.invoke({'question': user_query})
            st.markdown(response)
            
    # Save bot response to history
    st.session_state.messages.append({"role": "assistant", "content": response})