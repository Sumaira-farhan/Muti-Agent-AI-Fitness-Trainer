# =========================
# AI FITNESS TRAINER STREAMLIT APP
# A Project by Ms. Sumaira Farhan
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

st.markdown(
    "### 👩‍🏫 A Project by Ms. Sumaira Farhan",
    unsafe_allow_html=True
)

st.write("Your personal AI gym coach with memory 💪")

# =========================
# SIDEBAR
# =========================
st.sidebar.header("Settings")

API_KEY = st.sidebar.text_input("Enter Groq API Key", type="password")

st.sidebar.markdown("---")
st.sidebar.markdown("👩‍🏫 Project by Ms. Sumaira Farhan")

if not API_KEY:
    st.warning("Please enter your Groq API Key to continue.")
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
# MODELS
# =========================
MODELS = [
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant"
]

def call_llm(prompt):
    for model in MODELS:
        try:
            res = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a world-class personal fitness trainer. Motivating, friendly, and practical."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7
            )
            return res.choices[0].message.content
        except:
            continue

    return "⚠️ AI model error. Please try again."

# =========================
# AGENT FUNCTION
# =========================
def agent(user_input):

    extract_memory(user_input)

    prompt = f"""
You are a personal fitness coach.

User Profile:
{get_context()}

User Message:
{user_input}

Rules:
- Be motivating like a real trainer
- Give workout + diet advice
- Use memory when needed
- Ask follow-up questions
"""

    reply = call_llm(prompt)

    memory["chat_history"].append({
        "time": str(datetime.now()),
        "user": user_input,
        "bot": reply
    })

    save_memory()

    return reply

# =========================
# CHAT UI
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Talk to your fitness coach...")

if user_input:

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    reply = agent(user_input)

    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.write(reply)
