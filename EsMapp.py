import streamlit as st
import os
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

# Page configuration (must be first Streamlit command)
st.set_page_config(
    page_title="EsMa",
    page_icon=":writing_hand:",
    layout="wide"
)

# Essay types
list_essay_type = [
    "Argumentative", "Persuasive", 'Explanatory', 'Descriptive',
    "Narrative", 'Cause and Effect', "Process Analysis",
    "Compare/Contrast", "General"
]


def ai_assistant(prompt):
    """Function to call the AI assistant"""
    response = client.chat.completions.create(
        model="deepseek/deepseek-r1-distill-llama-70b:free",
        messages=[
            {
                "role": "system",
                "content": """You are EsMa (Essay Maker), a tool that helps students create essays.
                Strictly only write the requested essay content, no additional commentary."""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content


# Main app function
def main():
    st.subheader("EsMa")
    st.title("Your Free Essay Maker Tool")

    # User inputs
    essay_type = st.selectbox("Select Essay Type", list_essay_type)
    user_prompt = st.text_area(
        "Enter your essay topic or instructions:",
        "Write your prompt here...",
        height=100
    )

    # Generate button
    if st.button("Generate Essay"):
        if user_prompt.strip() == "Write your prompt here..." or not user_prompt.strip():
            st.warning("Please enter a valid prompt")
        else:
            with st.spinner("Generating your essay..."):
                full_prompt = f"Write a {essay_type} essay about: {user_prompt}"
                try:
                    essay = ai_assistant(full_prompt)
                    st.text_area("Generated Essay", essay, height=300)
                except Exception as e:
                    st.error(f"An error occurred: {e}")


# Run the main function
if __name__ == "__main__":
    main()