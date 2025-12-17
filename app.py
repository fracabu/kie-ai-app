"""
AI Video Generator - Streamlit UI
Genera video AI con Kie.ai Sora 2
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


def create_video_task(prompt: str, duration: str = "15", aspect_ratio: str = "landscape") -> str | None:
    """Crea un task di generazione video su Kie.ai."""
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
        st.error(f"Errore API: {result}")
        return None


# ============ STREAMLIT UI ============

st.set_page_config(
    page_title="AI Video Generator",
    page_icon="🎬",
    layout="centered"
)

# Header
st.title("🎬 AI Video Generator")
st.caption("Genera video con Kie.ai Sora 2")

# Check API key
if not KIE_API_KEY:
    st.error("KIE_API_KEY non configurata! Aggiungi la chiave nel file `.env`")
    st.stop()

# Sidebar info
with st.sidebar:
    st.header("Info")
    st.info("""
    **Costi:**
    - 10s video: $0.15
    - 15s video: $0.15

    **Tempo:** 2-5 minuti
    """)

    st.divider()
    st.caption("Powered by Kie.ai Sora 2")

# Main content
st.subheader("1. Descrivi il tuo video")

prompt = st.text_area(
    "Prompt",
    placeholder="Descrivi la scena che vuoi generare...\n\nEs: A beautiful sunset over the ocean, waves gently crashing on the shore, golden hour lighting, cinematic drone shot, 4K quality",
    height=150
)

# Options in columns
col1, col2 = st.columns(2)

with col1:
    duration = st.selectbox(
        "Durata",
        options=["15", "10"],
        format_func=lambda x: f"{x} secondi"
    )

with col2:
    aspect_ratio = st.selectbox(
        "Formato",
        options=["landscape", "portrait"],
        format_func=lambda x: "16:9 Orizzontale" if x == "landscape" else "9:16 Verticale"
    )

st.divider()

# Generate button
if st.button("🚀 Genera Video", type="primary", use_container_width=True):
    if not prompt.strip():
        st.warning("Inserisci un prompt!")
    else:
        st.subheader("2. Generazione")

        # Create task
        with st.spinner("Invio richiesta a Kie.ai..."):
            task_id = create_video_task(prompt, duration, aspect_ratio)

        if task_id:
            # Success - mostra task ID e link a dashboard
            st.success("**Richiesta inviata con successo!**")

            st.info(f"""
            📋 **Task ID:** `{task_id}`

            ⏱️ **Tempo stimato:** 2-5 minuti

            💰 **Costo:** ~$0.15 (30 credits)
            """)

            # Link diretto a Kie.ai dashboard
            st.divider()
            st.write("**Controlla lo stato del video su Kie.ai:**")
            st.link_button("🔗 Apri Dashboard Kie.ai", "https://kie.ai/it/logs", use_container_width=True)

            st.caption("Il video apparira' nei 'Logs' quando sara' pronto.")
