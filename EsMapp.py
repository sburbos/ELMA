import streamlit as st
from openai import OpenAI

# ===== 1. PAGE CONFIG MUST BE FIRST =====
st.set_page_config(
    page_title="EsMa",
    page_icon=":writing_hand:",
    layout="wide"
)

# ===== 2. SECRETS HANDLING =====
try:
    # Access nested secrets
    api_key = st.secrets.openrouter.OPENAI_API_KEY
    base_url = st.secrets.openrouter.OPENAI_BASE_URL

    # Initialize client
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    # Quick connection test
    client.models.list()

except Exception as e:
    st.error(f"""
    🔌 Connection Failed: {str(e)}

    Current secret structure:
    ```python
    {st.secrets}
    ```
    """)
    st.stop()

# ===== 3. YOUR APP CODE =====
list_essay_type = [
    "Argumentative", "Persuasive", 'Explanatory', 'Descriptive',
    "Narrative", 'Cause and Effect', "Process Analysis",
    "Compare/Contrast", "General"
]

with st.container():
    st.subheader("EsMa")
    st.title("Your Free Essay Maker Tool")

    essay_type = st.selectbox("Essay Type", list_essay_type)
    content_prompt = st.text_area("Prompt", "Write your prompt here:", height=100)

    if st.button("Generate Essay"):
        if content_prompt.strip() in ("", "Write your prompt here:"):
            st.warning("Please enter a prompt")
        else:
            with st.spinner("Generating your essay..."):
                full_prompt = f"Write a {essay_type} essay about: {content_prompt}"
                try:
                    essay = client.chat.completions.create(
                        model="deepseek/deepseek-chat-v3-0324:free",
                        messages=[
                            {"role": "system", "content": "You are EsMa, an essay writing assistant."},
                            {"role": "user", "content": full_prompt}
                        ]
                    ).choices[0].message.content

                    st.text_area("Generated Essay", essay, height=300)
                except Exception as e:
                    st.error(f"Essay generation failed: {str(e)}")