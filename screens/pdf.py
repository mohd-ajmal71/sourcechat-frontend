import streamlit as st
import requests
import uuid

API_URL = "https://sourcechat-ajmal.onrender.com"


def show():

    st.title("📄 Chat with PDF")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "uploaded" not in st.session_state:
        st.session_state.uploaded = False

    if "document_id" not in st.session_state:
        st.session_state.document_id = None

    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_file:

        if st.button("Upload PDF"):

            files = [
                (
                    "files",
                    (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/pdf",
                    ),
                )
            ]

            with st.spinner("Processing PDF..."):

                try:

                    response = requests.post(
                        f"{API_URL}/upload",
                        params={
                            "session_id": st.session_state.session_id
                        },
                        files=files,
                    )

                    if response.status_code == 200:

                        data = response.json()

                        st.session_state.document_id = data[
                            "document_id"
                        ]

                        st.session_state.uploaded = True
                        st.session_state.messages = []

                        st.success(
                            "PDF uploaded successfully."
                        )

                    else:

                        st.error(
                            f"Upload failed: {response.text}"
                        )

                except Exception as e:

                    st.error(
                        f"Upload error: {e}"
                    )

    st.divider()

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if message["role"] == "assistant":

                sources = message.get("sources", [])

                if sources:

                    st.markdown("**📚 Sources**")

                    seen = set()

                    for source in sources:

                        key = (
                            source["source"],
                            source["page"]
                        )

                        if key not in seen:

                            seen.add(key)

                            st.markdown(
                                f"- **{source['source']}** "
                                f"(Page {source['page']})"
                            )

    if (
        st.session_state.uploaded
        and st.session_state.document_id
    ):

        question = st.chat_input(
            "Ask a question about your PDF..."
        )

        if question:

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question,
                }
            )

            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):

                with st.spinner("Thinking..."):

                    try:

                        response = requests.post(
                            f"{API_URL}/chat",
                            json={
                                "question": question,
                                "session_id": st.session_state.session_id,
                                "document_id": st.session_state.document_id,
                            }
                        )

                        if response.status_code == 200:

                            data = response.json()

                            answer = data["answer"]
                            sources = data.get("sources", [])

                            st.markdown(answer)

                            if sources:

                                st.markdown("**📚 Sources**")

                                seen = set()

                                for source in sources:

                                    key = (
                                        source["source"],
                                        source["page"]
                                    )

                                    if key not in seen:

                                        seen.add(key)

                                        st.markdown(
                                            f"- **{source['source']}** "
                                            f"(Page {source['page']})"
                                        )

                            st.session_state.messages.append(
                                {
                                    "role": "assistant",
                                    "content": answer,
                                    "sources": sources,
                                }
                            )

                        else:

                            st.error(
                                f"Chat failed: {response.text}"
                            )

                    except Exception as e:

                        st.error(
                            f"Chat error: {e}"
                        )

    else:

        st.info(
            "Upload a PDF to start chatting."
        )