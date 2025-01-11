
import streamlit as st

import google.generativeai as ggi



fetcheed_api_key = st.secrets["gemini_api_key")
ggi.configure(api_key = fetcheed_api_key)

model = ggi.GenerativeModel("gemini-pro") 
chat = model.start_chat()

def LLM_Response(question):
    response = chat.send_message(question,stream=True)
    return response

st.title("Chat Application using Gemini Pro")

user_quest = st.text_input("Ask a question:")
btn = st.button("Ask")

if btn and user_quest:
    result = LLM_Response(user_quest)
    st.subheader("Response : ")
    for word in result:
        st.text(word.text)
