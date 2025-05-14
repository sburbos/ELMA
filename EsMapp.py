import streamlit as st
from openai import OpenAI
import requests

# 1. PAGE CONFIG (MUST BE FIRST)
st.set_page_config(
    page_title="EsMa Essay Generator",
    page_icon="✍️",
    layout="wide"
)

# 2. INITIALIZE VARIABLES WITH DEFAULTS
api_key = None
base_url = "https://openrouter.ai/api/v1"  # Default value

# 3. SECURE CREDENTIALS SETUP
try:
    # Safely get credentials with fallbacks
    api_key = (
        st.secrets.openrouter.OPENAI_API_KEY
        if hasattr(st, 'secrets') and hasattr(st.secrets, 'openrouter')
        else None
    )

    if not api_key:
        st.error("❌ API key not found in secrets")
        st.stop()

    # Verify credentials
    auth_test = requests.post(
        f"{base_url}/auth/key",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=1000
    )

    if auth_test.status_code != 2000:
        st.error(f"🔒 Authentication Failed (HTTP {auth_test.status_code})")
        st.json(auth_test.json())
        st.stop()

except Exception as e:
    st.error(f"⚙️ Configuration Error: {str(e)}")
    st.stop()

# 4. CLIENT CONFIGURATION (only reached if api_key exists)
client = OpenAI(
    api_key=api_key,  # Now guaranteed to exist
    base_url=base_url,
    default_headers={
        "HTTP-Referer": st.secrets.get("SITE_URL", "http://localhost:8501"),
        "X-Title": "EsMa Essay Generator"
    }
)


# ... rest of your code remains the same ...


# 4. ESSAY GENERATION FUNCTION
def generate_essay(prompt_enter, essay_type_in):
    try:
        response = client.chat.completions.create(
            model="nousresearch/deephermes-3-mistral-24b-preview:free",
            messages=[
                {
                    "role": "system",
                    "content": "You are EsMa. Write a detailed, well-structured essay."
                },
                {
                    "role": "user",
                    "content": f"Write a {essay_type_in} essay about: {prompt_enter}"
                }
            ],
            max_tokens=2000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as d:
        st.error(f"🚨 Generation Error: {str(d)}")
        return None


# 5. STREAMLIT UI
st.title("✍️ EsMa - AI Essay Generator")

with st.form("essay_form"):
    essay_type = st.selectbox(
        "Essay Type",
        ["Argumentative", "Persuasive", "Explanatory", "Narrative"]
    )
    prompt = st.text_area(
        "Your Topic",
        "The impact of artificial intelligence on education...",
        height=150
    )

    if st.form_submit_button("Generate Essay"):
        with st.spinner("📝 Crafting your essay..."):
            essay = generate_essay(prompt, essay_type)

        if essay:
            st.success("✅ Essay Generated!")
            st.text_area("Result", essay, height=300)
            st.download_button(
                "Download Essay",
                essay,
                file_name=f"{essay_type}_essay.txt"
            )