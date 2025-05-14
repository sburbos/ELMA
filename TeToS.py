import streamlit as st
import os
from openai import OpenAI

# Initialize the OpenAI client with proper configuration

with st.container():
    st.subheader("TeToS by Elley")
    st.title("Your Free Text-To-Speech Tool")

# Debug: Show loaded secrets (remove after testing)
pages = [ st.Page("EsMapp.py", title="Essay Maker"),
        st.Page("TeToS.py", title="Text To Speech"),]


pg = st.navigation(pages)
pg.run()