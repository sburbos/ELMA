import streamlit as st
import os
from openai import OpenAI

# Initialize the OpenAI client with proper configuration

# Debug: Show loaded secrets (remove after testing)
st.write("Secrets keys:", list(st.secrets.keys()))

# Initialize client with multiple fallback options
try:
    api_key = (
            st.secrets.get("OPENAI_API_KEY") or  # Streamlit Cloud
            os.environ.get("OPENAI_API_KEY") or  # Environment variable
            "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"  # Fallback (remove in production)
    )

    base_url = (
            st.secrets.get("OPENAI_API_KEY") or
            os.environ.get("OPENAI_API_KEY") or
            "https://openrouter.ai/api/v1"
    )

    if not api_key or api_key == "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":
        st.error("API key not configured. Please set OPENAI_API_KEY in secrets.")
        st.stop()

    client = OpenAI(api_key=api_key, base_url=base_url)

except Exception as d:
    st.error(f"Failed to initialize API client: {str(d)}")
    st.stop()

# Rest of your app...

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