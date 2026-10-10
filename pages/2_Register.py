import streamlit as st

st.set_page_config(
    page_title="Register | ScholarShield",
    page_icon="🛡️",
    layout="wide"
)

from auth.register import show_register_page

show_register_page()