import streamlit as st


def apply_custom_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');

        :root {
            --emerald-light: #e6f3f0;
            --emerald-deep: #2d5a4c;
            --amber-light: #fff9e6;
            --amber-deep: #b08a2e;
            --watercolor-bg: linear-gradient(135deg, #e6f3f0 0%, #fff9e6 100%);
        }

        .stApp {
            background: var(--watercolor-bg);
            font-family: 'Outfit', sans-serif;
        }

        h1, h2, h3 {
            font-family: 'Playfair Display', serif;
            color: var(--emerald-deep);
        }

        .stChatMessage {
            background-color: rgba(255, 255, 255, 0.4);
            border-radius: 15px;
            border: 1px solid rgba(45, 90, 76, 0.1);
            backdrop-filter: blur(5px);
            margin-bottom: 1rem;
        }

        .stChatMessage [data-testid="stChatMessageContent"] {
            color: #333;
        }

        .report-container {
            background-color: white;
            padding: 2rem;
            border-radius: 20px;
            border-left: 5px solid var(--amber-deep);
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            margin-top: 2rem;
        }

        .sidebar .sidebar-content {
            background-color: var(--emerald-light);
        }
        
        /* Premium button styling */
        .stButton>button {
            border-radius: 20px;
            border: 1px solid var(--emerald-deep);
            color: var(--emerald-deep);
            background-color: transparent;
            transition: all 0.3s;
        }
        
        .stButton>button:hover {
            background-color: var(--emerald-deep);
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


HEADER_HTML = """
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="font-size: 3.5rem; margin-bottom: 0;">SELENE</h1>
    <p style="font-style: italic; color: #555; font-size: 1.2rem;">Privacy-first Clinical Advocacy Agent</p>
</div>
"""
