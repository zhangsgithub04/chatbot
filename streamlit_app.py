import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Generate Linux and Cybersecurity Lab Procedures")
st.write(
    "Input a topic "
)

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
    if "current_topic" not in st.session_state:
        st.session_state.current_topic = ""
    if "current_distribution" not in st.session_state:
        st.session_state.current_distribution = ""
    if "lab_outputs" not in st.session_state:
        st.session_state.lab_outputs = []

    # Create a sidebar to display lab outputs
    st.sidebar.header("Lab Outputs")
    for i, output in enumerate(st.session_state.lab_outputs):
        st.sidebar.subheader(f"Lab {i+1}")
        st.sidebar.write(output)

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a submit button to initiate the chat.
    col1, col2 = st.columns([6, 6])
    if not st.session_state.lab_generated:
        topic = st.text_input("Please input a Topic")
        distribution = st.text_input("Please input the Linux Distribution")
        submitted = col1.button("Submit")
        next_lab = False
    else:
        topic = st.text_input("Please input a Topic", value=st.session_state.current_topic, disabled=True)
        distribution = st.text_input("Please input the Linux Distribution", value=st.session_state.current_distribution, disabled=True)
        submitted = False
        next_lab = col1