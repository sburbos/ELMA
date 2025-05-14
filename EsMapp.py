import streamlit as st

from openai import OpenAI
import edge_tts
import asyncio


# Initialize the OpenAI client with proper configuration

st.set_page_config(
    page_title="EsMa",
    page_icon=":writing_hand:",
    layout="wide"
)
# Debug: Show loaded secrets (remove after testing)

def page_1():
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
        "Compare/Contrast","Critique", "Definition", "General"
    ]

    list_level = ["Elementary", "Junior High", "Senior High", "Undergraduate", "Graduate", "Postgraduate", "PhD", "Masters", "Doctorate"]
    list_speech_type = ["Casual", "Intimate", "Formal", "Frozen", "Consultative"]
    left, right = st.columns(2, vertical_alignment="top")


    def ai_assistant(prompt):
        try:
            response = client.chat.completions.create(
                model="nousresearch/deephermes-3-mistral-24b-preview:free",
                messages=[
                    {
                        "role": "system",
                        "content": """You are EsMa (Essay Maker). Strictly only write the requested essay content. 
                        Do not write any other information. Meaning, only write paragraphs. Also the output must have be clear and specific with no vague output"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=20000  # Added to prevent timeouts
            )
            return response.choices[0].message.content
        except Exception as det:
            st.error(f"Failed to generate essay: {str(det)}")
            return None


    # Main app interface
    def main():
        with st.container():
            left.subheader("EsMa by Elley")
            left.title("Your Free Essay Maker Tool")
            right.subheader("")
            right.title("")
        with st.container():
            level_essay = left.selectbox("Type-Level", list_level)
            speech_type = left.selectbox("Type of Speech", list_speech_type)
            essay_type = left.selectbox("Essay Type", list_essay_type)
            word_num = left.slider("Select Number Words", min_value=0, max_value=1500, step=100)
            selected_pov = left.segmented_control('Point of View', ['First', 'Second', 'Third'], selection_mode = "single")

        with st.container():
            content_prompt = left.text_area("Prompt", "", height=150)
            other_info_prompt = left.text_area("Other Instructions", "", height=70)

            if st.button("Generate Essay"):
                if content_prompt.strip() in ("", "Generated prompt"):
                    st.warning("Please enter a valid prompt")
                else:
                    with st.spinner("Generating your essay..."):
                        full_prompt = f"Write a comprehensive {essay_type}, point of view: {selected_pov} point of view, education level: {level_essay},  type of speech: {speech_type}, number of minimum words: {word_num}, essay about: {content_prompt}. With extra task {other_info_prompt}"
                        essay = ai_assistant(full_prompt)
                        if essay:
                            right.text_area("Generated Essay", value=essay, height=680)

            else:
                right.text_area("Generated Essay", "", height=680)


    if __name__ == "__main__":
        main()



voices_by_gender = {
    "Female": {
        "AdriNeural": {"ShortName": "af-ZA-AdriNeural"},
        "AminaNeural": {"ShortName": "ar-DZ-AminaNeural"},
        "AmalNeural": {"ShortName": "ar-QA-AmalNeural"},
        "AmanyNeural": {"ShortName": "ar-SY-AmanyNeural"},
        "AyshaNeural": {"ShortName": "ar-OM-AyshaNeural"},
        "BanuNeural": {"ShortName": "az-AZ-BanuNeural"},
        "KalinaNeural": {"ShortName": "bg-BG-KalinaNeural"},
        "LailaNeural": {"ShortName": "ar-BH-LailaNeural"},
        "LaithNeural": {"ShortName": "ar-SY-LaithNeural"},  # Note: Male, moved below
        "LaylaNeural": {"ShortName": "ar-LB-LaylaNeural"},
        "MekdesNeural": {"ShortName": "am-ET-MekdesNeural"},
        "MaryamNeural": {"ShortName": "ar-YE-MaryamNeural"},
        "MounaNeural": {"ShortName": "ar-MA-MounaNeural"},
        "NabanitaNeural": {"ShortName": "bn-BD-NabanitaNeural"},
        "NouraNeural": {"ShortName": "ar-KW-NouraNeural"},
        "PradeepNeural": {"ShortName": "bn-BD-PradeepNeural"},  # Note: Male, moved below
        "RanaNeural": {"ShortName": "ar-IQ-RanaNeural"},
        "ReemNeural": {"ShortName": "ar-TN-ReemNeural"},
        "SalmaNeural": {"ShortName": "ar-EG-SalmaNeural"},
        "SanaNeural": {"ShortName": "ar-JO-SanaNeural"},
        "TanishaaNeural": {"ShortName": "bn-IN-TanishaaNeural"},
        "VesnaNeural": {"ShortName": "bs-BA-VesnaNeural"},
        "ZariyahNeural": {"ShortName": "ar-SA-ZariyahNeural"},
        # Add all other Female voices here, sorted alphabetically by name
    },
    "Male": {
        "AbdullahNeural": {"ShortName": "ar-OM-AbdullahNeural"},
        "AliNeural": {"ShortName": "ar-BH-AliNeural"},
        "AmehaNeural": {"ShortName": "am-ET-AmehaNeural"},
        "BabekNeural": {"ShortName": "az-AZ-BabekNeural"},
        "BasselNeural": {"ShortName": "ar-IQ-BasselNeural"},
        "BashkarNeural": {"ShortName": "bn-IN-BashkarNeural"},
        "BorislavNeural": {"ShortName": "bg-BG-BorislavNeural"},
        "FahedNeural": {"ShortName": "ar-KW-FahedNeural"},
        "GoranNeural": {"ShortName": "bs-BA-GoranNeural"},
        "HamedNeural": {"ShortName": "ar-SA-HamedNeural"},
        "HediNeural": {"ShortName": "ar-TN-HediNeural"},
        "IlirNeural": {"ShortName": "sq-AL-IlirNeural"},
        "IsmaelNeural": {"ShortName": "ar-DZ-IsmaelNeural"},
        "JamalNeural": {"ShortName": "ar-MA-JamalNeural"},
        "LaithNeural": {"ShortName": "ar-SY-LaithNeural"},
        "MoazNeural": {"ShortName": "ar-QA-MoazNeural"},
        "OmarNeural": {"ShortName": "ar-LY-OmarNeural"},
        "PradeepNeural": {"ShortName": "bn-BD-PradeepNeural"},
        "RamiNeural": {"ShortName": "ar-LB-RamiNeural"},
        "SalehNeural": {"ShortName": "ar-YE-SalehNeural"},
        "ShakirNeural": {"ShortName": "ar-EG-ShakirNeural"},
        "TaimNeural": {"ShortName": "ar-JO-TaimNeural"},
        "WillemNeural": {"ShortName": "af-ZA-WillemNeural"},
        # Add all other Male voices here, sorted alphabetically by name
    }
}





async def text_to_speech(text, filename, character):
    communicate = edge_tts.Communicate(text, character)
    await communicate.save(filename)
    return filename  # Return filename after saving

def page_2():
    st.subheader("TeTos by Elley")
    st.title("Free Online Text-To-Speech Tool ")
    content_prompt = st.text_area("Prompt", "", height=150)
    selected_voice = st.segmented_control('Point of View', ['Male', 'Female'], selection_mode="single")
    voice_final = None
    if selected_voice == "Male":
        voice_final = st.selectbox("Male Characters", list(voices_by_gender["Male"].keys()))
    elif selected_voice == "Female":
        voice_final = st.selectbox("Female Characters", list(voices_by_gender["Female"].keys()))
    if st.button("Generate Voice"):
        if content_prompt.strip() in ("", "Generated prompt"):
            st.warning("Please enter a valid prompt")
        else:
            with st.spinner("Generating your voice..."):
                filename = "voice.mp3"
                # Run the async function properly
                voice_arranged = voice_final[selected_voice][voice_final]["ShortName"]
                asyncio.run(text_to_speech(content_prompt, filename,voice_arranged))
                # Open the saved file and pass bytes to st.audio
                with open(filename, "rb") as f:
                    audio_bytes = f.read()
                st.audio(audio_bytes, format="audio/mpeg", loop=True)



pg = st.navigation([st.Page(page_1, title = "Essay Maker"), st.Page(page_2, title = "Text To Speech")])
pg.run()



