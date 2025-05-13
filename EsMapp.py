import streamlit as st
import requests
import os
from openai import OpenAI

# Set up for OpenRouter
os.environ[
    "OPENAI_API_KEY"] = "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"  # From https://openrouter.ai/settings/keys
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

client = OpenAI()
saved_contents = []

st.set_page_config(page_title="EsMa", page_icon=":writing_hand:", layout="wide")
list_essay_type = ["Argumentative", "Persuasive", 'Explanatory', 'Descriptive', "Narrative",
                   'Cause and Effect', "Process Analysis", "Compare/Contrast", "General"]


def ai_assistant(x):
    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[{
            "role": "system",
            "content": """I shall name you EsMa short for Essay Maker. You are a tool helping students to create their essays.
            You (Strictly) only need to write their essays and nothing else."""
        }, {
            "role": "user",
            "content": x
        }]
    )
    result = response.choices[0].message.content
    saved_contents.append(result)
    return result


# Main app interface
with st.container():
    st.subheader("EsMa")
    st.title("Your Free Essay Maker Tool")

    # Get essay type first
    essay_type = st.selectbox("Essay Type", list_essay_type)

    # Get user prompt
    content_prompt = st.text_area("Prompt", "Write your prompt here:", height=100)

    # Generate essay when button is clicked
    if st.button("Generate Essay"):
        if content_prompt and content_prompt != "Write your prompt here:":
            full_prompt = f"Write a {essay_type} essay about: {content_prompt}"
            with st.spinner("Generating your essay..."):
                essay = ai_assistant(full_prompt)
            st.text_area("Generated Essay", essay, height=300)
        else:
            st.warning("Please enter a prompt for your essay")