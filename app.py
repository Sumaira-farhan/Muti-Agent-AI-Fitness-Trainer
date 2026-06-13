# =========================
# AI FITNESS TRAINER STREAMLIT APP
# (Converted from your agent code)
# =========================

import streamlit as st
import json
import os
from datetime import datetime
from groq import Groq

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AI Fitness Trainer", page_icon="🏋️")

st.title("🏋️ AI Fitness Trainer")
st.write("Your personal AI gym coach with memory 💪")

# =========================
# API KEY INPUT
# =========================
API_KEY = st.sidebar.text_input("Enter Groq API Key", type="password")

if not API_KEY:
    st.warning("Please enter your Groq API Key in sidebar to start")
    st.stop()

client = Groq(api_key=API_KEY)

# =========================
# MEMORY FILE
# =========================
MEMORY_FILE = "trainer_memory.json"

if os.path.exists(MEMORY_FILE):
    memory = json.load(open(MEMORY_FILE))
else:
    memory = {
        "profile": {},
        "chat_history": []
    }

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

# =========================
# MEMORY FUNCTIONS
# =========================
def get_context():
    return json.dumps(memory["profile"], indent=2)

def extract_memory(user_input):
    text = user_input.lower()

    if "my name is" in text:
        memory["profile"]["name"] = user_input.split("is")[-1].strip()

    if "my weight is" in text:
        memory["profile"]["weight"] = user_input.split("is")[-1].strip()

    if "my goal is" in text:
        memory["profile"]["goal"] = user_input.split("is")[-1].strip()

    if "my height is" in text:
        memory["profile"]["height"] = user_input.split("is")[-1].strip()

    save_memory()

# =========================
# PROMPT BUILDER
# =========================
def build_prompt(user_input):
    return f"""
You are a WORLD CLASS PERSONAL FITNESS TRAINER.

Personality:
- Friendly
- Motivational
- Practical
- Slightly strict like a real coach

User Profile:
{get_context()}

Rules:
- Use memory when relevant
- Give workout, diet, lifestyle advice
- Ask follow-up questions
- Keep responses conversational

User message:
{user_input}
"""

# =========================
# AGENT FUNCTION
# =========================
def agent(user_input):

    extract_memory(user_input)

    prompt = build_prompt(user_input)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a professional fitness coach."},
            {"role": "user", "content": prompt}
        ]
    )

    reply = response.choices[0].message.content

    memory["chat_history"].append({
        "time": str(datetime.now()),
        "user": user_input,
        "bot": reply
    })

    save_memory()

    return reply

# =========================
# CHAT HISTORY UI
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# =========================
# USER INPUT
# =========================
user_input = st.chat_input("Talk to your fitness coach...")

if user_input:

    # user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    # agent response
    reply = agent(user_input)

    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.write(reply)
