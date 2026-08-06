import streamlit as st

from screens.home import show as home_page
from screens.pdf import show as pdf_page
from screens.youtube import show as youtube_page
from screens.website import show as website_page
from screens.settings import show as settings_page
from screens.about import show as about_page


st.set_page_config(
    page_title="SourceChat",
    page_icon="📄",
    layout="wide"
)


# Hide default Streamlit sidebar
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        display:none;
    }

    [data-testid="collapsedControl"] {
        display:none;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# First page when app starts
if "page" not in st.session_state:
    st.session_state.page = "home"


# Router

if st.session_state.page == "home":

    home_page()


elif st.session_state.page == "pdf":

    pdf_page()


elif st.session_state.page == "youtube":

    youtube_page()


elif st.session_state.page == "website":

    website_page()


elif st.session_state.page == "settings":

    settings_page()


elif st.session_state.page == "about":

    about_page()