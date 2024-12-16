import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Generate Linux and Cybersecurity Lab Procedures")
st.write(
    "Input a topic "
)

topic = st.text_input("Please input a Topic")
distribution = st.text_input("Please input the Linux Distribution")

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
#openai_api_key = st.text_input("OpenAI API Key", type="password")
openai_api_key = st.secrets["openai_api_key"]
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "lab_generated" not in st.session_state:
        st.session_state.lab_generated = False

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a submit button to initiate the chat.
    col1, col2 = st.columns([6, 6])
    if not st.session_state.lab_generated:
        submitted = col1.button("Submit")
        next_lab = False
    else:
        submitted = False
        next_lab = col1.button("Next Lab")

    if submitted or next_lab:
        if next_lab:
            st.session_state.messages = []
            st.session_state.lab_generated = False
        # Create a prompt.
        prompt = "Please generate a detalied lab procedure with detailed commands and options, as well as justification for " + topic + " with respect to " + distribution

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.lab_generated = True

    if st.session_state.lab_generated:
        col2.write("Lab generated successfully!")