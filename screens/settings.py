import streamlit as st


def show():

    if st.button("⬅ Home"):
        st.session_state.page = "home"
        st.rerun()

    st.title("⚙️ Settings")