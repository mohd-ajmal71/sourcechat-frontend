
import streamlit as st
import requests
import os

API_URL = "https://sourcechat-ajmal.onrender.com"


def show():

    st.markdown("""
    <style>

    .source-heading {
        font-size: 38px;
        font-weight: 850;
        background: linear-gradient(100deg, #2563eb, #6366f1, #9333ea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }

    .source-description {
        color: #64748b;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .upload-panel {
        background: linear-gradient(
            120deg,
            rgba(219,234,254,0.85),
            rgba(237,233,254,0.9)
        );
        border: 1px solid rgba(99,102,241,0.2);
        border-radius: 22px;
        padding: 23px;
        margin: 15px 0;
    }

    .upload-heading {
        color: #312e81;
        font-size: 21px;
        font-weight: 750;
    }

    .upload-description {
        color: #64748b;
        font-size: 14px;
        margin-top: 5px;
    }

    .document-panel {
        background: rgba(255,255,255,0.85);
        border: 1px solid #c7d2fe;
        border-radius: 16px;
        padding: 18px;
        margin-top: 15px;
    }

    .chat-heading {
        color: #312e81;
        font-size: 23px;
        font-weight: 750;
        margin-top: 25px;
        margin-bottom: 12px;
    }

    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.85);
        border: 1px dashed #818cf8;
        border-radius: 16px;
        padding: 15px;
    }

    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,0.88);
        border: 1px solid rgba(129,140,248,0.18);
        border-radius: 17px;
        padding: 15px;
        box-shadow: 0 4px 14px rgba(49,46,129,0.04);
    }

    [data-testid="stChatInput"] {
        border-radius: 15px;
    }

    .source-note {
        background: linear-gradient(110deg, #eff6ff, #f5f3ff);
        border-left: 4px solid #6366f1;
        border-radius: 10px;
        padding: 12px 15px;
        color: #3730a3;
        margin-top: 8px;
        font-size: 14px;
    }

    </style>
    """, unsafe_allow_html=True)

    if st.button("← Home", key="sourcechat_home"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown("""
    <div class="source-heading">📚 SourceChat</div>

    <div class="source-description">
        Upload your PDF documents and get intelligent,
        document-based answers with source references.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="upload-panel">
        <div class="upload-heading">📄 Upload Your Documents</div>
        <div class="upload-description">
            Add one or multiple PDF files to start asking questions.
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Choose PDF documents",
        type=["pdf"],
        accept_multiple_files=True,
        key="sourcechat_uploader"
    )

    if uploaded_files:

        st.caption(f"{len(uploaded_files)} PDF file(s) selected.")

        if st.button(
            "⬆️ Upload Documents",
            type="primary",
            width="stretch",
            key="upload_sourcechat"
        ):

            files = []

            for uploaded_file in uploaded_files:
                files.append(
                    (
                        "files",
                        (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf"
                        )
                    )
                )

            try:
                with st.spinner("Processing your documents..."):

                    response = requests.post(
                        f"{API_URL}/upload",
                        params={
                            "session_id": st.session_state.session_id
                        },
                        files=files,
                        timeout=300
                    )

                if response.status_code == 200:

                    data = response.json()

                    st.session_state.documents = data["document_ids"]
                    st.session_state.uploaded = True
                    st.session_state.messages = []

                    st.success("Documents uploaded successfully!")

                else:
                    st.error(f"Upload failed: {response.text}")

            except requests.RequestException as e:
                st.error(f"Upload error: {e}")

            except (KeyError, ValueError) as e:
                st.error(f"Unexpected upload response: {e}")

    if st.session_state.documents:

        st.markdown(f"""
        <div class="document-panel">
            <div style="color:#312e81;font-size:19px;font-weight:750;">
                ✅ Documents Ready
            </div>
            <div style="color:#64748b;font-size:14px;margin-top:5px;">
                {len(st.session_state.documents)} document(s)
                available for question answering.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="chat-heading">
        💬 Ask Questions About Your Documents
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.documents:

        for message in st.session_state.messages:

            with st.chat_message(message["role"]):

                st.markdown(message["content"])

                if message["role"] == "assistant":

                    sources = message.get("sources", [])

                    if sources:
                        st.markdown("**📚 Cited Sources**")

                        unique_sources = list(dict.fromkeys(
                            os.path.basename(source["source"].replace("\\", "/"))
                            for source in sources
                            if source.get("source")
                        ))

                        for filename in unique_sources:
                            st.markdown(
                                f"""
                                <div class="source-note">
                                    📄 <b>{filename}</b>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

        question = st.chat_input(
            "Ask anything about your uploaded PDFs..."
        )

        if question:

            st.session_state.messages.append({
                "role": "user",
                "content": question
            })

            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):

                with st.spinner("Finding relevant information..."):

                    try:
                        response = requests.post(
                            f"{API_URL}/chat",
                            json={
                                "question": question,
                                "session_id": st.session_state.session_id,
                                "document_ids": st.session_state.documents
                            },
                            timeout=180
                        )

                        if response.status_code == 200:

                            data = response.json()

                            answer = data["answer"]
                            sources = data.get("sources", [])

                            st.markdown(answer)

                            if sources:
                                st.markdown("**📚 Cited Sources**")

                                unique_sources = list(dict.fromkeys(
                                    os.path.basename(source["source"].replace("\\", "/"))
                                    for source in sources
                                    if source.get("source")
                                ))

                                for filename in unique_sources:
                                    st.markdown(
                                        f"""
                                        <div class="source-note">
                                            📄 <b>{filename}</b>
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )

                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": answer,
                                "sources": sources
                            })

                        else:
                            st.error(f"Chat failed: {response.text}")

                    except requests.RequestException as e:
                        st.error(f"Chat error: {e}")

                    except (KeyError, ValueError) as e:
                        st.error(f"Unexpected chat response: {e}")

    else:

        st.markdown("""
        <div style="
            background:linear-gradient(120deg,#eff6ff,#f5f3ff);
            border:1px solid #c7d2fe;
            border-radius:18px;
            padding:30px;
            text-align:center;
            margin-top:15px;
        ">
            <div style="font-size:38px;">📖</div>
            <div style="
                color:#312e81;
                font-size:19px;
                font-weight:750;
                margin-top:10px;
            ">
                Your Document Chat Starts Here
            </div>
            <div style="
                color:#64748b;
                font-size:14px;
                margin-top:8px;
            ">
                Upload your PDF documents above to start
                asking questions and receiving cited answers.
            </div>
        </div>
        """, unsafe_allow_html=True)
