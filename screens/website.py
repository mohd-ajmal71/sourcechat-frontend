import streamlit as st


def show():

    if st.button("⬅ Home"):
        st.session_state.page = "home"
        st.rerun()

    st.title("🌐 Chat with Website")

    st.write("Website chat page")