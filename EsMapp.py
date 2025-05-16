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
# Initialize the OpenAI client with proper configuration

st.set_page_config(
    page_title="Lley",
    page_icon=":writing_hand:",
    layout="wide"
)
st.logo("final logo 2.png", icon_image="enlarge 1.png", size = "large")
def main_page():
    st.markdown("""
    <style>
        /* Disable all scrolling */
        html, body, .stApp {
            overflow: hidden !important;
            height: 100vh !important;
            width: 100vw !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        /* Main container - fills entire viewport */
        .static-container {
            height: 100vh;
            width: 100vw;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: #000000;
            position: fixed;
            top: 0;
            left: 0;
        }

        /* Name styling */
        .name {
            font-family: 'Arial Black', sans-serif;
            font-size: 8rem;
            font-weight: 900;
            color: white;
            text-align: center;
            margin: 0;
            padding: 0;
            text-transform: uppercase;
            letter-spacing: 0.5rem;
        }

        /* Simple underline animation */
        .underline {
            height: 4px;
            width: 0;
            background: white;
            margin: 1rem auto;
            animation: expand 2s ease-out forwards;
            animation-delay: 0.5s;
        }

        @keyframes expand {
            from { width: 0; }
            to { width: 80%; }
        }

        /* Subtle footer - absolutely positioned */
        .footer {
            position: absolute;
            bottom: 2rem;
            color: rgba(255,255,255,0.5);
            font-size: 0.8rem;
            letter-spacing: 0.1rem;
        }

        /* Responsive adjustments */
        @media (max-width: 768px) {
            .name {
                font-size: 3rem;
                letter-spacing: 0.2rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # JavaScript to ensure no scrolling can occur
    html("""
    <script>
        // Lock scroll position on load
        document.addEventListener('DOMContentLoaded', function() {
            window.scrollTo(0, 0);
            document.body.style.overflow = 'hidden';
        });

        // Prevent any scrolling attempts
        document.addEventListener('scroll', function(e) {
            window.scrollTo(0, 0);
        });

        // Prevent touch scrolling on mobile
        document.addEventListener('touchmove', function(e) {
            e.preventDefault();
        }, { passive: false });
    </script>
    """)

    # Static content - just the name
    st.markdown("""
    <div class="static-container">
        <h1 class="name">Lley</h1>
        <div class="underline"></div>
        <div class="footer">EST. 2025</div>
    </div>
    """, unsafe_allow_html=True)

    # JavaScript for additional effects
    def add_js():
        html("""
        <script>
        // Mouse move parallax effect
        document.addEventListener('mousemove', function(e) {
            const letters = document.querySelectorAll('.letter');
            const x = e.clientX / window.innerWidth;
            const y = e.clientY / window.innerHeight;

            letters.forEach((letter, index) => {
                const offset = (index + 1) * 10;
                letter.style.transform = `translate(${(x - 0.5) * offset}px, ${(y - 0.5) * offset}px)`;
            });
        });

        // Click ripple effect
        document.addEventListener('click', function(e) {
            const ripple = document.createElement('div');
            ripple.style.position = 'absolute';
            ripple.style.width = '20px';
            ripple.style.height = '20px';
            ripple.style.backgroundColor = 'rgba(255, 255, 255, 0.5)';
            ripple.style.borderRadius = '50%';
            ripple.style.pointerEvents = 'none';
            ripple.style.left = `${e.clientX - 10}px`;
            ripple.style.top = `${e.clientY - 10}px`;
            ripple.style.transform = 'scale(0)';

            document.body.appendChild(ripple);

            setTimeout(() => {
                ripple.style.transition = 'transform 0.5s ease-out, opacity 0.5s ease-out';
                ripple.style.transform = 'scale(20)';
                ripple.style.opacity = '0';

                setTimeout(() => {
                    ripple.remove();
                }, 500);
            }, 10);
        });
        </script>
        """)

    add_js()

    # Main content - just the name with animated letters
    st.markdown("""
    <div class="main-container">
        <h1 class="name">
            <span class="letter l1">L</span>
            <span class="letter l2">L</span>
            <span class="letter e">e</span>
            <span class="letter y">y</span>
        </h1>
        <div class="footer">experience the future</div>
    </div>
    """, unsafe_allow_html=True)



# Debug: Show loaded secrets (remove after testing)

def esma():
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


def pdf2quiz():
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
        except Exception as d:
            st.error(f"Error reading PPTX: {str(d)}")
            return None

    def ai_assistant(prompt):
        try:
            response = client.chat.completions.create(
                model="nousresearch/deephermes-3-mistral-24b-preview:free",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a system only for creating a quiz python dictionary. 
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
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=20000,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as det:
            st.error(f"Failed to generate quiz: {str(det)}")
            return None

    # Initialize session state
    if 'quiz' not in st.session_state:
        st.session_state.quiz = {
            'data': None,
            'answers': {},
            'submitted': False,
            'file_processed': None,
            'file_type': None
        }

    st.title("File to Quiz Generator")
    st.subheader("Upload PDF or PPTX to generate a quiz")

    # File uploader for both PDF and PPTX
    uploaded_file = st.file_uploader("Upload File", type=["pdf", "pptx"])

    if uploaded_file:
        # Display file info
        file_type = "PDF" if uploaded_file.name.endswith('.pdf') else "PPTX"
        st.write(f"Uploaded {file_type} file: {uploaded_file.name} ({uploaded_file.size / 1024:.2f} KB)")

        # Number of questions input
        number_quiz = st.number_input(
            "Number of questions to generate", min_value=1, max_value=100,value=5,help="Select how many quiz questions you want to generate from the file")

        if st.button("Generate Quiz"):
            with st.spinner(f"Generating quiz from {file_type}..."):
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
                    full_prompt = f"""Create a multiple choice quiz based on the following text. 
                    Generate {number_quiz} good quality questions that test understanding of key concepts.
                    For each question, provide 4 plausible options (a-d) and indicate the correct answer.
                    Return ONLY the Python dictionary in the specified format.

                    Text content:
                    {extracted_text[:10000]}"""  # Limit to first 10k chars

                    content_out = ai_assistant(full_prompt)

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
                                'file_type': file_type
                            }
                            st.rerun()

                        except Exception as e:
                            st.error(f"Error processing quiz: {str(e)}")
                            st.text("Raw AI output:")
                            st.code(content_out)
                else:
                    st.warning(extracted_text or "Could not extract text from the file")

    # Display the quiz if generated
    if st.session_state.quiz['data']:
        st.subheader(f"Quiz Generated from {st.session_state.quiz.get('file_type', 'Unknown Type')}")

        st.write(f"File: {st.session_state.quiz['file_processed'].name}")

        # Track if all questions have been answered
        all_answered = True

        for q_num, question in st.session_state.quiz['data'].items():
            st.markdown(f"**Question {q_num}**")
            st.write(question['question'])

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

            # Check if all questions answered
            if st.session_state.quiz['answers'].get(q_num) is None:
                all_answered = False

            # Show feedback after submission
            if st.session_state.quiz['submitted']:
                correct_answer = question[question['answer_key']]
                if st.session_state.quiz['answers'][q_num] == correct_answer:
                    st.success("✓ Correct!")
                else:
                    st.error(f"✗ Incorrect. The correct answer is: {correct_answer}")

        # Submit or Reset buttons
        col1, col2 = st.columns(2)
        with col1:
            if not st.session_state.quiz['submitted']:
                if st.button("Submit Answers", disabled=not all_answered):
                    st.session_state.quiz['submitted'] = True
                    st.rerun()
        with col2:
            if st.button("Reset Quiz"):
                st.session_state.quiz = {
                    'data': None,
                    'answers': {},
                    'submitted': False,
                    'file_processed': None,
                    'file_type': None
                }
                st.rerun()

        # Calculate and display score if submitted
        if st.session_state.quiz['submitted']:
            score = sum(
                1 for q_num, question in st.session_state.quiz['data'].items()
                if st.session_state.quiz['answers'][q_num] == question[question['answer_key']]
            )
            st.success(f"Your score: {score}/{len(st.session_state.quiz['data'])}")

def about():
    st.title("About")

pages={ "Tools": [st.Page(main_page, title="Home"), st.Page(aito, title="AITO"),
                  st.Page(esma, title="Essay Maker"),
                  st.Page(tetos, title="Text To Speech"),
                  st.Page(pdf2quiz, title="Pdf To Quiz")],
        "About": [st.Page(about, title="About")],

        }
pg = st.navigation(pages)
pg.run()


