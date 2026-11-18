
import streamlit as st
import uuid

from screens.home import show as home_page
from screens.sourcechat import show as sourcechat_page
from screens.verifier import show as verifier_page
from screens.pdf_verifier import show as pdf_verifier_page
from screens.image_verifier import show as image_verifier_page

st.set_page_config(
    page_title="SourceChat & Verifier",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
[data-testid="stSidebar"],
[data-testid="collapsedControl"],
#MainMenu,
footer {
    display: none !important;
}

.stApp {
    background:
        radial-gradient(ellipse at 5% 5%, rgba(191, 219, 254, 0.65), transparent 35%),
        radial-gradient(ellipse at 95% 10%, rgba(221, 214, 254, 0.65), transparent 35%),
        radial-gradient(ellipse at 50% 100%, rgba(204, 251, 241, 0.45), transparent 40%),
        linear-gradient(135deg, #f8faff 0%, #f4f3ff 50%, #f0fdfa 100%);
    background-attachment: fixed;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* General buttons */
.stButton > button {
    width: 100%;
    min-height: 46px;
    border: none;
    border-radius: 12px;
    font-weight: 650;
    transition: all 0.25s ease;
    background: linear-gradient(110deg, #4f46e5, #7c3aed);
    color: white;
    box-shadow: 0 5px 15px rgba(79, 70, 229, 0.16);
}

.stButton > button:hover {
    transform: translateY(-2px);
    color: white;
    border: none;
    box-shadow: 0 9px 22px rgba(79, 70, 229, 0.25);
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(255, 255, 255, 0.78);
    border: 1px dashed #818cf8;
    border-radius: 16px;
    padding: 16px;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: rgba(255, 255, 255, 0.82);
    border: 1px solid rgba(148, 163, 184, 0.18);
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 4px 14px rgba(30, 41, 59, 0.04);
}

/* Text inputs */
.stTextInput input,
.stTextArea textarea {
    border-radius: 12px;
    border: 1px solid #c7d2fe;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #6366f1;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.12);
}

/* Select boxes */
[data-testid="stSelectbox"] > div > div {
    border-radius: 12px;
}

/* Dividers */
hr {
    border-color: rgba(148, 163, 184, 0.25);
}

/* Headings */
h1, h2, h3 {
    color: #1e1b4b;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "page" not in st.session_state:
    st.session_state.page = "home"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "documents" not in st.session_state:
    st.session_state.documents = []

if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

if st.session_state.page == "home":
    home_page()

elif st.session_state.page == "sourcechat":
    sourcechat_page()

elif st.session_state.page == "verifier":
    verifier_page()

elif st.session_state.page == "pdf_verifier":
    pdf_verifier_page()

elif st.session_state.page == "image_verifier":
    image_verifier_page()

else:
    st.session_state.page = "home"
    st.rerun()
