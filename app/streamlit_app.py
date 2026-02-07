import streamlit as st
import sys
import os
import io
import base64
from pathlib import Path

# Ensure app is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.graph.graph import app
from app.utils.logger import logger
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS
import streamlit.components.v1 as components

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Amaury Rammanat | CV IA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════
# 📸 CHARGEMENT DE VOTRE PHOTO
# ═══════════════════════════════════════════════════════════════
def get_base64_image(image_path):
    """Convertit une image locale en base64."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

PHOTO_PATH = Path(__file__).parent / "assets" / "photo_amaury.jpg .png"
PHOTO_BASE64 = get_base64_image(PHOTO_PATH)

if PHOTO_BASE64:
    PHOTO_SRC = f"data:image/png;base64,{PHOTO_BASE64}"
else:
    PHOTO_SRC = "https://ui-avatars.com/api/?name=Amaury+Rammanat&size=200&background=667eea&color=fff&bold=true&rounded=true"

# ═══════════════════════════════════════════════════════════════
# 🎨 CSS COMPLET — RAINBOW BORDER SANS HALO
# ═══════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
    /* ══════════════════════════════════════════════════════════
       🌈 ANIMATIONS
    ══════════════════════════════════════════════════════════ */
    @property --angle {{
        syntax: "<angle>";
        initial-value: 0deg;
        inherits: false;
    }}

    @keyframes apple-spin {{
        to {{ --angle: 360deg; }}
    }}

    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-8px); }}
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes border-dance {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    /* ══════════════════════════════════════════════════════════
       🖼️ BACKGROUND
    ══════════════════════════════════════════════════════════ */
    .stApp {{
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
        background-attachment: fixed;
    }}

    .stApp::before {{
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background:
            radial-gradient(circle at 20% 20%, rgba(102, 126, 234, 0.12) 0%, transparent 40%),
            radial-gradient(circle at 80% 80%, rgba(118, 75, 162, 0.12) 0%, transparent 40%),
            radial-gradient(circle at 50% 50%, rgba(240, 147, 251, 0.06) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }}

    /* ══════════════════════════════════════════════════════════
       👤 AVATAR CHAT — RAINBOW BORDER SANS HALO
    ══════════════════════════════════════════════════════════ */
    .chat-avatar-wrapper {{
        position: relative;
        width: 48px;
        height: 48px;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .chat-avatar-wrapper::before {{
        content: '';
        position: absolute;
        inset: -2px;
        border-radius: 50%;
        background: conic-gradient(
            from var(--angle, 0deg),
            #f06292, #ba68c8, #7e57c2, #5c6bc0,
            #42a5f5, #26c6da, #66bb6a, #ffee58,
            #ffa726, #ef5350, #f06292
        );
        -webkit-mask:
            radial-gradient(farthest-side, transparent calc(100% - 2px), #fff calc(100% - 2px));
        mask:
            radial-gradient(farthest-side, transparent calc(100% - 2px), #fff calc(100% - 2px));
        animation: apple-spin 4s linear infinite;
        z-index: 1;
    }}

    .chat-avatar {{
        width: 100%;
        height: 100%;
        border-radius: 50%;
        object-fit: cover;
        position: relative;
        z-index: 2;
        background: #1a1a2e;
    }}

    /* ══════════════════════════════════════════════════════════
       👤 PROFILE HEADER — GRANDE PHOTO RAINBOW BORDER
    ══════════════════════════════════════════════════════════ */
    .profile-wrapper {{
        position: relative;
        width: 156px;
        height: 156px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
    }}

    .profile-wrapper::before {{
        content: '';
        position: absolute;
        inset: -4px;
        border-radius: 50%;
        background: conic-gradient(
            from var(--angle, 0deg),
            #f06292, #ba68c8, #7e57c2, #5c6bc0,
            #42a5f5, #26c6da, #66bb6a, #ffee58,
            #ffa726, #ef5350, #f06292
        );
        -webkit-mask:
            radial-gradient(farthest-side, transparent calc(100% - 4px), #fff calc(100% - 4px));
        mask:
            radial-gradient(farthest-side, transparent calc(100% - 4px), #fff calc(100% - 4px));
        animation: apple-spin 5s linear infinite;
        z-index: 1;
    }}

    .profile-photo {{
        width: 100%;
        height: 100%;
        border-radius: 50%;
        object-fit: cover;
        position: relative;
        z-index: 2;
        background: #1a1a2e;
    }}

    /* ══════════════════════════════════════════════════════════
       👤 SIDEBAR PHOTO — PETITE RAINBOW BORDER
    ══════════════════════════════════════════════════════════ */
    .profile-wrapper-small {{
        position: relative;
        width: 106px;
        height: 106px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
    }}

    .profile-wrapper-small::before {{
        content: '';
        position: absolute;
        inset: -3px;
        border-radius: 50%;
        background: conic-gradient(
            from var(--angle, 0deg),
            #f06292, #ba68c8, #7e57c2, #5c6bc0,
            #42a5f5, #26c6da, #66bb6a, #ffee58,
            #ffa726, #ef5350, #f06292
        );
        -webkit-mask:
            radial-gradient(farthest-side, transparent calc(100% - 3px), #fff calc(100% - 3px));
        mask:
            radial-gradient(farthest-side, transparent calc(100% - 3px), #fff calc(100% - 3px));
        animation: apple-spin 5s linear infinite;
        z-index: 1;
    }}

    .profile-photo-small {{
        width: 100%;
        height: 100%;
        border-radius: 50%;
        object-fit: cover;
        position: relative;
        z-index: 2;
        background: #1a1a2e;
    }}

    /* ══════════════════════════════════════════════════════════
       💬 MESSAGES CHAT — RAINBOW BORDER SANS HALO
    ══════════════════════════════════════════════════════════ */
    .custom-chat-message {{
        display: flex;
        gap: 15px;
        padding: 22px;
        margin: 14px 0;
        border-radius: 22px;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        animation: fadeIn 0.4s ease;
        position: relative;
    }}

    /* ── Assistant message ── */
    .chat-message-assistant {{
        background: rgba(255, 255, 255, 0.04);
        border: none;
        position: relative;
        z-index: 1;
    }}

    .chat-message-assistant::before {{
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 22px;
        padding: 2px;
        background: conic-gradient(
            from var(--angle, 0deg),
            #f06292, #ba68c8, #7e57c2, #5c6bc0,
            #42a5f5, #26c6da, #66bb6a, #ffee58,
            #ffa726, #ef5350, #f06292
        );
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        animation: apple-spin 6s linear infinite;
        z-index: -1;
        pointer-events: none;
    }}

    /* ── User message ── */
    .chat-message-user {{
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.12), rgba(118, 75, 162, 0.12));
        border: none;
        flex-direction: row-reverse;
        position: relative;
        z-index: 1;
    }}

    .chat-message-user::before {{
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 22px;
        padding: 2px;
        background: conic-gradient(
            from var(--angle, 0deg),
            #667eea, #764ba2, #f093fb, #c471f5,
            #667eea, #764ba2, #f093fb
        );
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        animation: apple-spin 6s linear infinite;
        z-index: -1;
        pointer-events: none;
    }}

    .chat-message-user .chat-content {{
        text-align: right;
    }}

    .chat-content {{
        flex: 1;
        color: rgba(255, 255, 255, 0.9);
        line-height: 1.7;
    }}

    .chat-content p {{
        margin: 0 0 10px 0;
    }}

    .chat-content ul, .chat-content ol {{
        margin: 10px 0;
        padding-left: 20px;
    }}

    .chat-content li {{
        margin: 5px 0;
    }}

    .chat-content strong {{
        color: #c4b5fd;
    }}

    .chat-content code {{
        background: rgba(102, 126, 234, 0.2);
        padding: 2px 6px;
        border-radius: 4px;
        font-family: 'Fira Code', monospace;
    }}

    /* ══════════════════════════════════════════════════════════
       🪟 GLASSMORPHISM
    ══════════════════════════════════════════════════════════ */
    .glass-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        transition: all 0.4s ease;
    }}

    .glass-card:hover {{
        transform: translateY(-5px);
        border-color: rgba(255, 255, 255, 0.2);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
    }}

    /* ══════════════════════════════════════════════════════════
       📝 HEADER — RAINBOW TOP LINE
    ══════════════════════════════════════════════════════════ */
    .main-header {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border-radius: 30px;
        padding: 35px 40px;
        margin-bottom: 30px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        position: relative;
        overflow: hidden;
    }}

    .main-header::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(
            90deg,
            #f06292, #ba68c8, #7e57c2, #5c6bc0,
            #42a5f5, #26c6da, #66bb6a, #ffee58,
            #ffa726, #ef5350, #f06292
        );
        background-size: 300% 100%;
        animation: border-dance 5s ease infinite;
    }}

    .header-content {{
        display: flex;
        align-items: center;
        gap: 35px;
        flex-wrap: wrap;
    }}

    .header-text h1 {{
        color: white;
        font-size: 2.4rem;
        font-weight: 700;
        margin: 0 0 10px 0;
        background: linear-gradient(135deg, #ffffff 0%, #c9d6ff 50%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}

    .header-text p {{
        color: rgba(255, 255, 255, 0.75);
        font-size: 1.15rem;
        margin: 0;
    }}

    .status-badge {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, #00c853, #00e676);
        color: white;
        padding: 10px 22px;
        border-radius: 50px;
        font-size: 0.95rem;
        font-weight: 600;
        margin-top: 15px;
        box-shadow: 0 4px 20px rgba(0, 200, 83, 0.35);
        animation: float 3s ease-in-out infinite;
    }}

    /* ══════════════════════════════════════════════════════════
       📊 INFO GRID
    ══════════════════════════════════════════════════════════ */
    .info-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
        margin: 25px 0;
    }}

    .info-item {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.06);
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}

    .info-item::before {{
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }}

    .info-item:hover::before {{
        transform: scaleX(1);
    }}

    .info-item:hover {{
        transform: translateY(-8px);
        border-color: rgba(102, 126, 234, 0.3);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.25);
    }}

    .info-icon {{
        font-size: 2rem;
        margin-bottom: 12px;
        display: block;
    }}

    .info-label {{
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 8px;
    }}

    .info-value {{
        color: white;
        font-size: 1.05rem;
        font-weight: 500;
    }}

    .info-value a {{
        color: #a78bfa;
        text-decoration: none;
        transition: all 0.3s;
    }}

    .info-value a:hover {{
        color: #c4b5fd;
        text-shadow: 0 0 10px rgba(167, 139, 250, 0.5);
    }}

    /* ══════════════════════════════════════════════════════════
       💬 CACHER LES MESSAGES STREAMLIT PAR DÉFAUT
    ══════════════════════════════════════════════════════════ */
    [data-testid="stChatMessage"] {{
        display: none !important;
    }}

    /* ══════════════════════════════════════════════════════════
       📝 CHAT INPUT — RAINBOW BORDER ANIMÉE
       On entoure le conteneur d'un wrapper rainbow
    ══════════════════════════════════════════════════════════ */

    /* Conteneur bottom (fixed) du chat input */
    [data-testid="stBottom"] > div {{
        background: transparent !important;
    }}

    /* Le wrapper principal du chat input */
    .stChatInput {{
        position: relative !important;
        z-index: 1 !important;
    }}

    .stChatInput > div {{
        background: rgba(15, 15, 30, 0.9) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: none !important;
        border-radius: 25px !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        z-index: 2 !important;
    }}

    /* Rainbow border via un wrapper qu'on simule avec box-shadow + outline trick */
    /* Technique : on utilise un outline + gradient via pseudo-element sur le parent */

    .stChatInput {{
        position: relative !important;
        padding: 2px !important;
        border-radius: 27px !important;
        background: conic-gradient(
            from var(--angle, 0deg),
            #f06292, #ba68c8, #7e57c2, #5c6bc0,
            #42a5f5, #26c6da, #66bb6a, #ffee58,
            #ffa726, #ef5350, #f06292
        ) !important;
        animation: apple-spin 4s linear infinite !important;
    }}

    .stChatInput > div {{
        border-radius: 25px !important;
    }}

    .stChatInput input {{
        color: white !important;
    }}

    .stChatInput input::placeholder {{
        color: rgba(255, 255, 255, 0.4) !important;
    }}

    .stChatInput button {{
        color: white !important;
    }}

    /* ══════════════════════════════════════════════════════════
       📱 SIDEBAR
    ══════════════════════════════════════════════════════════ */
    [data-testid="stSidebar"] {{
        background: rgba(15, 15, 30, 0.95) !important;
        backdrop-filter: blur(30px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }}

    [data-testid="stSidebar"] > div:first-child {{
        background: transparent !important;
    }}

    .sidebar-title {{
        text-align: center;
        margin: 20px 0;
        font-size: 1.2rem;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    /* ══════════════════════════════════════════════════════════
       🔘 BUTTONS
    ══════════════════════════════════════════════════════════ */
    .stButton > button {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 12px 25px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.35) !important;
    }}

    .stButton > button:hover {{
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.45) !important;
    }}

    /* ══════════════════════════════════════════════════════════
       📋 EXPANDERS
    ══════════════════════════════════════════════════════════ */
    .streamlit-expanderHeader {{
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: white !important;
    }}

    .streamlit-expanderContent {{
        background: rgba(255, 255, 255, 0.02) !important;
        border-radius: 0 0 15px 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-top: none !important;
    }}

    /* ══════════════════════════════════════════════════════════
       🎯 SUGGESTION CARDS
    ══════════════════════════════════════════════════════════ */
    .suggestion-card {{
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.06);
        transition: all 0.3s ease;
        height: 100%;
    }}

    .suggestion-card:hover {{
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(102, 126, 234, 0.3);
        transform: translateY(-5px);
    }}

    .suggestion-card h4 {{
        color: #a78bfa;
        margin-bottom: 15px;
        font-size: 1.1rem;
    }}

    .suggestion-card ul {{
        list-style: none;
        padding: 0;
        margin: 0;
    }}

    .suggestion-card li {{
        color: rgba(255, 255, 255, 0.75);
        padding: 8px 0;
        transition: all 0.2s;
        padding-left: 5px;
        border-radius: 8px;
    }}

    .suggestion-card li:hover {{
        color: #c4b5fd;
        background: rgba(102, 126, 234, 0.1);
        padding-left: 12px;
    }}

    /* ══════════════════════════════════════════════════════════
       🔊 AUDIO
    ══════════════════════════════════════════════════════════ */
    .audio-container {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border-radius: 15px;
        padding: 12px;
        margin-top: 10px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }}

    /* ══════════════════════════════════════════════════════════
       ✨ SKILL TAGS
    ══════════════════════════════════════════════════════════ */
    .skill-tag {{
        display: inline-block;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
        padding: 6px 14px;
        border-radius: 50px;
        margin: 4px;
        font-size: 0.85rem;
        color: white;
        border: 1px solid rgba(102, 126, 234, 0.2);
        transition: all 0.3s ease;
    }}

    .skill-tag:hover {{
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }}

    /* ══════════════════════════════════════════════════════════
       📱 RESPONSIVE
    ══════════════════════════════════════════════════════════ */
    @media (max-width: 768px) {{
        .header-content {{
            flex-direction: column;
            text-align: center;
        }}

        .header-text h1 {{
            font-size: 1.8rem;
        }}

        .custom-chat-message {{
            flex-direction: column !important;
            align-items: flex-start;
        }}

        .chat-message-user {{
            align-items: flex-end;
        }}

        .chat-message-user .chat-content {{
            text-align: left;
        }}
    }}

    /* ══════════════════════════════════════════════════════════
       🎨 MISC
    ══════════════════════════════════════════════════════════ */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    ::-webkit-scrollbar {{
        width: 8px;
    }}

    ::-webkit-scrollbar-track {{
        background: rgba(255, 255, 255, 0.02);
    }}

    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }}

    .stMarkdown, .stText, p, span, li {{
        color: rgba(255, 255, 255, 0.85) !important;
    }}

    h1, h2, h3, h4, h5, h6 {{
        color: white !important;
    }}

    hr {{
        border-color: rgba(255, 255, 255, 0.1) !important;
    }}

    .stSpinner > div {{
        border-top-color: #667eea !important;
    }}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 🌈 JAVASCRIPT — ANIME --angle POUR TOUS LES NAVIGATEURS
# ═══════════════════════════════════════════════════════════════
components.html("""
<script>
(function() {
    let angle = 0;
    function updateAngle() {
        angle = (angle + 0.8) % 360;
        document.documentElement.style.setProperty('--angle', angle + 'deg');
        requestAnimationFrame(updateAngle);
    }
    updateAngle();
})();
</script>
""", height=0)

# ═══════════════════════════════════════════════════════════════
# 🎨 FONCTION POUR AFFICHER UN MESSAGE AVEC PHOTO RAINBOW
# ═══════════════════════════════════════════════════════════════
def render_chat_message(role: str, content: str, photo_src: str):
    """Affiche un message de chat avec photo rainbow border."""
    message_class = "chat-message-assistant" if role == "assistant" else "chat-message-user"

    content_html = content.replace("\n", "<br>")
    content_html = content_html.replace("**", "<strong>").replace("**", "</strong>")

    html = f"""
    <div class="custom-chat-message {message_class}">
        <div class="chat-avatar-wrapper">
            <img src="{photo_src}" class="chat-avatar" alt="Avatar">
        </div>
        <div class="chat-content">
            {content_html}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 📸 HEADER AVEC PHOTO
# ═══════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="main-header">
    <div class="header-content">
        <div class="profile-wrapper">
            <img src="{PHOTO_SRC}" class="profile-photo" alt="Amaury Rammanat">
        </div>
        <div class="header-text">
            <h1>Amaury Rammanat</h1>
            <p>Développeur IA en formation | Passionné par le Machine Learning & l'IA Générative</p>
            <div class="status-badge">
                Recherche Alternance Sept. 2026
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 📊 INFO GRID
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="info-grid">
    <div class="info-item">
        <span class="info-icon">Localisation</span>
        <div class="info-label">Ville</div>
        <div class="info-value">Lille, France</div>
    </div>
    <div class="info-item">
        <span class="info-icon">Email</span>
        <div class="info-label">Contact</div>
        <div class="info-value">
            <a href="mailto:rammanatamaury@gmail.com">rammanatamaury@gmail.com</a>
        </div>
    </div>
    <div class="info-item">
        <span class="info-icon">Réseaux</span>
        <div class="info-label">Profils</div>
        <div class="info-value">
            <a href="https://linkedin.com/in/amaury-r-1bb0b032b/" target="_blank">LinkedIn</a> •
            <a href="https://github.com/John-Do59" target="_blank">GitHub</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 💡 SUGGESTIONS
# ═══════════════════════════════════════════════════════════════
with st.expander("Exemples de questions à me poser", expanded=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="suggestion-card">
            <h4>Présentation</h4>
            <ul>
                <li>Présente-toi</li>
                <li>Qui es-tu ?</li>
                <li>Quel poste recherches-tu ?</li>
                <li>Pourquoi l'IA ?</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="suggestion-card">
            <h4>Compétences</h4>
            <ul>
                <li>Quelles sont tes compétences ?</li>
                <li>Tu connais Python ?</li>
                <li>Ton niveau en ML ?</li>
                <li>Quels outils IA ?</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="suggestion-card">
            <h4>Parcours</h4>
            <ul>
                <li>Parle-moi de tes formations</li>
                <li>Tes expériences pro ?</li>
                <li>Quels projets ?</li>
                <li>Pourquoi la reconversion ?</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 🔊 AUDIO PLAYER
# ═══════════════════════════════════════════════════════════════
def create_audio_player(audio_bytes):
    b64 = base64.b64encode(audio_bytes).decode()
    return f"""
    <div class="audio-container">
        <audio id="cvAudio" controls autoplay style="width:100%; border-radius: 10px;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    </div>
    <script>
        var audio = document.getElementById('cvAudio');
        audio.play().catch(function(e) {{ console.log("Autoplay blocked"); }});
    </script>
    """

# ═══════════════════════════════════════════════════════════════
# 📱 SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div style="display: flex; justify-content: center; padding: 20px 0;">
        <div class="profile-wrapper-small">
            <img src="{PHOTO_SRC}" class="profile-photo-small" alt="AR">
        </div>
    </div>
    <div class="sidebar-title">Interaction Vocale</div>
    """, unsafe_allow_html=True)

    text_from_voice = speech_to_text(
        language="fr",
        start_prompt="Parler",
        stop_prompt="Stop",
        just_once=True,
        key="stt"
    )

    if text_from_voice:
        st.success(f"Capturé : {text_from_voice}")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### Options")
    tts_enabled = st.toggle("Réponse vocale", value=True)
    safari_mode = st.checkbox("Mode Safari", value=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    st.markdown("""
    <div style="text-align: center; margin-bottom: 10px;">
        <span style="color: rgba(255,255,255,0.5); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px;">Technologies</span>
    </div>
    <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 5px;">
        <span class="skill-tag">Python</span>
        <span class="skill-tag">LangChain</span>
        <span class="skill-tag">RAG</span>
        <span class="skill-tag">SQL</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Effacer la conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ═══════════════════════════════════════════════════════════════
# 💬 SESSION STATE
# ═══════════════════════════════════════════════════════════════
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": """Bonjour ! Je suis l'assistant IA d'**Amaury Rammanat**.

Je suis actuellement en formation de **Développeur IA chez Simplon** et je recherche une **alternance d'un an à partir de septembre 2026**.

**Je peux vous parler de :**
- Mes **compétences** (Python, SQL, Machine Learning, LLM, RAG...)
- Mon **parcours** et mes **formations** (Simplon, Apple Foundation, ULCO)
- Mes **projets** (Sport-Unity IA, Chatbots, Automatisations N8N)
- Ma **recherche d'alternance** (Data Analyst, Data Scientist, Dev IA)

**Que souhaitez-vous savoir sur mon profil ?**"""
    }]

if "last_spoken" not in st.session_state:
    st.session_state.last_spoken = None

# ═══════════════════════════════════════════════════════════════
# 💬 AFFICHAGE DES MESSAGES AVEC PHOTO RAINBOW
# ═══════════════════════════════════════════════════════════════
chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        render_chat_message(
            role=msg["role"],
            content=msg["content"],
            photo_src=PHOTO_SRC
        )

# ═══════════════════════════════════════════════════════════════
# 💬 INPUT
# ═══════════════════════════════════════════════════════════════
chat_input = st.chat_input("💬 Posez votre question sur mon CV...")
prompt = text_from_voice if text_from_voice else chat_input

# ═══════════════════════════════════════════════════════════════
# 🔄 TRAITEMENT
# ═══════════════════════════════════════════════════════════════
if prompt:
    if len(st.session_state.messages) == 0 or st.session_state.messages[-1].get("content") != prompt:

        st.session_state.messages.append({"role": "user", "content": prompt})
        render_chat_message("user", prompt, PHOTO_SRC)

        with st.spinner("Je réfléchis..."):
            try:
                initial_state = {
                    "question": prompt,
                    "messages": [{"role": "user", "content": prompt}]
                }

                final_state = app.invoke(initial_state)

                response = final_state.get("response", "")
                if not response:
                    response = "Je n'ai pas trouvé cette information dans mon CV. Pouvez-vous reformuler ?"

                render_chat_message("assistant", response, PHOTO_SRC)

                if tts_enabled and response and len(response) < 4000:
                    if response != st.session_state.last_spoken:
                        try:
                            tts = gTTS(text=response, lang="fr")
                            audio_bytes = io.BytesIO()
                            tts.write_to_fp(audio_bytes)
                            audio_bytes.seek(0)
                            audio_data = audio_bytes.read()

                            st.session_state.last_spoken = response

                            if safari_mode:
                                components.html(create_audio_player(audio_data), height=60)
                            else:
                                st.audio(audio_data, format="audio/mp3", autoplay=True)
                        except Exception as e:
                            logger.error(f"TTS error: {e}")

                with st.expander("Debug", expanded=False):
                    dcol1, dcol2 = st.columns(2)
                    with dcol1:
                        st.markdown(f"**Intention:** `{final_state.get('intent')}`")
                    with dcol2:
                        if final_state.get("documents"):
                            st.markdown(f"**RAG:** {len(final_state.get('documents'))} docs")

                    if final_state.get("sql_query") and final_state.get("sql_query") not in ["Error", "Invalid"]:
                        st.code(final_state.get("sql_query"), language="sql")

                st.session_state.messages.append({"role": "assistant", "content": response})

            except Exception as e:
                logger.error(f"Error: {e}")
                st.error("❌ Une erreur est survenue.")

# ═══════════════════════════════════════════════════════════════
# 🎨 FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div style="text-align: center; margin-top: 50px; padding: 30px; opacity: 0.5;">
    <p style="font-size: 0.85rem;">
        Développé avec soin par <strong>Amaury Rammanat</strong><br>
        Python • LangChain • LangGraph • Streamlit
    </p>
</div>
""", unsafe_allow_html=True)