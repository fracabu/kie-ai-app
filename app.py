"""
AI Video Generator - Streamlit UI
Generate AI videos with Kie.ai Sora 2
"""

import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Config
KIE_API_KEY = os.getenv("KIE_API_KEY")

# Kie.ai API endpoint
KIE_CREATE_TASK = "https://api.kie.ai/api/v1/jobs/createTask"

# Translations
TRANSLATIONS = {
    "it": {
        "page_title": "AI Video Generator",
        "caption": "Genera video con Kie.ai Sora 2",
        "api_error": "KIE_API_KEY non configurata! Aggiungi la chiave nel file `.env`",
        "sidebar_info": "Info",
        "sidebar_costs": "**Costi:**",
        "sidebar_time": "**Tempo:** 2-5 minuti",
        "language": "Lingua",
        "step1_title": "1. Descrivi il tuo video",
        "prompt_label": "Prompt",
        "prompt_placeholder": "Descrivi la scena che vuoi generare...\n\nEs: A beautiful sunset over the ocean, waves gently crashing on the shore, golden hour lighting, cinematic drone shot, 4K quality",
        "duration_label": "Durata",
        "duration_format": "{} secondi",
        "format_label": "Formato",
        "format_landscape": "16:9 Orizzontale",
        "format_portrait": "9:16 Verticale",
        "generate_btn": "Genera Video",
        "prompt_warning": "Inserisci un prompt!",
        "step2_title": "2. Generazione",
        "sending": "Invio richiesta a Kie.ai...",
        "success": "**Richiesta inviata con successo!**",
        "task_id": "Task ID",
        "estimated_time": "Tempo stimato",
        "cost": "Costo",
        "check_status": "**Controlla lo stato del video su Kie.ai:**",
        "open_dashboard": "Apri Dashboard Kie.ai",
        "video_ready_caption": "Il video apparira' nei 'Logs' quando sara' pronto.",
        "dashboard_url": "https://kie.ai/it/logs"
    },
    "en": {
        "page_title": "AI Video Generator",
        "caption": "Generate videos with Kie.ai Sora 2",
        "api_error": "KIE_API_KEY not configured! Add the key in the `.env` file",
        "sidebar_info": "Info",
        "sidebar_costs": "**Costs:**",
        "sidebar_time": "**Time:** 2-5 minutes",
        "language": "Language",
        "step1_title": "1. Describe your video",
        "prompt_label": "Prompt",
        "prompt_placeholder": "Describe the scene you want to generate...\n\nEx: A beautiful sunset over the ocean, waves gently crashing on the shore, golden hour lighting, cinematic drone shot, 4K quality",
        "duration_label": "Duration",
        "duration_format": "{} seconds",
        "format_label": "Format",
        "format_landscape": "16:9 Landscape",
        "format_portrait": "9:16 Portrait",
        "generate_btn": "Generate Video",
        "prompt_warning": "Please enter a prompt!",
        "step2_title": "2. Generation",
        "sending": "Sending request to Kie.ai...",
        "success": "**Request sent successfully!**",
        "task_id": "Task ID",
        "estimated_time": "Estimated time",
        "cost": "Cost",
        "check_status": "**Check your video status on Kie.ai:**",
        "open_dashboard": "Open Kie.ai Dashboard",
        "video_ready_caption": "The video will appear in 'Logs' when ready.",
        "dashboard_url": "https://kie.ai/logs"
    }
}


def get_text(key: str, lang: str) -> str:
    """Get translated text for the given key and language."""
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)


def create_video_task(prompt: str, duration: str = "15", aspect_ratio: str = "landscape") -> str | None:
    """Create a video generation task on Kie.ai."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {KIE_API_KEY}"
    }

    payload = {
        "model": "sora-2-text-to-video",
        "input": {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "n_frames": duration,
            "remove_watermark": True
        }
    }

    response = requests.post(KIE_CREATE_TASK, headers=headers, json=payload)
    result = response.json()

    if result.get("code") == 200:
        return result["data"]["taskId"]
    else:
        st.error(f"API Error: {result}")
        return None


# ============ STREAMLIT UI ============

st.set_page_config(
    page_title="AI Video Generator",
    page_icon="🎬",
    layout="centered"
)

# Sidebar - Language selector first
with st.sidebar:
    lang = st.selectbox(
        "🌐 Language / Lingua",
        options=["en", "it"],
        format_func=lambda x: "English" if x == "en" else "Italiano"
    )

    st.divider()

    st.header(get_text("sidebar_info", lang))
    st.info(f"""
    {get_text("sidebar_costs", lang)}
    - 10s video: $0.15
    - 15s video: $0.15

    {get_text("sidebar_time", lang)}
    """)

    st.divider()
    st.caption("Powered by Kie.ai Sora 2")

# Header
st.title("🎬 AI Video Generator")
st.caption(get_text("caption", lang))

# Check API key
if not KIE_API_KEY:
    st.error(get_text("api_error", lang))
    st.stop()

# Main content
st.subheader(get_text("step1_title", lang))

prompt = st.text_area(
    get_text("prompt_label", lang),
    placeholder=get_text("prompt_placeholder", lang),
    height=150
)

# Options in columns
col1, col2 = st.columns(2)

with col1:
    duration = st.selectbox(
        get_text("duration_label", lang),
        options=["15", "10"],
        format_func=lambda x: get_text("duration_format", lang).format(x)
    )

with col2:
    aspect_ratio = st.selectbox(
        get_text("format_label", lang),
        options=["landscape", "portrait"],
        format_func=lambda x: get_text("format_landscape", lang) if x == "landscape" else get_text("format_portrait", lang)
    )

st.divider()

# Generate button
if st.button(f"🚀 {get_text('generate_btn', lang)}", type="primary", use_container_width=True):
    if not prompt.strip():
        st.warning(get_text("prompt_warning", lang))
    else:
        st.subheader(get_text("step2_title", lang))

        # Create task
        with st.spinner(get_text("sending", lang)):
            task_id = create_video_task(prompt, duration, aspect_ratio)

        if task_id:
            # Success - show task ID and dashboard link
            st.success(get_text("success", lang))

            st.info(f"""
            📋 **{get_text("task_id", lang)}:** `{task_id}`

            ⏱️ **{get_text("estimated_time", lang)}:** 2-5 min

            💰 **{get_text("cost", lang)}:** ~$0.15 (30 credits)
            """)

            # Direct link to Kie.ai dashboard
            st.divider()
            st.write(get_text("check_status", lang))
            st.link_button(f"🔗 {get_text('open_dashboard', lang)}", get_text("dashboard_url", lang), use_container_width=True)

            st.caption(get_text("video_ready_caption", lang))
