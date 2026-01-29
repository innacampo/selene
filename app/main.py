import sys
from pathlib import Path
import uuid
import asyncio

# Setup path before any local imports
root_path = str(Path(__file__).parent.parent)
if root_path not in sys.path:
    sys.path.append(root_path)

import streamlit as st
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types
from main_agent.agent import root_agent
from styles import apply_custom_styles, HEADER_HTML

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="SELENE | Clinical Advocacy Agent", page_icon="🌙", layout="wide"
)

# Apply custom styling
apply_custom_styles()

# Static initialization
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_service" not in st.session_state:
    st.session_state.session_service = InMemorySessionService()

if "final_report" not in st.session_state:
    st.session_state.final_report = None


async def run_agent(query):
    # Ensure session service is ready
    if "session_service" not in st.session_state:
        st.session_state.session_service = InMemorySessionService()

    session_service = st.session_state.session_service
    app_name = "agents"  # Align with working tests
    user_id = "test_user"  # Align with working tests
    session_id = st.session_state.session_id

    # Ensure session exists in the service
    try:
        await session_service.create_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )
    except Exception:
        # If it fails, it usually means it already exists in InMemorySessionService
        pass

    runner = Runner(
        agent=root_agent,
        app_name=app_name,
        session_service=session_service,
    )

    response_text = ""
    try:
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=genai_types.Content(
                role="user", parts=[genai_types.Part.from_text(text=query)]
            ),
        ):
            if event.is_final_response() and event.content and event.content.parts:
                response_text = event.content.parts[0].text
    except Exception as e:
        response_text = f"Error during agent execution: {str(e)}"
        import traceback

        traceback.print_exc()

    return response_text


# --- Main UI ---

st.markdown(HEADER_HTML, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("About SELENE")
    st.info(
        "SELENE is a multiagent architecture designed to help patients navigate complex medical interactions. "
        "It analyzes narratives to identify symptoms and potential clinical bias."
    )

    if st.button("Reset Conversation"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.session_state.final_report = None
        st.rerun()

# Chat Area
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Describe your clinical experience or symptoms..."):
    # Add user message to UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)

    # Run agent
    with st.chat_message("assistant"):
        with st.spinner("Analyzing narrative..."):
            # Using asyncio.run for cleaner execution if not in a running loop
            try:
                # Check if we are already in an event loop
                try:
                    loop = asyncio.get_running_loop()
                    response = loop.run_until_complete(run_agent(prompt))
                except RuntimeError:
                    response = asyncio.run(run_agent(prompt))
            except Exception as e:
                response = f"An unexpected error occurred: {str(e)}"

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.final_report = response

# Final Report Display (if available)
if st.session_state.final_report:
    st.write("---")
    with st.expander("📄 View Latest Advocacy Report", expanded=True):
        st.markdown(
            f'<div class="report-container">{st.session_state.final_report}</div>',
            unsafe_allow_html=True,
        )
