import streamlit as st
import requests

API_URL = "https://sourcechat-ajmal.onrender.com"


def show():

    st.title("📄 Chat with PDF")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "uploaded" not in st.session_state:
        st.session_state.uploaded = False

    if "documents" not in st.session_state:
        st.session_state.documents = []

    uploaded_files = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:

        if st.button("Upload PDF"):

            files = []

            for uploaded_file in uploaded_files:

                files.append(
                    (
                        "files",
                        (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf",
                        ),
                    )
                )

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

                        st.session_state.documents = data["document_ids"]

                        st.session_state.uploaded = True
                        st.session_state.messages = []

                        st.success(
                            "PDFs uploaded successfully."
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

                    for source in sources:

                        st.markdown(
                            f"- **{source['source']}** "
                            f"(Page {source['page']})"
                        )

    if (
        st.session_state.uploaded
        and st.session_state.documents
    ):

        question = st.chat_input(
            "Ask a question about your PDFs..."
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
                                "document_ids": st.session_state.documents,
                            }
                        )

                        if response.status_code == 200:

                            data = response.json()

                            answer = data["answer"]
                            sources = data.get("sources", [])

                            st.markdown(answer)

                            if sources:

                                st.markdown("**📚 Sources**")

                                for source in sources:

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
            "Upload PDFs to start chatting."
        )