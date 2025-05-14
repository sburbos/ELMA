import streamlit as st
from openai import OpenAI
import requests

# 1. PAGE CONFIG (MUST BE FIRST)
st.set_page_config(
    page_title="EsMa Essay Generator",
    page_icon="✍️",
    layout="wide"
)

# 2. API CONFIGURATION
BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME = "deepseek/deepseek-chat-v3-0324:free"

# 3. SECURE CREDENTIALS HANDLING
try:
    # Get API key with proper existence checks
    if not hasattr(st, 'secrets') or not hasattr(st.secrets, 'openrouter'):
        st.error("❌ Secrets not configured properly")
        st.stop()

    api_key = st.secrets.openrouter.OPENAI_API_KEY

    # Verify API key is valid format
    if not api_key.startswith("sk-or-v1-"):
        st.error("❌ Invalid API key format")
        st.stop()

    # Test authentication with correct endpoint
    auth_response = requests.get(
        f"{BASE_URL}/auth/key",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=10
    )

    if auth_response.status_code != 200:
        st.error(f"🔒 Authentication Failed (HTTP {auth_response.status_code})")
        st.json(auth_response.json())
        st.stop()

except Exception as e:
    st.error(f"⚙️ Configuration Error: {str(e)}")
    st.stop()

# 4. CLIENT SETUP WITH PROPER ENDPOINTS
client = OpenAI(
    api_key=api_key,
    base_url=BASE_URL,
    default_headers={
        "HTTP-Referer": st.secrets.get("SITE_URL", "http://localhost:8501"),
        "X-Title": "EsMa Essay Generator"
    }
)


# 5. ESSAY GENERATION FUNCTION
def generate_essay(prompt: str, essay_type: str) -> str:
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are EsMa, an AI essay writing assistant."},
                {"role": "user", "content": f"Write a {essay_type} essay about: {prompt}"}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"🚨 Generation Error: {str(e)}")
        return None


# 6. STREAMLIT UI
st.title("✍️ EsMa Essay Generator")

with st.form("essay_form"):
    essay_type = st.selectbox(
        "Essay Type",
        ["Argumentative", "Persuasive", "Explanatory", "Narrative"]
    )
    prompt = st.text_area(
        "Your Topic",
        "The impact of artificial intelligence on modern education...",
        height=150
    )

    if st.form_submit_button("Generate Essay"):
        with st.spinner("📝 Crafting your essay..."):
            essay = generate_essay(prompt, essay_type)

        if essay:
            st.success("✅ Essay Generated Successfully!")
            st.text_area("Result", essay, height=300)
            st.download_button(
                "Download Essay",
                essay,
                file_name=f"{essay_type.lower()}_essay.txt"
            )

# 7. DEBUG SECTION (REMOVE IN PRODUCTION)
with st.expander("🔍 Debug Info"):
    st.write("API Base URL:", BASE_URL)
    st.write("Model Name:", MODEL_NAME)
    st.write("Key Prefix:", api_key[:10] + "..." if api_key else "None")