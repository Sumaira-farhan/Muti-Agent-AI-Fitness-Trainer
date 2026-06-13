
import streamlit as st
from transformers import pipeline

# Load Models

# BERT-based sentiment model
senti_model = pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
)

# GPT text generation model
generator = pipeline(
    "text-generation",
    model="distilgpt2"
)

# Streamlit UI

st.title("BERT and GPT Models")
st.write(
    "This app performs Sentiment Analysis using BERT "
    "and Text Generation using GPT."
)

menu = st.sidebar.selectbox(
    "Choose a model",
    ["Sentiment Analysis", "Text Generation"]
)

# Sentiment Analysis

if menu == "Sentiment Analysis":

    st.header("BERT Sentiment Analysis")

    text = st.text_area("Enter a sentence:")

    if st.button("Analyze Sentiment"):

        if text.strip() != "":

            result = senti_model(text)[0]

            st.success(f"Prediction: {result['label']}")
            st.write(f"Confidence Score: {round(result['score'], 2)}")

        else:
            st.warning("Please enter some text.")

# Text Generation

elif menu == "Text Generation":

    st.header("GPT Text Generation")

    prompt = st.text_area("Enter a prompt:")

    if st.button("Generate Text"):

        if prompt.strip() != "":

            output = generator(
                            prompt, max_new_tokens=60, do_sample=True, temperature=0.7, top_p=0.9,
                            repetition_penalty=1.2, no_repeat_ngram_size=3
                            )


            st.write(output[0]["generated_text"])

        else:
            st.warning("Please enter a prompt.")
