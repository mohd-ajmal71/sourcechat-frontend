
import streamlit as st
from pathlib import Path


def show():
    st.markdown("""
    <style>

    .stApp {
        background:
            radial-gradient(ellipse at 5% 10%, rgba(129, 140, 248, 0.25), transparent 35%),
            radial-gradient(ellipse at 95% 15%, rgba(192, 132, 252, 0.24), transparent 35%),
            radial-gradient(ellipse at 50% 95%, rgba(45, 212, 191, 0.16), transparent 40%),
            linear-gradient(135deg, #f8faff, #f1f0ff, #effbff);
        background-attachment: fixed;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 3.5rem;
        padding-bottom: 2rem;
    }

    .hero-label {
        text-align: center;
        margin-bottom: 15px;
    }

    .hero-label span {
        display: inline-block;
        padding: 8px 19px;
        border-radius: 30px;
        background: linear-gradient(100deg, #e0e7ff, #f3e8ff);
        color: #5b21b6;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1.5px;
    }

    .hero-title {
        text-align: center;
        font-size: 49px;
        font-weight: 850;
        letter-spacing: -1.5px;
        line-height: 1.2;
        background: linear-gradient(100deg, #2563eb, #7c3aed, #0f9fba);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 14px;
    }

    .hero-subtitle {
        text-align: center;
        color: #64748b;
        font-size: 17px;
        font-weight: 450;
        margin-bottom: 12px;
    }

    /* Hero image spacing */

    .hero-image-container {
        margin-top: 15px;
        margin-bottom: 35px;
    }

    /* Feature cards */

    .st-key-source_card,
    .st-key-verifier_card {
        border-radius: 25px;
        overflow: hidden;
    }

    .st-key-source_card button {
        background: linear-gradient(
            135deg,
            #1d4ed8 0%,
            #4f46e5 48%,
            #9333ea 100%
        ) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        border-radius: 25px !important;
        min-height: 310px !important;
        width: 100% !important;
        padding: 35px 28px !important;
        box-shadow: 0 15px 35px rgba(79, 70, 229, 0.25) !important;
        transition: all 0.3s ease !important;
        white-space: pre-line !important;
    }

    .st-key-verifier_card button {
        background: linear-gradient(
            135deg,
            #0f766e 0%,
            #0891b2 48%,
            #4f46e5 100%
        ) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        border-radius: 25px !important;
        min-height: 310px !important;
        width: 100% !important;
        padding: 35px 28px !important;
        box-shadow: 0 15px 35px rgba(8, 145, 178, 0.25) !important;
        transition: all 0.3s ease !important;
        white-space: pre-line !important;
    }

    .st-key-source_card button:hover,
    .st-key-verifier_card button:hover {
        transform: translateY(-9px);
        filter: brightness(1.10);
        box-shadow: 0 23px 45px rgba(30, 41, 59, 0.23) !important;
        border: 1px solid rgba(255,255,255,0.5) !important;
    }

    .st-key-source_card button p,
    .st-key-verifier_card button p {
        font-size: 21px !important;
        font-weight: 700 !important;
        line-height: 1.8 !important;
        color: white !important;
    }

    /* Footer */

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 13px;
        margin-top: 75px;
        padding-bottom: 15px;
    }

    @media (max-width: 768px) {
        .hero-title {
            font-size: 34px;
        }

        .hero-subtitle {
            font-size: 14px;
        }

        .st-key-source_card button,
        .st-key-verifier_card button {
            min-height: 240px !important;
        }
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-label">
        <span>✦ AI-POWERED DOCUMENT WORKSPACE</span>
    </div>

    <div class="hero-title">
        SourceChat & Verifier
    </div>

    <div class="hero-subtitle">
        Intelligent Document Question Answering & Copyright Risk Verification
    </div>
    """, unsafe_allow_html=True)

    # Hero image

    image_path = Path(__file__).resolve().parent.parent / "assets" / "home_hero.jpeg"

    if image_path.exists():
        image_col1, image_col2, image_col3 = st.columns([1, 4, 1])

        with image_col2:
            st.image(
                str(image_path),
                use_container_width=True
            )
    else:
        st.warning("Hero image not found. Please add home_hero.png inside the assets folder.")

    st.markdown('<div class="hero-image-container"></div>', unsafe_allow_html=True)

    # Feature cards

    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container(key="source_card"):
            if st.button(
                "📚\n\nSourceChat\n\nChat with your PDF documents\n\nExplore SourceChat  →",
                key="open_sourcechat",
                use_container_width=True
            ):
                st.session_state.page = "sourcechat"
                st.rerun()

    with col2:
        with st.container(key="verifier_card"):
            if st.button(
                "🛡️\n\nVerifier\n\nAnalyze copyright and licensing risks\n\nExplore Verifier  →",
                key="open_verifier",
                use_container_width=True
            ):
                st.session_state.page = "verifier"
                st.rerun()

    st.markdown("""
    <div class="footer">
        © 2026 SourceChat & Verifier | Powered by AI
    </div>
    """, unsafe_allow_html=True)
