import streamlit as st
import os
from openai import OpenAI

# Initialize the OpenAI client with proper configuration
client = OpenAI(
    api_key=st.secrets["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"],  # Will use environment variable if available
    base_url=st.secrets["https://openrouter.ai/api/v1"]
)

st.set_page_config(
    page_title="EsMa",
    page_icon=":writing_hand:",
    layout="wide"
)

list_essay_type = [
    "Argumentative", "Persuasive", 'Explanatory', 'Descriptive',
    "Narrative", 'Cause and Effect', "Process Analysis",
    "Compare/Contrast", "General"
]


def ai_assistant(prompt):
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[
                {
                    "role": "system",
                    "content": """You are EsMa (Essay Maker). Strictly only write the requested essay content."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=2000  # Added to prevent timeouts
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Failed to generate essay: {str(e)}")
        return None


# Main app interface
def main():
    st.subheader("EsMa")
    st.title("Your Free Essay Maker Tool")

    essay_type = st.selectbox("Essay Type", list_essay_type)
    content_prompt = st.text_area("Prompt", "Write your prompt here:", height=100)

    if st.button("Generate Essay"):
        if content_prompt.strip() in ("", "Write your prompt here:"):
            st.warning("Please enter a valid prompt")
        else:
            with st.spinner("Generating your essay..."):
                full_prompt = f"Write a comprehensive {essay_type} essay about: {content_prompt}"
                essay = ai_assistant(full_prompt)
                if essay:
                    st.text_area("Generated Essay", value=essay, height=300)


if __name__ == "__main__":
    main()