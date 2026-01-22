import streamlit as st
from engine import MedGemmaEngine
import time

st.set_page_config(page_title="MedGemma Chat", page_icon="🩺", layout="centered")

# --- Styling ---
st.markdown("""
<style>
    .stApp {
        background-color: #f0f2f6;
    }
    .stChatInput {
        position: fixed;
        bottom: 3rem;
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

# --- State ---
if "engine" not in st.session_state:
    st.session_state.engine = MedGemmaEngine()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "model_loaded" not in st.session_state:
    st.session_state.model_loaded = False

# --- Sidebar ---
with st.sidebar:
    st.title("🩺 MedGemma")
    st.write("Local Medical AI Assistant")
    
    # Model Path Config
    model_path = st.text_input("Model Path", value="google/medgemma-1.5-4b-it", help="Path to your local model folder or HF ID")
    if model_path != st.session_state.engine.model_path:
        st.session_state.engine.model_path = model_path
        st.session_state.model_loaded = False # Reset if path changed

    # HF Token Input
    hf_token = st.text_input("Hugging Face Token", type="password", help="Required for gated models like MedGemma if not logged in via CLI.")

    if not st.session_state.model_loaded:
        if st.button("Load Model", key="load_btn"):
            with st.spinner(f"Loading {model_path}... (this may take time)"):
                success, msg = st.session_state.engine.load_model(token=hf_token if hf_token else None)
                if success:
                    st.session_state.model_loaded = True
                    st.success(msg)
                else:
                    st.error(msg)
    else:
        st.success("Model Active ✅")
        if st.button("Unload / Reset"):
            st.session_state.model_loaded = False
            st.session_state.engine.model = None
            st.rerun()

    st.write("---")
    if st.button("Hard Reset / Force Reload"):
        st.session_state.clear()
        st.rerun()

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- Main UI ---
st.title("Medical Assistant")

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Ask a medical question..."):
    # Check if model is loaded
    if not st.session_state.model_loaded:
        st.error("Please load the model in the sidebar first.")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate Entry
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.engine.generate_response(st.session_state.messages)
                st.markdown(response)
        
        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": response})
