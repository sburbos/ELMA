import streamlit as st
import os
from openai import OpenAI

# Initialize the OpenAI client with proper configuration

st.set_page_config(
    page_title="EsMa",
    page_icon=":writing_hand:",
    layout="wide"
)
# Debug: Show loaded secrets (remove after testing)
pages = [ st.Page("EsMapp.py", title="Essay Maker"),
        st.Page("TeToS.py", title="Text To Speech"),]


def page_2():
    st.title('Text to Speech')

pg = st.navigation(pages)
pg.run()