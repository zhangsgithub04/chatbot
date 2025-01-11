import streamlit as st
import google.generativeai as ggi
from transformers import pipeline
from huggingface_hub import HfApi

# Configure API keys
fetchpeed_api_key = st.secrets["gemini_api_key"]
hf_api_key = st.secrets["hf_api_key"]

# Configure Hugging Face API
hf_api = HfApi(token=hf_api_key)

# Configure Google Generative AI
ggi.configure(api_key=fetchpeed_api_key)

# Initialize model and chat
model = ggi.GenerativeModel("gemini-pro")
chat = model.start_chat()

# Initialize zero-shot classifier
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def LLM_Response(question):
    """Send a message to the chat and return the response."""
    try:
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        return str(e)

def validate_input(user_input):
    """Validate user input using zero-shot classification."""
    candidate_labels = ["Linux command", "Computer science", "Technology"]
    result = classifier(user_input, candidate_labels)
    if result["labels"][0] == "Linux command":
        return True
    return False

st.title("Chat Application using Gemini Pro")

user_quest = st.text_input("Ask a question about Linux commands:")
btn = st.button("Ask")

if btn and user_quest:
    if validate_input(user_quest):
        result = LLM_Response(user_quest)
        st.subheader("Response:")
        for word in result:
            st.text(word.text)
    else:
        st.error("Please ask a question related to Linux commands.")
