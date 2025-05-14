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

    languages = ["English (US)", "Filipino", "Hindi" ]

    content_list_category = ["Facebook", "Youtube", "Tiktok", "Twitter/X", "Reddit", 'Instagram', "Spotify",]
    content_list_content = ["Vlog", "Blog", "Written Post", "Podcast", "Music", "Article",]
    content_list_complexity = ["Micro-Content", "Standard Content", "Premium Content", "Enterprise Content", "Legacy Content",]
    content_list_tiers = ["Beginner", "Intermediate", "Advanced", "Expert",]
    content_creator_types = [
        # YouTube/TikTok Types
        "The Guru",
        "The Everyman",
        "The Mad Scientist",
        "The Storyteller",
        "The Entertainer",

        # Educational Content Types
        "The Professor",
        "The Simplifier",
        "The Debunker",
        "The Coach",

        # Fiction/Narrative Types
        "The Hero",
        "The Mentor",
        "The Trickster",
        "The Villain",

        # Additional Digital Types
        "The Reactor",
        "The Investigator",
        "The Trendsetter",
        "The Parodist",
        "The Nostalgist",
        "The Minimalist",
    ]


    def ai_assistant(prompt):
        try:
            response = client.chat.completions.create(
                model="nousresearch/deephermes-3-mistral-24b-preview:free",
                messages=[
                    {
                        "role": "system",
                        "content": """You are EsMa. Strictly only write the requested essay content or content creation scripts. 
                        Do not write any other information. Meaning, only write paragraphs (unless user chose content creation). Also the output must have be clear and specific with no vague output"""
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
        on = right.toggle("Activate Content Creation")
        if not on:
            with st.container():
                level_essay = left.selectbox("Type-Level", list_level)
                speech_type = left.selectbox("Type of Speech", list_speech_type)
                essay_type = left.selectbox("Essay Type", list_essay_type)
                speech = left.selectbox("Select Language", languages)
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
                            full_prompt = f"Write a comprehensive {essay_type}, point of view: {selected_pov} point of view, education level: {level_essay}, language to use:{speech},  type of speech: {speech_type}, number of minimum words: {word_num}, essay about: {content_prompt}. With extra task {other_info_prompt}"
                            essay = ai_assistant(full_prompt)
                            if essay:
                                right.text_area("Generated Essay", value=essay, height=680)

                else:
                    right.text_area("Generated Essay", "", height=680)
        else:
            with st.container():
                content_place = left.selectbox("Where to Post?", content_list_category)
                content_type = left.selectbox("Type of Content", content_list_content)
                content_complexity = left.selectbox("Content Complexity", content_list_complexity)
                content_tier = left.selectbox("Content Tier", content_list_tiers)
                selected_character= left.selectbox("Select Language", content_creator_types)
                speech = left.segmented_control('Point of View', languages, selection_mode="single")

            with st.container():
                content_prompt = left.text_area("Prompt", "", height=150)
                other_info_prompt = left.text_area("Other Instructions", "", height=70)

                if st.button("Generate Essay"):
                    if content_prompt.strip() in ("", "Generated prompt"):
                        st.warning("Please enter a valid prompt")
                    else:
                        with st.spinner("Generating your essay..."):
                            full_prompt = f"""Write a content about: {content_prompt} in a language:{speech}that will be posted or used in: {content_place}
                            having a content type: {content_type}, having a content complexity: {content_complexity}, having a content tier for: {content_tier}
                            and will portray a character: {selected_character}. With extra task {other_info_prompt}
                                                
"""
                            content_out = ai_assistant(full_prompt)
                            if content_out:
                                right.text_area("Generated Content", value=content_out, height=680)

                else:
                    right.text_area("Generated Content", "", height=680)



    if __name__ == "__main__":
        main()



voices_by_gender = {
  "Male": {
    "AbdullahNeural (Oman)": {"ShortName": "ar-OM-AbdullahNeural"},
    "AliNeural (Bahrain)": {"ShortName": "ar-BH-AliNeural"},
    "AhmetNeural (Turkey)": {"ShortName": "tr-TR-AhmetNeural"},
    "AledNeural (Wales)": {"ShortName": "cy-GB-AledNeural"},
    "AleksandarNeural (North Macedonia)": {"ShortName": "mk-MK-AleksandarNeural"},
    "AlvaroNeural (Spain)": {"ShortName": "es-ES-AlvaroNeural"},
    "AlonsoNeural (United States)": {"ShortName": "es-US-AlonsoNeural"},
    "AndresNeural (Guatemala)": {"ShortName": "es-GT-AndresNeural"},
    "AntoineNeural (Canada)": {"ShortName": "fr-CA-AntoineNeural"},
    "AntoninNeural (Czech)": {"ShortName": "cs-CZ-AntoninNeural"},
    "AnbuNeural (Singapore)": {"ShortName": "ta-SG-AnbuNeural"},
    "ArdiNeural (Indonesian)": {"ShortName": "id-ID-ArdiNeural"},
    "ArnaudNeural (Belgium)": {"ShortName": "nl-BE-ArnaudNeural"},
    "AsadNeural (Pakistan)": {"ShortName": "ur-PK-AsadNeural"},
    "AviNeural (Israel)": {"ShortName": "he-IL-AvriNeural"},
    "BabekNeural (Azerbaijani)": {"ShortName": "az-AZ-BabekNeural"},
    "BashkarNeural (Bengali)": {"ShortName": "bn-IN-BashkarNeural"},
    "BasselNeural (Iraq)": {"ShortName": "ar-IQ-BasselNeural"},
    "BorislavNeural (Bulgarian)": {"ShortName": "bg-BG-BorislavNeural"},
    "CarlosNeural (Honduras)": {"ShortName": "es-HN-CarlosNeural"},
    "ChilembaNeural (Kenya)": {"ShortName": "en-KE-ChilembaNeural"},
    "ChristopherNeural (US)": {"ShortName": "en-US-ChristopherNeural"},
    "ColmNeural (Irish)": {"ShortName": "ga-IE-ColmNeural"},
    "ConradNeural (German)": {"ShortName": "de-DE-ConradNeural"},
    "ConnorNeural (Ireland)": {"ShortName": "en-IE-ConnorNeural"},
    "DauletNeural (Kazakh)": {"ShortName": "kk-KZ-DauletNeural"},
    "DaudNeural (Tanzania)": {"ShortName": "sw-TZ-DaudiNeural"},
    "DmitryNeural (Russian)": {"ShortName": "ru-RU-DmitryNeural"},
    "DiegoNeural (Italian)": {"ShortName": "it-IT-DiegoNeural"},
    "DimasNeural (Javanese)": {"ShortName": "jv-ID-DimasNeural"},
    "DuarteNeural (Portuguese)": {"ShortName": "pt-PT-DuarteNeural"},
    "EmilNeural (Romanian)": {"ShortName": "ro-RO-EmilNeural"},
    "EnricNeural (Catalan)": {"ShortName": "ca-ES-EnricNeural"},
    "EricNeural (US)": {"ShortName": "en-US-EricNeural"},
    "EveritaNeural (Latvian)": {"ShortName": "lv-LV-EveritaNeural"},
    "FabriceNeural (Swiss French)": {"ShortName": "fr-CH-FabriceNeural"},
    "FaridNeural (Persian)": {"ShortName": "fa-IR-FaridNeural"},
    "FedericoNeural (Nicaragua)": {"ShortName": "es-NI-FedericoNeural"},
    "FinnNeural (Norwegian)": {"ShortName": "nb-NO-FinnNeural"},
    "GaganNeural (Kannada)": {"ShortName": "kn-IN-GaganNeural"},
    "GerardNeural (Belgian French)": {"ShortName": "fr-BE-GerardNeural"},
    "GiorgiNeural (Georgian)": {"ShortName": "ka-GE-GiorgiNeural"},
    "GonzaloNeural (Colombia)": {"ShortName": "es-CO-GonzaloNeural"},
    "GoranNeural (Bosnian)": {"ShortName": "bs-BA-GoranNeural"},
    "GulNawazNeural (Pashto)": {"ShortName": "ps-AF-GulNawazNeural"},
    "GunnarNeural (Icelandic)": {"ShortName": "is-IS-GunnarNeural"},
    "GuyNeural (US)": {"ShortName": "en-US-GuyNeural"},
    "HamdanNeural (UAE)": {"ShortName": "ar-AE-HamdanNeural"},
    "HamedNeural (Saudi Arabia)": {"ShortName": "ar-SA-HamedNeural"},
    "HarriNeural (Finnish)": {"ShortName": "fi-FI-HarriNeural"},
    "HenriNeural (French)": {"ShortName": "fr-FR-HenriNeural"},
    "HediNeural (Tunisia)": {"ShortName": "ar-TN-HediNeural"},
    "IlirNeural (Albanian)": {"ShortName": "sq-AL-IlirNeural"},
    "InJoonNeural (Korean)": {"ShortName": "ko-KR-InJoonNeural"},
    "IsmaelNeural (Algeria)": {"ShortName": "ar-DZ-IsmaelNeural"},
    "JanNeural (Swiss German)": {"ShortName": "de-CH-JanNeural"},
    "JajangNeural (Sundanese)": {"ShortName": "su-ID-JajangNeural"},
    "JamalNeural (Morocco)": {"ShortName": "ar-MA-JamalNeural"},
    "JavierNeural (Equatorial Guinea)": {"ShortName": "es-GQ-JavierNeural"},
    "JeanNeural (Canadian French)": {"ShortName": "fr-CA-JeanNeural"},
    "JeppeNeural (Danish)": {"ShortName": "da-DK-JeppeNeural"},
    "JonasNeural (Austrian German)": {"ShortName": "de-AT-JonasNeural"},
    "JorgeNeural (Mexico)": {"ShortName": "es-MX-JorgeNeural"},
    "JosephNeural (Maltese)": {"ShortName": "mt-MT-JosephNeural"},
    "JuanNeural (Costa Rica)": {"ShortName": "es-CR-JuanNeural"},
    "KertNeural (Estonian)": {"ShortName": "et-EE-KertNeural"},
    "KillianNeural (German)": {"ShortName": "de-DE-KillianNeural"},
    "KumarNeural (Sri Lanka Tamil)": {"ShortName": "ta-LK-KumarNeural"},
    "LaithNeural (Syria)": {"ShortName": "ar-SY-LaithNeural"},
    "LiamNeural (Canada)": {"ShortName": "en-CA-LiamNeural"},
    "LeonasNeural (Lithuanian)": {"ShortName": "lt-LT-LeonasNeural"},
    "LorenzoNeural (Chile)": {"ShortName": "es-CL-LorenzoNeural"},
    "LukasNeural (Slovak)": {"ShortName": "sk-SK-LukasNeural"},
    "LuisNeural (Ecuador)": {"ShortName": "es-EC-LuisNeural"},
    "LukeNeural (South Africa)": {"ShortName": "en-ZA-LukeNeural"},
    "MadhurNeural (Hindi)": {"ShortName": "hi-IN-MadhurNeural"},
    "MaartenNeural (Dutch)": {"ShortName": "nl-NL-MaartenNeural"},
    "ManoharNeural (Marathi)": {"ShortName": "mr-IN-ManoharNeural"},
    "ManuelNeural (Cuba)": {"ShortName": "es-CU-ManuelNeural"},
    "MarekNeural (Polish)": {"ShortName": "pl-PL-MarekNeural"},
    "MarioNeural (Paraguay)": {"ShortName": "es-PY-MarioNeural"},
    "MateoNeural (Uruguay)": {"ShortName": "es-UY-MateoNeural"},
    "MattiasNeural (Swedish)": {"ShortName": "sv-SE-MattiasNeural"},
    "MidhunNeural (Malayalam)": {"ShortName": "ml-IN-MidhunNeural"},
    "MitchellNeural (New Zealand)": {"ShortName": "en-NZ-MitchellNeural"},
    "MohanNeural (Telugu)": {"ShortName": "te-IN-MohanNeural"},
    "MoazNeural (Qatar)": {"ShortName": "ar-QA-MoazNeural"},
    "MuuseNeural (Somali)": {"ShortName": "so-SO-MuuseNeural"},
    "NamMinhNeural (Vietnamese)": {"ShortName": "vi-VN-NamMinhNeural"},
    "NestorasNeural (Greek)": {"ShortName": "el-GR-NestorasNeural"},
    "NicholasNeural (Serbian)": {"ShortName": "sr-RS-NicholasNeural"},
    "NilsNeural (Latvian)": {"ShortName": "lv-LV-NilsNeural"},
    "NiranjanNeural (Gujarati)": {"ShortName": "gu-IN-NiranjanNeural"},
    "NiwatNeural (Thai)": {"ShortName": "th-TH-NiwatNeural"},
    "OmarNeural (Libya)": {"ShortName": "ar-LY-OmarNeural"},
    "OstapNeural (Ukrainian)": {"ShortName": "uk-UA-OstapNeural"},
    "OsmanNeural (Malay)": {"ShortName": "ms-MY-OsmanNeural"},
    "PisethNeural (Khmer)": {"ShortName": "km-KH-PisethNeural"},
    "PrabhatNeural (Indian English)": {"ShortName": "en-IN-PrabhatNeural"},
    "PradeepNeural (Bangla)": {"ShortName": "bn-BD-PradeepNeural"},
    "RafikiNeural (Swahili Kenya)": {"ShortName": "sw-KE-RafikiNeural"},
    "RamiNeural (Lebanon)": {"ShortName": "ar-LB-RamiNeural"},
    "RokNeural (Slovenian)": {"ShortName": "sl-SI-RokNeural"},
    "RogerNeural (US)": {"ShortName": "en-US-RogerNeural"},
    "RoiNeural (Galician)": {"ShortName": "gl-ES-RoiNeural"},
    "RyanNeural (UK)": {"ShortName": "en-GB-RyanNeural"},
    "SagarNeural (Nepali)": {"ShortName": "ne-NP-SagarNeural"},
    "SalmanNeural (Urdu India)": {"ShortName": "ur-IN-SalmanNeural"},
    "SameeraNeural (Sinhala)": {"ShortName": "si-LK-SameeraNeural"},
    "SamNeural (Hong Kong English)": {"ShortName": "en-HK-SamNeural"},
    "SardorNeural (Uzbek)": {"ShortName": "uz-UZ-SardorNeural"},
    "SebastianNeural (Venezuela)": {"ShortName": "es-VE-SebastianNeural"},
    "ShakirNeural (Egypt)": {"ShortName": "ar-EG-ShakirNeural"},
    "SteffanNeural (US)": {"ShortName": "en-US-SteffanNeural"},
    "SreckoNeural (Croatian)": {"ShortName": "hr-HR-SreckoNeural"},
    "SuryaNeural (Malaysian Tamil)": {"ShortName": "ta-MY-SuryaNeural"},
    "TaimNeural (Jordan)": {"ShortName": "ar-JO-TaimNeural"},
    "TamasNeural (Hungarian)": {"ShortName": "hu-HU-TamasNeural"},
    "ThembaNeural (Zulu)": {"ShortName": "zu-ZA-ThembaNeural"},
    "ThomasNeural (UK)": {"ShortName": "en-GB-ThomasNeural"},
    "ThihaNeural (Burmese)": {"ShortName": "my-MM-ThihaNeural"},
    "ValluvarNeural (Tamil)": {"ShortName": "ta-IN-ValluvarNeural"},
    "WanLungNeural (Cantonese)": {"ShortName": "zh-HK-WanLungNeural"},
    "WayneNeural (Singapore English)": {"ShortName": "en-SG-WayneNeural"},
    "WilliamNeural (Australian)": {"ShortName": "en-AU-WilliamNeural"},
    "WillemNeural (Afrikaans)": {"ShortName": "af-ZA-WillemNeural"},
    "YunJheNeural (Taiwanese Mandarin)": {"ShortName": "zh-TW-YunJheNeural"},
    "YunjianNeural (Chinese)": {"ShortName": "zh-CN-YunjianNeural"},
    "YunxiNeural (Chinese)": {"ShortName": "zh-CN-YunxiNeural"},
    "YunxiaNeural (Chinese)": {"ShortName": "zh-CN-YunxiaNeural"},
    "YunyangNeural (Chinese)": {"ShortName": "zh-CN-YunyangNeural"},
  },
  "Female": {
    "AarohiNeural (Marathi)": {"ShortName": "mr-IN-AarohiNeural"},
    "AdriNeural (Afrikaans)": {"ShortName": "af-ZA-AdriNeural"},
    "AigulNeural (Kazakh)": {"ShortName": "kk-KZ-AigulNeural"},
    "AminaNeural (Algeria)": {"ShortName": "ar-DZ-AminaNeural"},
    "AmalNeural (Qatar)": {"ShortName": "ar-QA-AmalNeural"},
    "AmanyNeural (Syria)": {"ShortName": "ar-SY-AmanyNeural"},
    "AnaNeural (US)": {"ShortName": "en-US-AnaNeural"},
    "AnilaNeural (Albanian)": {"ShortName": "sq-AL-AnilaNeural"},
    "AnuNeural (Estonian)": {"ShortName": "et-EE-AnuNeural"},
    "AriaNeural (US)": {"ShortName": "en-US-AriaNeural"},
    "ArianeNeural (Swiss French)": {"ShortName": "fr-CH-ArianeNeural"},
    "AsiliaNeural (Kenyan English)": {"ShortName": "en-KE-AsiliaNeural"},
    "AthinaNeural (Greek)": {"ShortName": "el-GR-AthinaNeural"},
    "AyshaNeural (Oman)": {"ShortName": "ar-OM-AyshaNeural"},
    "BanuNeural (Azerbaijani)": {"ShortName": "az-AZ-BanuNeural"},
    "BlessicaNeural (Filipino)": {"ShortName": "fil-PH-BlessicaNeural"},
    "CamilaNeural (Peru)": {"ShortName": "es-PE-CamilaNeural"},
    "CatalinaNeural (Chile)": {"ShortName": "es-CL-CatalinaNeural"},
    "CharlineNeural (Belgian French)": {"ShortName": "fr-BE-CharlineNeural"},
    "ChristelNeural (Danish)": {"ShortName": "da-DK-ChristelNeural"},
    "ClaraNeural (Canada)": {"ShortName": "en-CA-ClaraNeural"},
    "ColetteNeural (Dutch)": {"ShortName": "nl-NL-ColetteNeural"},
    "DaliaNeural (Mexico)": {"ShortName": "es-MX-DaliaNeural"},
    "DeniseNeural (French)": {"ShortName": "fr-FR-DeniseNeural"},
    "DenaNeural (Belgian Dutch)": {"ShortName": "nl-BE-DenaNeural"},
    "DilaraNeural (Persian)": {"ShortName": "fa-IR-DilaraNeural"},
    "DhwaniNeural (Gujarati)": {"ShortName": "gu-IN-DhwaniNeural"},
    "EkaNeural (Georgian)": {"ShortName": "ka-GE-EkaNeural"},
    "ElenaNeural (Argentina)": {"ShortName": "es-AR-ElenaNeural"},
    "EloiseNeural (French)": {"ShortName": "fr-FR-EloiseNeural"},
    "ElsaNeural (Italian)": {"ShortName": "it-IT-ElsaNeural"},
    "ElviraNeural (Spanish)": {"ShortName": "es-ES-ElviraNeural"},
    "EmilyNeural (Ireland)": {"ShortName": "en-IE-EmilyNeural"},
    "EzinneNeural (Nigeria)": {"ShortName": "en-NG-EzinneNeural"},
    "FahedNeural (Kuwait)": {"ShortName": "ar-KW-FahedNeural"},
    "FatimaNeural (UAE)": {"ShortName": "ar-AE-FatimaNeural"},
    "FennaNeural (Dutch)": {"ShortName": "nl-NL-FennaNeural"},
    "FranciscaNeural (Brazilian Portuguese)": {"ShortName": "pt-BR-FranciscaNeural"},
    "GabrijelaNeural (Croatian)": {"ShortName": "hr-HR-GabrijelaNeural"},
    "GadisNeural (Indonesian)": {"ShortName": "id-ID-GadisNeural"},
    "GraceNeural (Maltese)": {"ShortName": "mt-MT-GraceNeural"},
    "GulNeural (Urdu India)": {"ShortName": "ur-IN-GulNeural"},
    "HilaNeural (Hebrew)": {"ShortName": "he-IL-HilaNeural"},
    "HiuGaaiNeural (Cantonese)": {"ShortName": "zh-HK-HiuGaaiNeural"},
    "HiuMaanNeural (Cantonese)": {"ShortName": "zh-HK-HiuMaanNeural"},
    "HoaiMyNeural (Vietnamese)": {"ShortName": "vi-VN-HoaiMyNeural"},
    "HsiaoChenNeural (Taiwanese Mandarin)": {"ShortName": "zh-TW-HsiaoChenNeural"},
    "HsiaoYuNeural (Taiwanese Mandarin)": {"ShortName": "zh-TW-HsiaoYuNeural"},
    "ImaniNeural (Tanzanian English)": {"ShortName": "en-TZ-ImaniNeural"},
    "ImanNeural (Libya)": {"ShortName": "ar-LY-ImanNeural"},
    "IsabellaNeural (Italian)": {"ShortName": "it-IT-IsabellaNeural"},
    "JoanaNeural (Catalan)": {"ShortName": "ca-ES-JoanaNeural"},
    "JennyNeural (US)": {"ShortName": "en-US-JennyNeural"},
    "KaniNeural (Malaysian Tamil)": {"ShortName": "ta-MY-KaniNeural"},
    "KarlaNeural (Honduras)": {"ShortName": "es-HN-KarlaNeural"},
    "KarinaNeural (Puerto Rico)": {"ShortName": "es-PR-KarinaNeural"},
    "KalinaNeural (Bulgarian)": {"ShortName": "bg-BG-KalinaNeural"},
    "KatjaNeural (German)": {"ShortName": "de-DE-KatjaNeural"},
    "KeomanyNeural (Lao)": {"ShortName": "lo-LA-KeomanyNeural"},
    "LailaNeural (Bahrain)": {"ShortName": "ar-BH-LailaNeural"},
    "LatifaNeural (Pashto)": {"ShortName": "ps-AF-LatifaNeural"},
    "LaylaNeural (Lebanon)": {"ShortName": "ar-LB-LaylaNeural"},
    "LeahNeural (South Africa)": {"ShortName": "en-ZA-LeahNeural"},
    "LibbyNeural (UK)": {"ShortName": "en-GB-LibbyNeural"},
    "LenaNeural (Swiss German)": {"ShortName": "de-CH-LeniNeural"},
    "LorenaNeural (El Salvador)": {"ShortName": "es-SV-LorenaNeural"},
    "LunaNeural (Singapore English)": {"ShortName": "en-SG-LunaNeural"},
    "MarijaNeural (Macedonian)": {"ShortName": "mk-MK-MarijaNeural"},
    "MartaNeural (Guatemala)": {"ShortName": "es-GT-MartaNeural"},
    "MaryamNeural (Yemen)": {"ShortName": "ar-YE-MaryamNeural"},
    "MaisieNeural (UK)": {"ShortName": "en-GB-MaisieNeural"},
    "MekdesNeural (Amharic)": {"ShortName": "am-ET-MekdesNeural"},
    "MichelleNeural (US)": {"ShortName": "en-US-MichelleNeural"},
    "MollyNeural (New Zealand)": {"ShortName": "en-NZ-MollyNeural"},
    "MounaNeural (Morocco)": {"ShortName": "ar-MA-MounaNeural"},
    "NabanitaNeural (Bangla)": {"ShortName": "bn-BD-NabanitaNeural"},
    "NanamiNeural (Japanese)": {"ShortName": "ja-JP-NanamiNeural"},
    "NatashaNeural (Australian)": {"ShortName": "en-AU-NatashaNeural"},
    "NeerjaNeural (Indian English)": {"ShortName": "en-IN-NeerjaNeural"},
    "NiaNeural (Welsh)": {"ShortName": "cy-GB-NiaNeural"},
    "NilarNeural (Burmese)": {"ShortName": "my-MM-NilarNeural"},
    "NoemiNeural (Hungarian)": {"ShortName": "hu-HU-NoemiNeural"},
    "NooraNeural (Finnish)": {"ShortName": "fi-FI-NooraNeural"},
    "NouraNeural (Kuwait)": {"ShortName": "ar-KW-NouraNeural"},
    "OnaNeural (Lithuanian)": {"ShortName": "lt-LT-OnaNeural"},
    "PallaviNeural (Tamil)": {"ShortName": "ta-IN-PallaviNeural"},
    "PalomaNeural (US Spanish)": {"ShortName": "es-US-PalomaNeural"},
    "PaolaNeural (Venezuela)": {"ShortName": "es-VE-PaolaNeural"},
    "PetraNeural (Slovenian)": {"ShortName": "sl-SI-PetraNeural"},
    "PolinaNeural (Ukrainian)": {"ShortName": "uk-UA-PolinaNeural"},
    "PernilleNeural (Norwegian)": {"ShortName": "nb-NO-PernilleNeural"},
    "PremwadeeNeural (Thai)": {"ShortName": "th-TH-PremwadeeNeural"},
    "RaquelNeural (Portuguese)": {"ShortName": "pt-PT-RaquelNeural"},
    "ReemNeural (Tunisia)": {"ShortName": "ar-TN-ReemNeural"},
    "RehemaNeural (Swahili Tanzania)": {"ShortName": "sw-TZ-RehemaNeural"},
    "RosaNeural (Philippine English)": {"ShortName": "en-PH-RosaNeural"},
    "SalmaNeural (Egypt)": {"ShortName": "ar-EG-SalmaNeural"},
    "SalomeNeural (Colombia)": {"ShortName": "es-CO-SalomeNeural"},
    "SanaNeural (Jordan)": {"ShortName": "ar-JO-SanaNeural"},
    "SabelaNeural (Galician)": {"ShortName": "gl-ES-SabelaNeural"},
    "SapnaNeural (Kannada)": {"ShortName": "kn-IN-SapnaNeural"},
    "SaranyaNeural (Sri Lanka Tamil)": {"ShortName": "ta-LK-SaranyaNeural"},
    "ShrutiNeural (Telugu)": {"ShortName": "te-IN-ShrutiNeural"},
    "SitiNeural (Javanese)": {"ShortName": "jv-ID-SitiNeural"},
    "SobhanaNeural (Malayalam)": {"ShortName": "ml-IN-SobhanaNeural"},
    "SofieNeural (Swedish)": {"ShortName": "sv-SE-SofieNeural"},
    "SoniaNeural (UK)": {"ShortName": "en-GB-SoniaNeural"},
    "SophieNeural (Serbian)": {"ShortName": "sr-RS-SophieNeural"},
    "SunHiNeural (Korean)": {"ShortName": "ko-KR-SunHiNeural"},
    "SvetlanaNeural (Russian)": {"ShortName": "ru-RU-SvetlanaNeural"},
    "SwaraNeural (Hindi)": {"ShortName": "hi-IN-SwaraNeural"},
    "TanishaaNeural (Bengali)": {"ShortName": "bn-IN-TanishaaNeural"},
    "TaniaNeural (Paraguay)": {"ShortName": "es-PY-TaniaNeural"},
    "TeresaNeural (Equatorial Guinea)": {"ShortName": "es-GQ-TeresaNeural"},
    "ThandoNeural (Zulu)": {"ShortName": "zu-ZA-ThandoNeural"},
    "ThiliniNeural (Sinhala)": {"ShortName": "si-LK-ThiliniNeural"},
    "TutiNeural (Sundanese)": {"ShortName": "su-ID-TutiNeural"},
    "UzmaNeural (Urdu Pakistan)": {"ShortName": "ur-PK-UzmaNeural"},
    "ValentinaNeural (Uruguay)": {"ShortName": "es-UY-ValentinaNeural"},
    "VenbaNeural (Singapore Tamil)": {"ShortName": "ta-SG-VenbaNeural"},
    "VesnaNeural (Bosnian)": {"ShortName": "bs-BA-VesnaNeural"},
    "ViktoriaNeural (Slovak)": {"ShortName": "sk-SK-ViktoriaNeural"},
    "VlastaNeural (Czech)": {"ShortName": "cs-CZ-VlastaNeural"},
    "XiaobeiNeural (Liaoning Mandarin)": {"ShortName": "zh-CN-liaoning-XiaobeiNeural"},
    "XiaoniNeural (Shaanxi Mandarin)": {"ShortName": "zh-CN-shaanxi-XiaoniNeural"},
    "XiaoxiaoNeural (Chinese)": {"ShortName": "zh-CN-XiaoxiaoNeural"},
    "XiaoyiNeural (Chinese)": {"ShortName": "zh-CN-XiaoyiNeural"},
    "YanNeural (Hong Kong English)": {"ShortName": "en-HK-YanNeural"},
    "YasminNeural (Malay)": {"ShortName": "ms-MY-YasminNeural"},
    "YesuiNeural (Mongolian)": {"ShortName": "mn-MN-YesuiNeural"},
    "ZariyahNeural (Saudi Arabia)": {"ShortName": "ar-SA-ZariyahNeural"},
    "ZofiaNeural (Polish)": {"ShortName": "pl-PL-ZofiaNeural"},
    "ZuriNeural (Swahili Kenya)": {"ShortName": "sw-KE-ZuriNeural"},
  },
}





async def text_to_speech(text, filename, character):
    communicate = edge_tts.Communicate(text, character)
    await communicate.save(filename)
    return filename  # Return filename after saving

def page_2():
    st.subheader("TeTos by Elley")
    st.title("Free Online Text-To-Speech Tool ")
    content_prompt = st.text_area("Prompt", "", height=150)
    selected_voice = st.segmented_control('Gender', ['Male', 'Female'], selection_mode="single")
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
                voice_arranged = voices_by_gender[selected_voice][voice_final]["ShortName"]
                asyncio.run(text_to_speech(content_prompt, filename,voice_arranged))
                # Open the saved file and pass bytes to st.audio
                with open(filename, "rb") as f:
                    audio_bytes = f.read()
                st.audio(audio_bytes, format="audio/mpeg", loop=True)


def page_3():
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

    def ai_assistant(messages):
        try:
            response = client.chat.completions.create(
                model="nousresearch/deephermes-3-mistral-24b-preview:free",
                messages=messages,
                max_tokens=20000
            )
            return response.choices[0].message.content
        except Exception as det:
            st.error(f"Failed to generate response: {str(det)}")
            return None

    st.title("AITO")
    st.caption("AI TOol for General Purpose")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You shall be named AITO a general AI TOol"}
        ]

    # Display chat messages from history
    for msg in st.session_state.messages:
        if msg["role"] != "system":  # Don't display system messages
            st.chat_message(msg["role"]).write(msg["content"])

    # Accept user input
    if prompt := st.chat_input():
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Get AI response with full conversation history
        response = ai_assistant(st.session_state.messages)

        if response:
            # Add AI response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.chat_message("assistant").write(response)



pg = st.navigation([st.Page(page_1, title = "Essay Maker"), st.Page(page_2, title = "Text To Speech"), st.Page(page_3, title = "AITO"),])
pg.run()



