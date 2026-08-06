import streamlit as st

def show():

    
    st.image("assets/home_banner.png", use_container_width=True)
    st.title("📄 SourceChat")

    st.write("Welcome to SourceChat")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📄 Chat with PDF", use_container_width=True):
            st.session_state.page = "pdf"
            st.rerun()

    with col2:
        if st.button("🎥 Chat with YouTube", use_container_width=True):
            st.session_state.page = "youtube"
            st.rerun()

    col3, col4 = st.columns(2)

    with col3:
        if st.button("🌐 Chat with Website", use_container_width=True):
            st.session_state.page = "website"
            st.rerun()

    with col4:
        if st.button("⚙️ Settings", use_container_width=True):
            st.session_state.page = "settings"
            st.rerun()

    st.write("")

    left, center, right = st.columns([4, 2, 4])
    with center:
        if st.button("ℹ️ About",use_container_width=True):
            st.session_state.page = "about"
            st.rerun()