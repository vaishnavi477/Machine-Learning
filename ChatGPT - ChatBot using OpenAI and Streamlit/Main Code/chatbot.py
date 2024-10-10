import streamlit as st   # type: ignore
import openai, os
from dotenv import load_dotenv

# Load environment variables for OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # Set the API key

# Title of the chatbot
st.title("My GPT-4o-mini Chatbot 🤖")

# CSS for full-page shaded blue gradient background
st.markdown(
    """
    <style>
    /* Apply the gradient to the whole page */
    html, body, .stApp {
        height: 100%;
        background: linear-gradient(135deg, #004e92, #000428); /* Shaded blue gradient */
        color: white; /* Text color for readability */
        /* Footer style */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize messages in the session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages
for message in st.session_state["messages"]:
    with st.text(message["role"]):
        st.markdown(message["content"])

# Handle user input and OpenAI response
if user_prompt := st.text_input("How can I help you?"):
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Display user message
    with st.text("user"):
        st.markdown(user_prompt)

    # Assistant response
    with st.text("assistant"):
        chatbot_msg = st.empty()
        full_response = ""
        stream = openai.ChatCompletion.create( # type: ignore
            model="gpt-4o-mini",
            messages=[
                {"role": msg["role"], "content": msg["content"]}
                for msg in st.session_state["messages"]
            ],
            temperature=0,
            stream=True,
        )

        # Stream the response
        for chunk in stream:
            token = chunk.choices[0].delta.get("content")
            if token is not None:
                full_response = full_response + token
                chatbot_msg.markdown(full_response)

        chatbot_msg.markdown(full_response)

    # Store assistant's response in session
    st.session_state.messages.append({"role": "assistant", "content": full_response})
