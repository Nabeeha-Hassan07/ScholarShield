import streamlit as st

st.set_page_config(
    page_title="Login | ScholarShield",
    page_icon="🛡️",
    layout="wide"
)

from auth.login import show_login_page

show_login_page()