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
st.write("Secrets keys:", list(st.secrets.keys()))

# Initialize client with multiple fallback options
st.write("All secrets:", st.secrets)

try:
    # Access nested secrets
    api_key = st.secrets.openrouter.OPENAI_API_KEY
    base_url = st.secrets.openrouter.OPENAI_BASE_URL

    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    # Test connection
    client.models.list()

except AttributeError as e:
    st.error(f"""
    Secret configuration error: {str(e)}
    Current secret structure: {dict(st.secrets)}
    Required structure:
    ```
    [openrouter]
    OPENAI_API_KEY = "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"
    OPENAI_BASE_URL = "https://openrouter.ai/api/v1"
    ```
    """)
    st.stop()
except Exception as d:
    st.error(f"API connection failed: {str(d)}")
    st.stop()

# Rest of your app...



list_essay_type = [
    "Argumentative", "Persuasive", 'Explanatory', 'Descriptive',
    "Narrative", 'Cause and Effect', "Process Analysis",
    "Compare/Contrast", "General"
]


def ai_assistant(prompt):
    try:
        response = client.chat.completions.create(
            model="nousresearch/deephermes-3-mistral-24b-preview:free",
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
    except Exception as det:
        st.error(f"Failed to generate essay: {str(det)}")
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