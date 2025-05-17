#google api key AIzaSyAI_nzXk4dW-VUxG7T23uB_Tm9WXT3ZQ1M
import streamlit as st
import tempfile
from attr import NothingType
from openai import OpenAI
import edge_tts
import asyncio
import PyPDF2
from io import StringIO
import ast
from streamlit.components.v1 import html
import math
from bs4 import BeautifulSoup
import numpy as np
from difflib import SequenceMatcher
import os
import requests

# Initialize the OpenAI client with proper configuration

st.set_page_config(
    page_title="LleY",
    page_icon=":writing_hand:",
    layout="wide"
)
st.logo("final logo 2.png", icon_image="enlarge 1.png", size = "large")

#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
#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
import requests

def ai_assistant(prompt, rule):
    keys = st.secrets.openrouter.API_KEYS
    base_url = "https://openrouter.ai/api/v1/chat/completions"

    for key in keys:
        try:
            headers = {
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://lley-ai.streamlit.app/",
                "X-Title": "LleY Ai"
            }

            messages = prompt if isinstance(prompt, list) else [
                {"role": "system", "content": rule},
                {"role": "user", "content": prompt}
            ]

            data = {
                "model": "nousresearch/deephermes-3-mistral-24b-preview:free",
                "messages": messages,
                "max_tokens": 2048
            }

            response = requests.post(base_url, headers=headers, json=data)

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            elif response.status_code == 429:
                st.warning(f"⚠️ API key ending in ...{key[-4:]} hit rate limit. Trying next key...")
                continue  # Try the next key
            else:
                continue

        except Exception as e:
            st.warning(f"⚠️ Failed with key ...{key[-4:]}, trying next. Error: {e}")
            continue

    st.error("🚫 All API keys failed or exceeded their limits.")
    return None



def main_page():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@700&display=swap');

        /* Remove all default margins/padding */
        html, body, .stApp {
            overflow: hidden !important;
            height: 100vh !important;
            width: 100vw !important;
            margin: 0 !important;
            padding: 0 !important;
            background: #000 !important;
        }

        /* Centered container */
        .center-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /* Main text styling */
        .main-text {
            font-family: 'Chakra Petch', sans-serif;
            font-size: clamp(3rem, 10vw, 8rem);
            font-weight: 700;
            color: #ff6a6a;
            text-transform: uppercase;
            letter-spacing: 0.5rem;
            text-align: center;
            position: relative;
            z-index: 10;
        }

        /* Orbiting circles container */
        .orbit-container {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
        }

        /* Circle styling */
        .orbiting-circle {
            position: absolute;
            border-radius: 50%;
            background: transparent;
            border: 2px solid #ff69b4;
            filter: drop-shadow(0 0 5px #ff1493);
            transform-origin: center center;
        }
    </style>
    """, unsafe_allow_html=True)

    # JavaScript for orbiting circles animation
    html("""
    <script>
    // Wait for Streamlit to fully load
    function waitForElm(selector) {
        return new Promise(resolve => {
            if (document.querySelector(selector)) {
                return resolve(document.querySelector(selector));
            }

            const observer = new MutationObserver(mutations => {
                if (document.querySelector(selector)) {
                    observer.disconnect();
                    resolve(document.querySelector(selector));
                }
            });

            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        });
    }

    waitForElm('.center-container').then((container) => {
        // Create orbit container
        const orbitContainer = document.createElement('div');
        orbitContainer.className = 'orbit-container';
        container.prepend(orbitContainer);

        const centerX = window.innerWidth / 2;
        const centerY = window.innerHeight / 2;

        // Create 8 orbiting circles
        for (let i = 0; i < 8; i++) {
            const circle = document.createElement('div');
            circle.className = 'orbiting-circle';

            // Different properties for each circle
            const size = 20 + (i * 15);
            const radius = 80 + (i * 60);
            const speed = 0.2 + (i * 0.05);
            const startAngle = (i * Math.PI * 2) / 8;

            circle.style.width = `${size}px`;
            circle.style.height = `${size}px`;
            circle.style.borderWidth = `${1 + (i * 0.3)}px`;

            let angle = startAngle;
            function animate() {
                angle += speed * 0.01;
                const x = centerX + Math.cos(angle) * radius;
                const y = centerY + Math.sin(angle) * radius;
                circle.style.left = `${x - size/2}px`;
                circle.style.top = `${y - size/2}px`;
                requestAnimationFrame(animate);
            }

            orbitContainer.appendChild(circle);
            animate();
        }

        // Disable scrolling
        document.body.style.overflow = 'hidden';
        window.addEventListener('scroll', () => window.scrollTo(0, 0));
    });
    </script>
    """)

    # Page structure - just the text container
    st.markdown("""
    <div class="center-container">
        <div class="main-text">LleY</div>
    </div>
    """, unsafe_allow_html=True)
# Debug: Show loaded secrets (remove after testing)

def esma():

    # Rest of your app...

    list_essay_type = [
        "Argumentative", "Persuasive", 'Explanatory', 'Descriptive',
        "Narrative", 'Cause and Effect', "Process Analysis",
        "Compare/Contrast", "Critique", "Definition", "General"
    ]

    list_level = ["Elementary", "Junior High", "Senior High", "Undergraduate", "Graduate", "Postgraduate", "PhD",
                  "Masters", "Doctorate"]
    list_speech_type = ["Casual", "Intimate", "Formal", "Frozen", "Consultative"]
    left, right = st.columns(2, vertical_alignment="top")

    languages = ["English (US)", "Filipino", "Hindi"]

    content_list_category = ["Facebook", "Youtube", "Tiktok", "Twitter/X", "Reddit", 'Instagram', "Spotify", ]
    content_list_content = ["Vlog", "Blog", "Written Post", "Podcast", "Music", "Article", ]
    content_list_complexity = ["Micro-Content", "Standard Content", "Premium Content", "Enterprise Content",
                               "Legacy Content", ]
    content_list_tiers = ["Beginner", "Intermediate", "Advanced", "Expert", ]
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
    condition_system = """You are EsMa. Strictly only write the requested essay content or content creation scripts. 
                        Do not write any other information. Meaning, only write paragraphs (unless user chose content creation). 
                        Also the output must have be clear and specific with no vague output"""


    # Main app interface
    def main():
        with st.container():
            left.subheader("EsMa by Elley")
            left.title("Your AI content generator")
            right.subheader("")
            right.title("")
        on = left.toggle("Activate Content Creation")
        if not on:
            with st.container():
                level_essay = left.selectbox("Type-Level", list_level)
                speech_type = left.selectbox("Type of Speech", list_speech_type)
                essay_type = left.selectbox("Essay Type", list_essay_type)
                speech = left.selectbox("Select Language", languages)
                word_num = left.slider("Select Number Words", min_value=0, max_value=1500, step=100)
                selected_pov = left.segmented_control('Point of View', ['First', 'Second', 'Third'],
                                                      selection_mode="single")

            with st.container():
                content_prompt = left.text_area("Prompt", "", height=150)
                other_info_prompt = left.text_area("Other Instructions", "", height=70)

                if st.button("Generate Essay"):
                    if content_prompt.strip() in ("", "Generated prompt"):
                        st.warning("Please enter a valid prompt")
                    else:
                        with st.spinner("Generating your essay..."):
                            full_prompt = f"Write a comprehensive {essay_type}, point of view: {selected_pov} point of view, education level: {level_essay}, language to use:{speech},  type of speech: {speech_type}, number of minimum words: {word_num}, essay about: {content_prompt}. With extra task {other_info_prompt}"
                            essay = ai_assistant(full_prompt, condition_system)
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
                selected_character = left.selectbox("Archetype", content_creator_types)
                word_num = left.slider("Select Number Words", min_value=0, max_value=1500, step=100)
                speech = left.segmented_control('Language', languages, selection_mode="single")

            with st.container():
                content_prompt = left.text_area("Prompt", "", height=150)
                other_info_prompt = left.text_area("Other Instructions", "", height=70)

                if st.button("Generate Essay"):
                    if content_prompt.strip() in ("", "Generated prompt"):
                        st.warning("Please enter a valid prompt")
                    else:
                        with st.spinner("Generating your essay..."):
                            full_prompt = f"""Write a content about: {content_prompt} in a language:{speech} , having a word length of: {word_num}, that will be posted or used in: {content_place}
                            having a content type: {content_type}, having a content complexity: {content_complexity}, having a content tier for: {content_tier}
                            and will portray a character: {selected_character}. With extra task {other_info_prompt}

"""
                            content_out = ai_assistant(full_prompt, condition_system)
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


def tetos():
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
                asyncio.run(text_to_speech(content_prompt, filename, voice_arranged))
                # Open the saved file and pass bytes to st.audio
                with open(filename, "rb") as f:
                    audio_bytes = f.read()
                st.audio(audio_bytes, format="audio/mpeg", loop=True)


def aito():


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
        response = ai_assistant(st.session_state.messages, rule=None)

        if response:
            # Add AI response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.chat_message("assistant").write(response)

def extract_pdf_text(pdf_file: str) -> str:
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        pdf_text = []
        for page in reader.pages:
            content = page.extract_text()
            if content:  # Only add if text was extracted
                pdf_text.append(content)
        return "\n".join(pdf_text) if pdf_text else "No text could be extracted from the PDF."
    except Exception as f:
        st.error(f"Error reading PDF: {str(f)}")
        return None

def extract_pptx_text(pptx_file):
    try:
        from pptx import Presentation
        prs = Presentation(pptx_file)
        text = []
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text.append(shape.text)
        return "\n".join(text) if text else "No text could be extracted from the PPTX."
    except ImportError:
        st.error("Please install python-pptx package: pip install python-pptx")
        return None
    except Exception as h:
        st.error(f"Error reading PPTX: {str(h)}")
        return None
def pdf2quiz():
    # System prompts for different quiz types
    system_condition_mcq = """You are a system only for creating a multiple choice quiz python dictionary. 
                        Return ONLY a properly formatted Python dictionary with no additional text or explanation.
                        Format:
                        {
                            "1": {
                                "question": "Question text",
                                "a": "Option A",
                                "b": "Option B",
                                "c": "Option C",
                                "d": "Option D",
                                "answer_key": "correct_letter"
                            },
                            ...
                        }"""

    system_condition_open = """You are a system only for creating an open-ended quiz python dictionary. 
                        Return ONLY a properly formatted Python dictionary with no additional text or explanation.
                        Format:
                        {
                            "1": {
                                "question": "Question text",
                                "type": "definition/enumeration/essay",
                                "model_answer": "The ideal answer that would score 10/10"
                            },
                            ...
                        }"""

    scoring_system = """You are an expert grader. Evaluate the student's answer based on the model answer.
                        Score each answer from 1-10 based on accuracy, completeness and relevance.
                        Provide a brief explanation for your scoring.
                        Return ONLY a Python dictionary with this format:
                        {
                            "score": x,
                            "explanation": "Brief explanation of the score"
                        }"""

    # Initialize session state
    if 'quiz' not in st.session_state:
        st.session_state.quiz = {
            'data': None,
            'answers': {},
            'submitted': False,
            'file_processed': None,
            'file_type': None,
            'quiz_type': 'multiple_choice'  # Default to multiple choice
        }

    st.title("File to Quiz Generator")
    st.subheader("Upload PDF or PPTX to generate a quiz")

    # Quiz type selection
    quiz_type = st.radio(
        "Quiz Type",
        options=["Multiple Choice", "Open-Ended (Definition/Enumeration/Essay)"],
        key="quiz_type_selector"
    )
    st.session_state.quiz['quiz_type'] = 'multiple_choice' if quiz_type == "Multiple Choice" else 'open_ended'

    # File uploader for both PDF and PPTX
    uploaded_file = st.file_uploader("Upload File", type=["pdf", "pptx"])

    # Toggle for custom prompt
    toggle_swap = st.toggle("Add Custom Prompt")
    extra_prompt = ""

    if toggle_swap:
        extra_prompt = st.text_area("Additional Instructions", "", height=150,
                                    help="Add any specific instructions for quiz generation")

    if uploaded_file:
        file_type = "PDF" if uploaded_file.name.endswith('.pdf') else "PPTX"
        st.write(f"Uploaded {file_type} file: {uploaded_file.name} ({uploaded_file.size / 1024:.2f} KB)")

        # Number of questions input
        number_quiz = st.number_input(
            "Number of questions to generate",
            min_value=1,
            max_value=100,
            value=5,
            help="Select how many quiz questions you want to generate from the file"
        )

        if st.button("Generate Quiz"):
            with st.spinner(f"Generating {quiz_type.lower()} quiz from {file_type}..."):
                # Save uploaded file to temp file
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name

                # Extract text based on file type
                if uploaded_file.name.endswith('.pdf'):
                    extracted_text = extract_pdf_text(tmp_file_path)
                else:
                    extracted_text = extract_pptx_text(tmp_file_path)

                if extracted_text and not extracted_text.startswith("No text"):
                    # Generate quiz from text
                    if st.session_state.quiz['quiz_type'] == 'multiple_choice':
                        full_prompt = f"""Create a multiple choice quiz based on the following text. 
                        Generate {number_quiz} good quality questions that test understanding of key concepts.
                        For each question, provide 4 plausible options (a-d) and indicate the correct answer.
                        Return ONLY the Python dictionary in the specified format. 
                        {extra_prompt if toggle_swap else ''}

                        Text content:
                        {extracted_text[:10000]}"""  # Limit to first 10k chars
                        system_prompt = system_condition_mcq
                    else:
                        full_prompt = f"""Create an open-ended quiz based on the following text. 
                        Generate {number_quiz} questions that require definition, enumeration, or essay answers.
                        For each question, provide a model answer that would score 10/10.
                        Return ONLY the Python dictionary in the specified format.
                        {extra_prompt if toggle_swap else ''}

                        Text content:
                        {extracted_text[:10000]}"""
                        system_prompt = system_condition_open

                    content_out = ai_assistant(full_prompt, system_prompt)

                    if content_out:
                        try:
                            # Clean the output
                            clean_output = content_out.strip()
                            if clean_output.startswith("```python"):
                                clean_output = clean_output[9:]
                            if clean_output.startswith("```"):
                                clean_output = clean_output[3:]
                            if clean_output.endswith("```"):
                                clean_output = clean_output[:-3]

                            # Convert to dictionary
                            quiz_data = ast.literal_eval(clean_output)

                            # Update session state
                            st.session_state.quiz = {
                                'data': quiz_data,
                                'answers': {q_num: None for q_num in quiz_data},
                                'submitted': False,
                                'file_processed': uploaded_file,
                                'file_type': file_type,
                                'quiz_type': st.session_state.quiz['quiz_type'],
                                'scores': {}
                            }
                            st.rerun()

                        except Exception as j:
                            st.error(f"Error processing quiz: {str(j)}")
                            st.text("Raw AI output:")
                            st.code(content_out)
                else:
                    st.warning(extracted_text or "Could not extract text from the file")

    # Display the quiz if generated
    if st.session_state.quiz['data']:
        st.subheader(
            f"{'Multiple Choice' if st.session_state.quiz['quiz_type'] == 'multiple_choice' else 'Open-Ended'} Quiz Generated from {st.session_state.quiz.get('file_type', 'Unknown Type')}")
        st.write(f"File: {st.session_state.quiz['file_processed'].name}")

        # Track if all questions have been answered
        all_answered = True

        for q_num, question in st.session_state.quiz['data'].items():
            st.markdown(f"**Question {q_num}**")
            st.write(question['question'])

            if st.session_state.quiz['quiz_type'] == 'multiple_choice':
                # Multiple choice interface
                options = [question['a'], question['b'], question['c'], question['d']]

                # Get current answer
                current_answer = st.session_state.quiz['answers'].get(q_num)

                # Show radio buttons
                user_choice = st.radio(
                    "Select your answer:",
                    options,
                    key=f"q_{q_num}",
                    index=options.index(current_answer) if current_answer in options else None
                )

                # Store answer if changed
                if user_choice and user_choice != current_answer:
                    st.session_state.quiz['answers'][q_num] = user_choice
                    st.rerun()
            else:
                # Open-ended interface
                current_answer = st.session_state.quiz['answers'].get(q_num, "")
                user_answer = st.text_area(
                    "Your answer:",
                    value=current_answer,
                    key=f"q_{q_num}",
                    height=150
                )

                # Store answer if changed
                if user_answer != current_answer:
                    st.session_state.quiz['answers'][q_num] = user_answer
                    st.rerun()

            # Check if all questions answered
            if st.session_state.quiz['answers'].get(q_num) is None:
                all_answered = False

            # Show feedback after submission
            if st.session_state.quiz['submitted']:
                if st.session_state.quiz['quiz_type'] == 'multiple_choice':
                    correct_answer = question[question['answer_key']]
                    if st.session_state.quiz['answers'][q_num] == correct_answer:
                        st.success("✓ Correct!")
                    else:
                        st.error(f"✗ Incorrect. The correct answer is: {correct_answer}")
                else:
                    if q_num in st.session_state.quiz.get('scores', {}):
                        score_data = st.session_state.quiz['scores'][q_num]
                        st.markdown(f"**Score: {score_data['score']}/10**")
                        st.markdown(f"**Explanation:** {score_data['explanation']}")
                        st.markdown("**Model Answer:**")
                        st.info(question['model_answer'])

        # Submit or Reset buttons
        col1, col2 = st.columns(2)
        with col1:
            if not st.session_state.quiz['submitted']:
                if st.button("Submit Answers", disabled=not all_answered):
                    if st.session_state.quiz['quiz_type'] == 'open_ended':
                        # For open-ended questions, we need to score each answer
                        with st.spinner("Evaluating your answers..."):
                            scores = {}
                            for q_num, question in st.session_state.quiz['data'].items():
                                user_answer = st.session_state.quiz['answers'][q_num]
                                prompt = f"""
                                Model Answer: {question['model_answer']}
                                Student Answer: {user_answer}

                                Evaluate the student's answer based on the model answer.
                                Score from 1-10 based on accuracy, completeness and relevance.
                                Provide a brief explanation for your scoring.
                                """
                                score_data = ai_assistant(prompt, scoring_system)
                                try:
                                    scores[q_num] = ast.literal_eval(score_data.strip())
                                except:
                                    scores[q_num] = {"score": 0, "explanation": "Could not evaluate this answer"}
                            st.session_state.quiz['scores'] = scores

                    st.session_state.quiz['submitted'] = True
                    st.rerun()
        with col2:
            if st.button("Reset Quiz"):
                st.session_state.quiz = {
                    'data': None,
                    'answers': {},
                    'submitted': False,
                    'file_processed': None,
                    'file_type': None,
                    'quiz_type': 'multiple_choice',
                    'scores': {}
                }
                st.rerun()

        # Calculate and display score if submitted
        if st.session_state.quiz['submitted']:
            if st.session_state.quiz['quiz_type'] == 'multiple_choice':
                score = sum(
                    1 for q_num, question in st.session_state.quiz['data'].items()
                    if st.session_state.quiz['answers'][q_num] == question[question['answer_key']]
                )
                st.success(f"Your score: {score}/{len(st.session_state.quiz['data'])}")
            else:
                total_score = sum(
                    score_data['score'] for score_data in st.session_state.quiz['scores'].values()
                )
                max_score = 10 * len(st.session_state.quiz['data'])
                st.success(f"Your total score: {total_score}/{max_score} ({round(total_score / max_score * 100, 1)}%)")


def extract_text_from_file(uploaded_file):
    """Extract text from uploaded file based on its type."""
    text = ""
    try:
        if uploaded_file.name.endswith('.pdf'):
            reader = PyPDF2.PdfReader(uploaded_file)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        elif uploaded_file.name.endswith('.docx'):
            doc = Document(uploaded_file)
            text = "\n".join([para.text for para in doc.paragraphs])
        elif uploaded_file.name.endswith('.txt'):
            text = uploaded_file.read().decode('utf-8')
        elif uploaded_file.name.endswith('.pptx'):
            prs = Presentation(uploaded_file)
            text = "\n".join([shape.text for slide in prs.slides for shape in slide.shapes if hasattr(shape, "text")])
    except Exception as e:
        st.error(f"Error extracting text: {str(e)}")
    return text


def turnitin_knockoff():
    # ... [previous code remains the same until the AI Detection section]

    # Enhanced AI Detection Analysis with Comprehensive Metrics
    st.subheader("🔍 AI Similarity Check")
    st.markdown("""
            <style>
                .metric-box {
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    padding: 15px;
                    margin-bottom: 15px;
                    background-color: #f9f9f9;
                }
                .metric-title {
                    font-weight: bold;
                    margin-bottom: 5px;
                }
                .source-link {
                    color: #0066cc;
                    text-decoration: underline;
                }
            </style>
            """, unsafe_allow_html=True)

    try:
        ai_prompt = f"""Analyze the following text comprehensively to determine AI-generation likelihood:
                {text[:analysis_depth]}

                Calculate an overall AI similarity percentage (0-100%) based on these measurable linguistic features:
                1. Perplexity (predictability of word choices)
                2. Burstiness (variation in sentence structure)
                3. Syntactic Uniformity (grammatical pattern consistency)
                4. Repetition (frequency of repeated phrases)

                For each feature:
                - Score between 0-100 (higher = more AI-like)
                - Explanation with specific examples from text
                - Typical human vs AI ranges
                - Weight in final calculation (perplexity: 30%, burstiness: 25%, 
                  syntactic uniformity: 25%, repetition: 20%)

                Also identify:
                - Specific passages most likely AI-generated
                - Similar online sources with clickable URLs
                - Supporting research references

                Return ONLY this JSON structure:
                {{
                    "overall_ai_score": 0-100,
                    "confidence": 0-100,
                    "limitations": "string",
                    "metrics": {{
                        "perplexity": {{
                            "score": 0-100,
                            "explanation": "string",
                            "human_range": "string",
                            "ai_range": "string",
                            "examples": ["string"],
                            "weight": 0.3
                        }},
                        "burstiness": {{
                            "score": 0-100,
                            "explanation": "string",
                            "human_range": "string",
                            "ai_range": "string",
                            "examples": ["string"],
                            "weight": 0.25
                        }},
                        "syntactic_uniformity": {{
                            "score": 0-100,
                            "explanation": "string",
                            "human_range": "string",
                            "ai_range": "string",
                            "examples": ["string"],
                            "weight": 0.25
                        }},
                        "repetition": {{
                            "score": 0-100,
                            "explanation": "string",
                            "human_range": "string",
                            "ai_range": "string",
                            "examples": ["string"],
                            "weight": 0.2
                        }}
                    }},
                    "flagged_passages": [
                        {{
                            "text": "string",
                            "score": 0-100,
                            "reason": "string",
                            "sources": [
                                {{
                                    "url": "string",
                                    "similarity": 0-100,
                                    "type": "AI|human"
                                }}
                            ]
                        }}
                    ],
                    "research_references": [
                        {{
                            "title": "string",
                            "url": "string",
                            "author": "string",
                            "year": number
                        }}
                    ],
                    "calculation_note": "string"
                }}"""

        ai_result = ai_assistant(ai_prompt, """You are an advanced AI detection system. Your analysis must:
                1. Use only measurable linguistic features
                2. Show exact calculation method
                3. Provide specific text examples
                4. Include verifiable sources
                5. Make all URLs complete and clickable
                Return ONLY valid JSON.""")

        if not ai_result:
            raise ValueError("No response received from AI assistant")

        try:
            ai_data = ast.literal_eval(ai_result)

            # Validation
            required = ["overall_ai_score", "confidence", "metrics", "flagged_passages"]
            if not all(field in ai_data for field in required):
                raise ValueError("Missing required fields in response")

            # Display Main Results
            st.markdown(f"""
                    <div class="metric-box">
                        <div class="metric-title">Overall AI Similarity Score</div>
                        <h2>{ai_data['overall_ai_score']}%</h2>
                        <div>Confidence: {ai_data['confidence']}%</div>
                        <div><small>{ai_data.get('calculation_note', '')}</small></div>
                    </div>
                    """, unsafe_allow_html=True)

            # Detailed Metrics Section
            with st.expander("Detailed Analysis Metrics", expanded=True):
                cols = st.columns(4)
                metrics = ai_data["metrics"]

                with cols[0]:
                    st.markdown(f"""
                            <div class="metric-box">
                                <div class="metric-title">Perplexity</div>
                                <h3>{metrics['perplexity']['score']}%</h3>
                                <div><small>Human: {metrics['perplexity']['human_range']}</small></div>
                                <div><small>AI: {metrics['perplexity']['ai_range']}</small></div>
                            </div>
                            """, unsafe_allow_html=True)
                    with st.popover("ℹ️ Details"):
                        st.write(metrics['perplexity']['explanation'])
                        st.write("Examples:")
                        for ex in metrics['perplexity']['examples'][:2]:
                            st.code(ex)

                with cols[1]:
                    st.markdown(f"""
                            <div class="metric-box">
                                <div class="metric-title">Burstiness</div>
                                <h3>{metrics['burstiness']['score']}%</h3>
                                <div><small>Human: {metrics['burstiness']['human_range']}</small></div>
                                <div><small>AI: {metrics['burstiness']['ai_range']}</small></div>
                            </div>
                            """, unsafe_allow_html=True)
                    with st.popover("ℹ️ Details"):
                        st.write(metrics['burstiness']['explanation'])
                        st.write("Examples:")
                        for ex in metrics['burstiness']['examples'][:2]:
                            st.code(ex)

                with cols[2]:
                    st.markdown(f"""
                            <div class="metric-box">
                                <div class="metric-title">Syntactic Uniformity</div>
                                <h3>{metrics['syntactic_uniformity']['score']}%</h3>
                                <div><small>Human: {metrics['syntactic_uniformity']['human_range']}</small></div>
                                <div><small>AI: {metrics['syntactic_uniformity']['ai_range']}</small></div>
                            </div>
                            """, unsafe_allow_html=True)
                    with st.popover("ℹ️ Details"):
                        st.write(metrics['syntactic_uniformity']['explanation'])
                        st.write("Examples:")
                        for ex in metrics['syntactic_uniformity']['examples'][:2]:
                            st.code(ex)

                with cols[3]:
                    st.markdown(f"""
                            <div class="metric-box">
                                <div class="metric-title">Repetition</div>
                                <h3>{metrics['repetition']['score']}%</h3>
                                <div><small>Human: {metrics['repetition']['human_range']}</small></div>
                                <div><small>AI: {metrics['repetition']['ai_range']}</small></div>
                            </div>
                            """, unsafe_allow_html=True)
                    with st.popover("ℹ️ Details"):
                        st.write(metrics['repetition']['explanation'])
                        st.write("Examples:")
                        for ex in metrics['repetition']['examples'][:2]:
                            st.code(ex)

            # Flagged Passages with Clickable Links
            with st.expander("Flagged Passages & Similar Sources"):
                for passage in ai_data["flagged_passages"]:
                    st.markdown(f"""
                            <div style="border-left: 3px solid #ff6b6b; padding-left: 10px; margin: 10px 0;">
                                <div style="font-weight: bold;">AI Likelihood: {passage['score']}%</div>
                                <code>{passage['text']}</code>
                                <div><small>Reason: {passage['reason']}</small></div>
                            </div>
                            """, unsafe_allow_html=True)

                    if passage.get("sources"):
                        st.markdown("**Similar Sources:**")
                        for source in passage["sources"]:
                            if source.get("url"):
                                st.markdown(
                                    f"- <a href='{source['url']}' class='source-link' target='_blank'>{source['url']}</a> "
                                    f"(Similarity: {source['similarity']}%, "
                                    f"Type: {source['type']})",
                                    unsafe_allow_html=True
                                )
                            else:
                                st.markdown(
                                    f"- Similar content found (Similarity: {source['similarity']}%, "
                                    f"Type: {source['type']})"
                                )
                    st.markdown("---")

            # Research References with Clickable Links
            if ai_data.get("research_references"):
                with st.expander("Supporting Research"):
                    for ref in ai_data["research_references"]:
                        if ref.get("url"):
                            st.markdown(
                                f"- <a href='{ref['url']}' class='source-link' target='_blank'>{ref['title']}</a> "
                                f"({ref['author']}, {ref['year']})",
                                unsafe_allow_html=True
                            )
                        else:
                            st.markdown(f"- {ref['title']} ({ref['author']}, {ref['year']})")

            # Limitations
            st.markdown(f"""
                    <div style="background-color: #fff3cd; padding: 10px; border-radius: 5px; margin-top: 20px;">
                        <strong>⚠️ Analysis Limitations:</strong> {ai_data.get('limitations', 'None specified')}
                    </div>
                    """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error processing analysis: {str(e)}")
            st.text_area("Raw AI Response", value=ai_result, height=200)

    except Exception as e:
        st.error(f"AI detection failed: {str(e)}")

    # ... [rest of the function remains the same]
    # ... [rest of the function remains the same]
# from bs4 import BeautifulSoup
# from docx import Document
# import python_pptx


# Add to your pages dictionary


def about():
    st.title("About")

pages={ "Tools": [st.Page(main_page, title="Home"), st.Page(aito, title="AITO"),
                  st.Page(esma, title="Essay Maker"),
                  st.Page(tetos, title="Text To Speech"),
                  st.Page(pdf2quiz, title="Pdf To Quiz"),
                  st.Page(turnitin_knockoff, title="Originality Checker"),],
        "About": [st.Page(about, title="About")],

        }
pg = st.navigation(pages)
pg.run()


