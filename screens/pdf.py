import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"


def show():

    st.title("📄 Chat with PDF")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "uploaded" not in st.session_state:
        st.session_state.uploaded = False

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
                        files=files,
                    )

                    if response.status_code == 200:
                        st.success("PDF uploaded successfully.")
                        st.session_state.uploaded = True
                    else:
                        st.error(response.text)

                except Exception as e:
                    st.error(e)

    st.divider()

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if message["role"] == "assistant":

                sources = message.get("sources", [])

                if sources:

                    st.markdown("**📚 Sources**")

                    unique_sources = []

                    for source in sources:
                        if source not in unique_sources:
                            unique_sources.append(source)

                    for source in unique_sources:
                        st.markdown(
                            f"- **{source['source']}** (Page {source['page']})"
                        )

    if st.session_state.uploaded:

        question = st.chat_input("Ask a question about your PDF...")

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
                                "question": question
                            }
                        )

                        if response.status_code == 200:

                            data = response.json()

                            answer = data["answer"]
                            sources = data["sources"]

                            st.markdown(answer)

                            if sources:

                                st.markdown("**📚 Sources**")

                                seen = set()

                                for source in sources:
                                    key = (source["source"], source["page"])
                                    if key not in seen:
                                        seen.add(key)
                                        st.markdown(f"- **{source['source']}** (Page {source['page']})")

                            st.session_state.messages.append(
                                {
                                    "role": "assistant",
                                    "content": answer,
                                    "sources": sources,
                                }
                            )

                        else:
                            st.error(response.text)

                    except Exception as e:
                        st.error(e)

    else:
        st.info("Upload a PDF to start chatting.")