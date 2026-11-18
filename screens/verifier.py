
import streamlit as st


def show():

    st.markdown("""
    <style>

    .verifier-heading {
        font-size: 39px;
        font-weight: 850;
        background: linear-gradient(100deg, #0f766e, #0891b2, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }

    .verifier-description {
        color: #64748b;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .verifier-label {
        text-align: center;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .verifier-label span {
        background: linear-gradient(100deg, #ccfbf1, #e0e7ff);
        color: #0f766e;
        padding: 8px 18px;
        border-radius: 30px;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1px;
    }

    .st-key-pdf_card button {
        background: linear-gradient(
            135deg,
            #2563eb,
            #4f46e5,
            #9333ea
        ) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        border-radius: 24px !important;
        min-height: 290px !important;
        width: 100% !important;
        padding: 30px !important;
        white-space: pre-line !important;
        box-shadow: 0 14px 32px rgba(79,70,229,0.22) !important;
        transition: all 0.3s ease !important;
    }

    .st-key-image_card button {
        background: linear-gradient(
            135deg,
            #0f766e,
            #0891b2,
            #6366f1
        ) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        border-radius: 24px !important;
        min-height: 290px !important;
        width: 100% !important;
        padding: 30px !important;
        white-space: pre-line !important;
        box-shadow: 0 14px 32px rgba(8,145,178,0.22) !important;
        transition: all 0.3s ease !important;
    }

    .st-key-pdf_card button:hover,
    .st-key-image_card button:hover {
        transform: translateY(-9px);
        filter: brightness(1.1);
        box-shadow: 0 23px 42px rgba(30,41,59,0.23) !important;
    }

    .st-key-pdf_card button p,
    .st-key-image_card button p {
        color: white !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        line-height: 1.8 !important;
    }

    .notice-panel {
        background: linear-gradient(
            110deg,
            rgba(224,231,255,0.85),
            rgba(204,251,241,0.75)
        );
        border: 1px solid rgba(99,102,241,0.18);
        border-radius: 16px;
        padding: 18px 22px;
        margin-top: 35px;
        color: #475569;
        font-size: 14px;
    }

    </style>
    """, unsafe_allow_html=True)

    if st.button("← Home", key="verifier_home"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown("""
    <div class="verifier-heading">🛡️ Verifier</div>

    <div class="verifier-description">
        Analyze documents and images for potential copyright
        and licensing risks.
    </div>

    <div class="verifier-label">
        <span>✦ CHOOSE VERIFICATION TYPE</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:

        with st.container(key="pdf_card"):

            if st.button(
                "📄\n\nPDF Verification\n\n"
                "Analyze PDF documents for potential copyright "
                "and licensing risks.\n\n"
                "Verify PDF  →",
                key="verify_pdf",
                use_container_width=True
            ):
                st.session_state.page = "pdf_verifier"
                st.rerun()

    with col2:

        with st.container(key="image_card"):

            if st.button(
                "🖼️\n\nImage Verification\n\n"
                "Analyze images for potential copyright "
                "and licensing risks.\n\n"
                "Verify Image  →",
                key="verify_image",
                use_container_width=True
            ):
                st.session_state.page = "image_verifier"
                st.rerun()

    st.markdown("""
    <div class="notice-panel">
        <b>ⓘ About Verification Results</b><br><br>
        Verification results provide potential risk indicators
        and supporting evidence. They are intended to assist
        users and do not constitute a definitive legal determination.
    </div>
    """, unsafe_allow_html=True)
