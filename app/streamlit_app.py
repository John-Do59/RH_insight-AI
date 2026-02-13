import streamlit as st
import sys
import os
import io
import base64
from pathlib import Path
import textwrap

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.graph.graph import app
from app.utils.logger import logger
from streamlit_mic_recorder import speech_to_text
import edge_tts
import asyncio
import streamlit.components.v1 as components

# CONFIG
st.set_page_config(
    page_title="Amaury Rammanat | CV IA",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CHARGEMENT PHOTO
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

PHOTO_PATH = Path(__file__).parent / "assets" / "photo_amaury.png"
PHOTO_BASE64 = get_base64_image(PHOTO_PATH)

if PHOTO_BASE64:
    ASSISTANT_PHOTO = f"data:image/png;base64,{PHOTO_BASE64}"
else:
    ASSISTANT_PHOTO = (
        "https://ui-avatars.com/api/?name=Amaury+Rammanat"
        "&size=200&background=667eea&color=fff&bold=true&rounded=true"
    )

# ── Avatar générique pour l'utilisateur (pas ta photo) ──
USER_AVATAR = (
    "https://ui-avatars.com/api/?name=You"
    "&size=200&background=3a3a5c&color=fff&bold=true&rounded=true"
)

# COULEURS PURPLE
PURPLE_GRADIENT = """
    #7c3aed, #8b5cf6, #a78bfa, #7c3aed,
    #6d28d9, #8b5cf6, #a78bfa, #7c3aed
"""
PURPLE_GRADIENT_LIGHT = """
    #667eea, #764ba2, #a78bfa, #c4b5fd,
    #667eea, #764ba2, #a78bfa
"""

# CSS COMPLET — PURPLE THEME
st.markdown(f"""
<style>
    /*  ANIMATIONS  */
    @property --angle {{
        syntax: "<angle>";
        initial-value: 0deg;
        inherits: false;
    }}

    @keyframes spin-purple {{
        to {{ --angle: 360deg; }}
    }}

    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-8px); }}
    }}

    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(15px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes typing-dots {{
        0%, 20% {{ opacity: 0.3; }}
        50% {{ opacity: 1; }}
        80%, 100% {{ opacity: 0.3; }}
    }}

    @keyframes border-flow {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    /*  BACKGROUND  */
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
            radial-gradient(circle at 20% 20%, rgba(124, 58, 237, 0.10) 0%, transparent 40%),
            radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.10) 0%, transparent 40%),
            radial-gradient(circle at 50% 50%, rgba(167, 139, 250, 0.05) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }}

    /*  AVATAR CHAT  */
    .chat-avatar-wrapper {{
        position: relative;
        width: 48px;
        height: 48px;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    /* Animated border ONLY on assistant avatar */
    .chat-message-assistant .chat-avatar-wrapper::before {{
        content: '';
        position: absolute;
        inset: -2px;
        border-radius: 50%;
        background: conic-gradient(
            from var(--angle, 0deg),
            {PURPLE_GRADIENT}
        );
        -webkit-mask:
            radial-gradient(farthest-side, transparent calc(100% - 2px), #fff calc(100% - 2px));
        mask:
            radial-gradient(farthest-side, transparent calc(100% - 2px), #fff calc(100% - 2px));
        animation: spin-purple 4s linear infinite;
        z-index: 1;
    }}

    /* User avatar — simple subtle border, no animation */
    .chat-message-user .chat-avatar-wrapper::before {{
        content: '';
        position: absolute;
        inset: -2px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.15);
        -webkit-mask:
            radial-gradient(farthest-side, transparent calc(100% - 2px), #fff calc(100% - 2px));
        mask:
            radial-gradient(farthest-side, transparent calc(100% - 2px), #fff calc(100% - 2px));
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

    /*  PROFILE HEADER  */
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
            {PURPLE_GRADIENT}
        );
        -webkit-mask:
            radial-gradient(farthest-side, transparent calc(100% - 4px), #fff calc(100% - 4px));
        mask:
            radial-gradient(farthest-side, transparent calc(100% - 4px), #fff calc(100% - 4px));
        animation: spin-purple 5s linear infinite;
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

    /*  SIDEBAR PHOTO — SMALL PURPLE BORDER  */
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
            {PURPLE_GRADIENT}
        );
        -webkit-mask:
            radial-gradient(farthest-side, transparent calc(100% - 3px), #fff calc(100% - 3px));
        mask:
            radial-gradient(farthest-side, transparent calc(100% - 3px), #fff calc(100% - 3px));
        animation: spin-purple 5s linear infinite;
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

    /*  MESSAGES CHAT  */
    .custom-chat-message {{
        display: flex;
        gap: 15px;
        padding: 22px;
        margin: 14px 0;
        border-radius: 22px;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        position: relative;
    }}

    /* Animation ONLY for new messages */
    .custom-chat-message.is-new {{
        animation: fadeInUp 0.5s ease-out;
    }}

    /*  Assistant message  */
    .chat-message-assistant {{
        background: rgba(255, 255, 255, 0.04);
        border: none;
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
            {PURPLE_GRADIENT}
        );
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        animation: spin-purple 6s linear infinite;
        z-index: -1;
        pointer-events: none;
    }}

    /* ── User message ── */
    .chat-message-user {{
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.10), rgba(118, 75, 162, 0.10));
        border: 1px solid rgba(139, 92, 246, 0.15);
        flex-direction: row-reverse;
        z-index: 1;
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

    .chat-content p:last-child {{
        margin-bottom: 0;
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
        background: rgba(124, 58, 237, 0.2);
        padding: 2px 6px;
        border-radius: 4px;
        font-family: 'Fira Code', monospace;
    }}

    /*  GLASSMORPHISM  */
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
        border-color: rgba(139, 92, 246, 0.3);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
    }}

    /*  HEADER  */
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
            #6d28d9, #7c3aed, #8b5cf6, #a78bfa,
            #c4b5fd, #a78bfa, #8b5cf6, #7c3aed, #6d28d9
        );
        background-size: 300% 100%;
        animation: border-flow 5s ease infinite;
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
        background: linear-gradient(135deg, #7c3aed, #8b5cf6);
        color: white;
        padding: 10px 22px;
        border-radius: 50px;
        font-size: 0.95rem;
        font-weight: 600;
        margin-top: 15px;
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.35);
        animation: float 3s ease-in-out infinite;
    }}

    /*  INFO GRID  */
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
        background: linear-gradient(90deg, #7c3aed, #8b5cf6, #a78bfa);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }}

    .info-item:hover::before {{
        transform: scaleX(1);
    }}

    .info-item:hover {{
        transform: translateY(-8px);
        border-color: rgba(124, 58, 237, 0.3);
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

    /* ═══ HIDE DEFAULT STREAMLIT CHAT ═══ */
    [data-testid="stChatMessage"] {{
        display: none !important;
    }}

    /* ═══ CHAT INPUT — PURPLE BORDER ═══ */
    [data-testid="stBottom"] > div {{
        background: transparent !important;
    }}

    .stChatInput {{
        position: relative !important;
        z-index: 1 !important;
        padding: 2px !important;
        border-radius: 27px !important;
        background: conic-gradient(
            from var(--angle, 0deg),
            {PURPLE_GRADIENT}
        ) !important;
        animation: spin-purple 4s linear infinite !important;
    }}

    .stChatInput > div {{
        background: rgba(15, 15, 30, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: none !important;
        border-radius: 25px !important;
        z-index: 2 !important;
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

    /*  SIDEBAR  */
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
        background: linear-gradient(135deg, #7c3aed, #8b5cf6, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    /*  BUTTONS  */
    .stButton > button {{
        background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 12px 25px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.35) !important;
    }}

    .stButton > button:hover {{
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.45) !important;
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
    }}

    /*  EXPANDERS  */
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

    /*  SUGGESTION CARDS  */
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
        border-color: rgba(124, 58, 237, 0.3);
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
        background: rgba(124, 58, 237, 0.1);
        padding-left: 12px;
    }}

    /* ═══ AUDIO ═══ */
    .audio-container {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border-radius: 15px;
        padding: 12px;
        margin-top: 10px;
        border: 1px solid rgba(124, 58, 237, 0.15);
    }}

    /*  SKILL TAGS  */
    .skill-tag {{
        display: inline-block;
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.2), rgba(139, 92, 246, 0.2));
        padding: 6px 14px;
        border-radius: 50px;
        margin: 4px;
        font-size: 0.85rem;
        color: white;
        border: 1px solid rgba(124, 58, 237, 0.25);
        transition: all 0.3s ease;
    }}

    .skill-tag:hover {{
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(124, 58, 237, 0.3);
    }}

    /* ═══ RESPONSIVE ═══ */
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

    /*  MISC  */
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
        background: linear-gradient(135deg, #7c3aed, #8b5cf6);
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
        border-top-color: #7c3aed !important;
    }}

    /* ═══ SOURCE BADGES ═══ */
    .source-badge {{
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
        margin-top: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .badge-rag {{
        background: rgba(124, 58, 237, 0.2);
        border: 1px solid rgba(124, 58, 237, 0.4);
        color: #c4b5fd;
    }}
    .badge-sql {{
        background: rgba(139, 92, 246, 0.2);
        border: 1px solid rgba(139, 92, 246, 0.4);
        color: #ddd6fe;
    }}
    .badge-github {{
        background: rgba(167, 139, 250, 0.2);
        border: 1px solid rgba(167, 139, 250, 0.4);
        color: #ede9fe;
    }}
    .badge-jobs {{
        background: rgba(109, 40, 217, 0.2);
        border: 1px solid rgba(109, 40, 217, 0.4);
        color: #a78bfa;
    }}
</style>
""", unsafe_allow_html=True)

# JAVASCRIPT — ANIME --angle
# NOTE: Ce script tourne dans une iframe, donc on utilise
# un CSS @keyframes comme fallback principal.
# Le JS ci-dessous tente de patcher le parent document.
components.html("""
<script>
(function() {
    let angle = 0;
    function updateAngle() {
        angle = (angle + 0.8) % 360;
        try {
            // Try to set on parent document (Streamlit main frame)
            window.parent.document.documentElement.style.setProperty('--angle', angle + 'deg');
        } catch(e) {
            // Fallback: set on own document
            document.documentElement.style.setProperty('--angle', angle + 'deg');
        }
        requestAnimationFrame(updateAngle);
    }
    updateAngle();
})();
</script>
""", height=0)


# FONCTION RENDU MESSAGE
def render_chat_message(
    role: str,
    content: str,
    sources: list = None,
    is_new: bool = False
):

    message_class = (
        "chat-message-assistant" if role == "assistant"
        else "chat-message-user"
    )
    new_class = "is-new" if is_new else ""

    # Choisir l'avatar selon le rôle
    avatar_src = ASSISTANT_PHOTO if role == "assistant" else USER_AVATAR

    # Conversion markdown basique → HTML
    import re
    content_html = content

    # Bold: **text** → <strong>text</strong>
    content_html = re.sub(
        r'\*\*(.+?)\*\*',
        r'<strong>\1</strong>',
        content_html
    )

    # Line breaks
    content_html = content_html.replace("\n", "<br>")

    # Source badges
    badges_html = ""
    if role == "assistant" and sources:
        badges_html = '<div style="margin-top: 10px;">'
        badge_map = {
            "rag": (' RAG (CV)', 'badge-rag'),
            "sql": (' SQL (Faits)', 'badge-sql'),
            "github": (' GitHub (Code)', 'badge-github'),
            "jobs": (' Emplois', 'badge-jobs'),
        }
        for src in sources:
            if src in badge_map:
                label, cls = badge_map[src]
                badges_html += f'<span class="source-badge {cls}">{label}</span>'
        badges_html += '</div>'

    # Rendu HTML final sur une seule ligne pour éviter que Streamlit n'interprète les indentations comme du Markdown (code blocks)
    html = (
        f'<div class="custom-chat-message {message_class} {new_class}">'
        f'<div class="chat-avatar-wrapper"><img src="{avatar_src}" class="chat-avatar" alt="{role}"></div>'
        f'<div class="chat-content">{content_html}{badges_html}</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


# HEADER
st.markdown(textwrap.dedent(f"""
    <div class="main-header">
        <div class="header-content">
            <div class="profile-wrapper">
                <img src="{ASSISTANT_PHOTO}" class="profile-photo" alt="Amaury Rammanat">
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
"""), unsafe_allow_html=True)

# INFO GRID
st.markdown(textwrap.dedent("""
    <div class="info-grid">
        <div class="info-item">
            <span class="info-icon"></span>
            <div class="info-label">Localisation</div>
            <div class="info-value">Lille, France</div>
        </div>
        <div class="info-item">
            <span class="info-icon"></span>
            <div class="info-label">Contact</div>
            <div class="info-value">
                <a href="mailto:rammanatamaury@gmail.com">rammanatamaury@gmail.com</a>
            </div>
        </div>
        <div class="info-item">
            <span class="info-icon"></span>
            <div class="info-label">Profils</div>
            <div class="info-value">
                <a href="https://linkedin.com/in/amaury-r-1bb0b032b/" target="_blank">LinkedIn</a> •
                <a href="https://github.com/John-Do59" target="_blank">GitHub</a>
            </div>
        </div>
    </div>
"""), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# SUGGESTIONS
with st.expander(" Exemples de questions à me poser", expanded=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(textwrap.dedent("""
            <div class="suggestion-card">
                <h4> Présentation</h4>
                <ul>
                    <li>Présente-toi</li>
                    <li>Qui es-tu ?</li>
                    <li>Quel poste recherches-tu ?</li>
                    <li>Pourquoi l'IA ?</li>
                </ul>
            </div>
        """), unsafe_allow_html=True)

    with col2:
        st.markdown(textwrap.dedent("""
            <div class="suggestion-card">
                <h4> Compétences</h4>
                <ul>
                    <li>Quelles sont tes compétences ?</li>
                    <li>Tu connais Python ?</li>
                    <li>Quels outils IA ?</li>
                </ul>
            </div>
        """), unsafe_allow_html=True)

    with col3:
        st.markdown(textwrap.dedent("""
            <div class="suggestion-card">
                <h4> Projets & Code</h4>
                <ul>
                    <li>Quels sont tes projets GitHub ?</li>
                    <li>Tes technos favorites ?</li>
                </ul>
            </div>
        """), unsafe_allow_html=True)


# AUDIO PLAYER
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


# SIDEBAR
with st.sidebar:
    st.markdown(textwrap.dedent(f"""
        <div style="display: flex; justify-content: center; padding: 20px 0;">
            <div class="profile-wrapper-small">
                <img src="{ASSISTANT_PHOTO}" class="profile-photo-small" alt="AR">
            </div>
        </div>
        <div class="sidebar-title"> Interaction Vocale</div>
    """), unsafe_allow_html=True)

    text_from_voice = speech_to_text(
        language="fr",
        start_prompt=" Parler",
        stop_prompt=" Stop",
        just_once=True,
        key="stt"
    )

    if text_from_voice:
        st.success(f" Capturé : {text_from_voice}")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("###  Options")
    tts_enabled = st.toggle(" Réponse vocale", value=True)
    safari_mode = st.checkbox(" Mode Safari", value=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    st.markdown(textwrap.dedent("""
        <div style="text-align: center; margin-bottom: 10px;">
            <span style="color: rgba(255,255,255,0.5); font-size: 0.75rem;
                  text-transform: uppercase; letter-spacing: 1px;">
                Technologies
            </span>
        </div>
        <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 5px;">
            <span class="skill-tag">Python</span>
            <span class="skill-tag">LangChain</span>
            <span class="skill-tag">RAG</span>
            <span class="skill-tag">SQL</span>
        </div>
    """), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Effacer la conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_spoken = None
        st.rerun()


# SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": (
            "Bonjour ! Je suis l'assistant IA d'**Amaury Rammanat**.\n\n"
            "Je suis actuellement en formation de **Développeur IA chez Simplon** "
            "et je recherche une **alternance d'un an à partir de septembre 2026**.\n\n"
            "**Je peux vous parler de :**\n"
            "- Mes **compétences** (Python, SQL, Machine Learning, LLM, RAG...)\n"
            "- Mon **parcours** et mes **formations** (Simplon, Apple Foundation, ULCO)\n"
            "- Mes **projets** (Sport-Unity IA, Chatbots, Automatisations N8N)\n"
            "- Ma **recherche d'alternance** (Data Analyst, Data Scientist, Dev IA)\n\n"
            "**Que souhaitez-vous savoir sur mon profil ?**"
        ),
        "sources": []
    }]

if "last_spoken" not in st.session_state:
    st.session_state.last_spoken = None

# Track le nombre de messages pour savoir lesquels sont "nouveaux"
if "rendered_count" not in st.session_state:
    st.session_state.rendered_count = 0


# AFFICHAGE DES MESSAGES
chat_container = st.container()

with chat_container:
    for i, msg in enumerate(st.session_state.messages):
        # Les messages déjà rendus ne sont pas "nouveaux"
        is_new = i >= st.session_state.rendered_count

        render_chat_message(
            role=msg["role"],
            content=msg["content"],
            sources=msg.get("sources"),
            is_new=is_new
        )

    # Mettre à jour le compteur
    st.session_state.rendered_count = len(st.session_state.messages)


# INPUT
chat_input = st.chat_input(" Posez votre question sur mon CV...")
prompt = text_from_voice if text_from_voice else chat_input


# TRAITEMENT
if prompt:
    # Éviter les doublons
    last_msg = st.session_state.messages[-1] if st.session_state.messages else None
    is_duplicate = (
        last_msg
        and last_msg.get("role") == "user"
        and last_msg.get("content") == prompt
    )

    if not is_duplicate:
        # Ajouter le message utilisateur
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "sources": []
        })
        render_chat_message("user", prompt, is_new=True)

        with st.spinner(" Je réfléchis..."):
            try:
                initial_state = {
                    "question": prompt,
                    "messages": [{"role": "user", "content": prompt}]
                }

                final_state = app.invoke(initial_state)

                response = final_state.get("response", "")
                sources = final_state.get("agent_sources", [])

                if not response:
                    response = (
                        "Je n'ai pas trouvé cette information dans mon CV. "
                        "Pouvez-vous reformuler ?"
                    )

                # Sauvegarder en session
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "sources": sources
                })

                render_chat_message(
                    "assistant", response,
                    sources=sources, is_new=True
                )

                # TTS
                # TTS (Haut parleur)
                if tts_enabled and response and len(response) < 4000:
                    if response != st.session_state.last_spoken:
                        try:
                            # Fonction asynchrone pour edge-tts
                            async def generate_voice():
                                voice = "fr-FR-HenriNeural"  # Voix d'homme française
                                communicate = edge_tts.Communicate(response, voice)
                                audio_data = b""
                                async for chunk in communicate.stream():
                                    if chunk["type"] == "audio":
                                        audio_data += chunk["data"]
                                return audio_data

                            audio_data = asyncio.run(generate_voice())
                            
                            st.session_state.last_spoken = response

                            if safari_mode:
                                components.html(
                                    create_audio_player(audio_data),
                                    height=60
                                )
                            else:
                                st.audio(
                                    audio_data,
                                    format="audio/mp3",
                                    autoplay=True
                                )
                        except Exception as e:
                            logger.error(f"TTS error: {e}")

                # Debug
                with st.expander("Debug", expanded=False):
                    dcol1, dcol2, dcol3 = st.columns(3)
                    with dcol1:
                        st.markdown(
                            f"**Intention:** `{final_state.get('intent')}`"
                        )
                    with dcol2:
                        st.markdown(
                            f"**Sources:** "
                            f"`{', '.join(sources) if sources else 'N/A'}`"
                        )
                    with dcol3:
                        docs = final_state.get("documents")
                        if docs:
                            st.markdown(f"**RAG:** {len(docs)} docs")

                    sql_q = final_state.get("sql_query")
                    if sql_q and sql_q not in ["Error", "Invalid"]:
                        st.code(sql_q, language="sql")

                    gh = final_state.get("github_data")
                    if gh:
                        st.markdown(f"**GitHub:** {len(gh)} repos")

            except Exception as e:
                logger.error(f"Error: {e}")
                st.error(" Une erreur est survenue. Veuillez réessayer.")


#  FOOTER
st.markdown("""
<div style="text-align: center; margin-top: 50px; padding: 30px; opacity: 0.5;">
    <p style="font-size: 0.85rem;">
        Développé par <strong>Amaury Rammanat</strong><br>
    </p>
</div>
""", unsafe_allow_html=True)