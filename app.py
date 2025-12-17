"""
AI Video Generator - Streamlit UI
Genera video AI con Kie.ai Sora 2
"""

import streamlit as st
import requests
import os
import time
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Config
KIE_API_KEY = os.getenv("KIE_API_KEY")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Kie.ai API endpoints
KIE_CREATE_TASK = "https://api.kie.ai/api/v1/jobs/createTask"
KIE_QUERY_TASK = "https://api.kie.ai/api/v1/jobs/queryTask"


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


def check_task_status(task_id: str) -> dict:
    """Controlla lo stato del task."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {KIE_API_KEY}"
    }

    response = requests.post(KIE_QUERY_TASK, headers=headers, json={"taskId": task_id})
    return response.json()


def wait_for_video(task_id: str, progress_bar, status_text, max_wait: int = 600) -> str | None:
    """Attende il completamento e restituisce l'URL del video."""
    start_time = time.time()

    while time.time() - start_time < max_wait:
        result = check_task_status(task_id)
        data = result.get("data", {})
        state = data.get("state", "").lower()

        elapsed = int(time.time() - start_time)
        progress = min(elapsed / max_wait, 0.95)  # Max 95% durante attesa
        progress_bar.progress(progress)
        status_text.text(f"Generazione in corso... {elapsed}s")

        if state == "success":
            result_json = json.loads(data.get("resultJson", "{}"))
            video_urls = result_json.get("resultUrls", [])
            if video_urls:
                progress_bar.progress(1.0)
                return video_urls[0]

        elif state == "fail":
            error = data.get("failMsg", "Errore sconosciuto")
            st.error(f"Generazione fallita: {error}")
            return None

        time.sleep(5)

    st.error(f"Timeout dopo {max_wait}s")
    return None


def download_video(url: str, filename: str) -> Path:
    """Scarica il video e lo salva localmente."""
    response = requests.get(url, stream=True)
    response.raise_for_status()

    filepath = OUTPUT_DIR / filename
    with open(filepath, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    return filepath


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
    st.error("⚠️ KIE_API_KEY non configurata! Aggiungi la chiave nel file `.env`")
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
            st.success(f"Task creato! ID: `{task_id[:20]}...`")

            # Progress
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Wait for video
            video_url = wait_for_video(task_id, progress_bar, status_text)

            if video_url:
                status_text.text("Download video...")

                # Download
                filename = f"video_{int(time.time())}.mp4"
                filepath = download_video(video_url, filename)

                # Show result
                st.subheader("3. Risultato")
                st.success(f"Video generato! Salvato in `{filepath}`")

                # Video player
                st.video(str(filepath))

                # Download button
                with open(filepath, "rb") as f:
                    st.download_button(
                        label="📥 Scarica Video",
                        data=f,
                        file_name=filename,
                        mime="video/mp4"
                    )
