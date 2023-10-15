# I created this file for my learning purpose about strealit
import os
import tempfile
import streamlit as st
from streamlit_chat import message
from agent import Agent
from dotenv import load_dotenv

load_dotenv()


st.title("Python Streamlit Learning")
st.header("Machine Learning")
# sub headers
st.subheader("Linear Regression")

st.info("Python Streamlit Learning")

# warnings
st.warning("Come on time.")

st.write("Enter your username")

password = st.text_input("Enter your password")
if password:
    st.write(f"I got a new password: {password}")
st.session_state["messages"] = "Enter your new password"
def display_messages():
    st.subheader("Chat")
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()


number = st.slider("a number",1,50, key="")
st.session_state['Values'] = "this is a value"
leng = len(st.session_state)
st.write(leng)
st.session_state["agent"] = Agent(os.getenv("OPENAI_API_KEY"))

def read_and_save_file():
    st.session_state["agent"].forget()
    st.session_state["messages"] = []
    st.session_state["user_input"] = ""
    st.session_state["agent"] = Agent(os.getenv("OPENAI_API_KEY"))
    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        with st.session_state["ingestion_spinner"], st.spinner(f"Ingesting {file.name}"):
            st.session_state["agent"].ingest(file_path)
        os.remove(file_path)

read_and_save_file()