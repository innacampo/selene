import streamlit as st
import json
from engine import SeleneBrain
import time

# --- Page Config ---
st.set_page_config(
    page_title="SELENE - Menopause Research Partner",
    page_icon="🌙",
    layout="centered"
)

# --- LUCIA Palette Styling ---
st.markdown("""
<style>
    /* Main container and background */
    .stApp {
        background-color: #F7D76D;
        color: #5D3A1A;
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #E65100;
        color: white;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Headers */
    h1, h2, h3 {
        color: #5D3A1A !important;
        font-weight: 700;
    }

    /* Buttons */
    .stButton>button {
        background-color: #FF8C00;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: transform 0.2s, background-color 0.2s;
    }

    .stButton>button:hover {
        background-color: #E65100;
        transform: scale(1.02);
        color: white;
    }

    /* Text areas */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.8);
        border: 2px solid #FF8C00;
        border-radius: 8px;
        color: #5D3A1A;
    }

    /* JSON display */
    .stJson {
        background-color: rgba(255, 255, 255, 0.5);
        border-radius: 8px;
        padding: 10px;
    }
    
    /* Privacy Indicator */
    .privacy-badge {
        background-color: #4CAF50;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if "brain" not in st.session_state:
    st.session_state.brain = SeleneBrain()
    # Note: We don't load the model immediately to avoid blocking UI
    st.session_state.model_loaded = False

# --- Sidebar ---
with st.sidebar:
    st.title("🌙 SELENE")
    st.markdown("### Menopause Research Partner")
    st.write("---")
    st.markdown('<div class="privacy-badge">🔒 Local Mode: Active</div>', unsafe_allow_html=True)
    st.write("")
    st.info("Your data stays local and private.")
    
    if st.button("Load Engine"):
        with st.spinner("Initializing Selene Brain..."):
            st.session_state.brain.load_model()
            st.session_state.model_loaded = True
        st.success("Engine Ready!")

# --- Main UI ---
st.title("How are you feeling today?")
st.write("Share your symptoms and I'll help you structure and log them privately.")

user_input = st.text_area("Daily Symptom Check-in", placeholder="e.g., I feel dizzy and hot tonight...", height=150)

if st.button("Log to Journal"):
    if not st.session_state.model_loaded:
        st.warning("⚠️ Please 'Load Engine' in the sidebar first.")
    elif not user_input.strip():
        st.error("Please enter some text first.")
    else:
        with st.spinner("SELENE is thinking..."):
            # Process the symptom
            structured_data = st.session_state.brain.process_symptom(user_input)
            
            if "error" not in structured_data:
                # Save to local storage
                success = st.session_state.brain.save_to_journal(structured_data)
                
                if success:
                    st.success("Symptom logged successfully to your private journal!")
                    st.markdown("### Structured Findings")
                    st.json(structured_data)
                else:
                    st.error("Failed to save to journal.")
            else:
                st.error("Processing failed.")
                st.write(structured_data.get("error"))
                if "raw_response" in structured_data:
                    with st.expander("Show raw output"):
                        st.write(structured_data["raw_response"])

# --- Journal Preview ---
st.write("---")
if st.checkbox("Show Journal History"):
    try:
        with open("data/journal.json", "r") as f:
            history = json.load(f)
        if history:
            st.write(f"Total entries: {len(history)}")
            st.table(history)
        else:
            st.write("Journal is empty.")
    except Exception as e:
        st.write("Could not load journal history.")
