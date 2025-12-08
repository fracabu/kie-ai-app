"""
Video Promozionale Generator
Genera un video promozionale di 1 minuto usando OpenRouter + Sora 2 (Kie.ai)
"""

import os
import json
import time
import requests
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
KIE_API_KEY = os.getenv("KIE_API_KEY")
SITE_URL = os.getenv("SITE_URL", "")
SITE_NAME = os.getenv("SITE_NAME", "VideoGenerator")

# Kie.ai endpoints
KIE_BASE_URL = "https://api.kie.ai/api/v1/jobs"
KIE_CREATE_TASK = f"{KIE_BASE_URL}/createTask"
KIE_QUERY_TASK = f"{KIE_BASE_URL}/queryTask"  # Try this endpoint

# OpenRouter endpoint
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Output directory
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_storyboard(business_description: str, num_scenes: int = 4) -> list[dict]:
    """
    Usa OpenRouter per generare uno storyboard con scene dettagliate.

    Args:
        business_description: Descrizione del servizio/business da promuovere
        num_scenes: Numero di scene (default 4 per ~60s totali con clip da 15s)

    Returns:
        Lista di scene con prompt dettagliati per Sora 2
    """
    print(f"\n{'='*60}")
    print("FASE 1: Generazione Storyboard con OpenRouter")
    print(f"{'='*60}")

    system_prompt = """Sei un esperto regista pubblicitario e video maker.
Devi creare uno storyboard per un video promozionale professionale.

Per ogni scena, fornisci un prompt DETTAGLIATO e CINEMATOGRAFICO per la generazione video AI.
I prompt devono essere in INGLESE e includere:
- Descrizione visiva dettagliata
- Movimenti di camera (pan, zoom, tracking shot, etc.)
- Illuminazione e atmosfera
- Stile visivo (cinematic, professional, warm colors, etc.)

Rispondi SOLO con un JSON valido nel formato:
{
  "title": "Titolo del video",
  "scenes": [
    {
      "scene_number": 1,
      "duration": 15,
      "description_it": "Descrizione in italiano",
      "prompt": "Detailed English prompt for AI video generation..."
    }
  ]
}"""

    user_prompt = f"""Crea uno storyboard per un video promozionale di 1 minuto per:

{business_description}

Genera esattamente {num_scenes} scene, ciascuna di 15 secondi.
Il video deve essere coinvolgente, professionale e persuasivo.
Ogni scena deve fluire naturalmente nella successiva.

Struttura consigliata:
- Scena 1: Hook/Apertura accattivante che cattura l'attenzione
- Scena 2: Presentazione del problema/necessità
- Scena 3: Soluzione offerta dal servizio/business
- Scena 4: Call-to-action e chiusura memorabile"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": SITE_URL,
        "X-Title": SITE_NAME,
    }

    payload = {
        "model": "anthropic/claude-sonnet-4",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }

    print("Generando storyboard...")
    response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()
    content = result["choices"][0]["message"]["content"]

    # Parse JSON from response
    try:
        # Try to extract JSON from the response
        if "```json" in content:
            json_str = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            json_str = content.split("```")[1].split("```")[0]
        else:
            json_str = content

        storyboard = json.loads(json_str.strip())
    except json.JSONDecodeError as e:
        print(f"Errore parsing JSON: {e}")
        print(f"Risposta raw: {content}")
        raise

    print(f"\nStoryboard generato: {storyboard.get('title', 'Video Promozionale')}")
    print(f"Numero scene: {len(storyboard['scenes'])}")

    for scene in storyboard["scenes"]:
        print(f"\n  Scena {scene['scene_number']}: {scene['description_it'][:50]}...")

    # Save storyboard
    storyboard_path = OUTPUT_DIR / f"storyboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(storyboard_path, "w", encoding="utf-8") as f:
        json.dump(storyboard, f, indent=2, ensure_ascii=False)
    print(f"\nStoryboard salvato: {storyboard_path}")

    return storyboard


def create_video_task(prompt: str, duration: int = 15, aspect_ratio: str = "landscape") -> str:
    """
    Crea un task di generazione video su Kie.ai Sora 2.

    Args:
        prompt: Prompt per la generazione video
        duration: Durata in secondi (10 o 15)
        aspect_ratio: "landscape" o "portrait"

    Returns:
        Task ID per tracking
    """
    headers = {
        "Authorization": f"Bearer {KIE_API_KEY}",
        "Content-Type": "application/json"
    }

    # Map duration to n_frames parameter
    n_frames = "15" if duration >= 15 else "10"

    payload = {
        "model": "sora-2-text-to-video",
        "input": {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "n_frames": n_frames,
            "remove_watermark": True
        }
    }

    response = requests.post(KIE_CREATE_TASK, headers=headers, json=payload)

    if not response.ok:
        print(f"    Errore API: {response.status_code}")
        print(f"    Response: {response.text}")
        response.raise_for_status()

    result = response.json()
    task_id = result.get("taskId") or result.get("task_id") or result.get("id") or result.get("data", {}).get("taskId")

    if not task_id:
        print(f"    Response completa: {result}")

    return task_id


def check_task_status(task_id: str) -> dict:
    """
    Controlla lo stato di un task di generazione video.

    Returns:
        Dict con status e video_url (se completato)
    """
    headers = {
        "Authorization": f"Bearer {KIE_API_KEY}",
        "Content-Type": "application/json"
    }

    endpoints_to_try = [
        ("POST", KIE_QUERY_TASK, {"taskId": task_id}),
        ("POST", f"{KIE_BASE_URL}/getTask", {"taskId": task_id}),
        ("GET", f"{KIE_QUERY_TASK}?taskId={task_id}", None),
        ("GET", f"{KIE_BASE_URL}/task/{task_id}", None),
        ("GET", f"{KIE_BASE_URL}/{task_id}", None),
    ]

    for method, url, body in endpoints_to_try:
        try:
            if method == "POST":
                response = requests.post(url, headers=headers, json=body)
            else:
                response = requests.get(url, headers=headers)

            if response.status_code == 200:
                return response.json()
        except:
            continue

    # If all fail, raise with last error
    print(f"      Tutti gli endpoint falliti per task {task_id}")
    print(f"      Ultimo tentativo: {response.status_code} - {response.text[:300]}")
    response.raise_for_status()

    return response.json()


def wait_for_video(task_id: str, scene_num: int, max_wait: int = 600) -> str:
    """
    Attende il completamento della generazione video.

    Args:
        task_id: ID del task
        scene_num: Numero della scena (per logging)
        max_wait: Tempo massimo di attesa in secondi

    Returns:
        URL del video generato
    """
    start_time = time.time()

    while time.time() - start_time < max_wait:
        result = check_task_status(task_id)
        status = result.get("status", "").lower()

        if status == "completed" or status == "success":
            video_url = result.get("video_url") or result.get("output", {}).get("video_url")
            print(f"  Scena {scene_num}: Completata!")
            return video_url
        elif status == "failed" or status == "error":
            error = result.get("error", "Unknown error")
            raise Exception(f"Generazione fallita per scena {scene_num}: {error}")

        # Progress indicator
        elapsed = int(time.time() - start_time)
        print(f"  Scena {scene_num}: In elaborazione... ({elapsed}s)", end="\r")
        time.sleep(10)

    raise TimeoutError(f"Timeout per scena {scene_num} dopo {max_wait}s")


def download_video(url: str, filename: str) -> Path:
    """Scarica un video da URL."""
    response = requests.get(url, stream=True)
    response.raise_for_status()

    filepath = OUTPUT_DIR / filename
    with open(filepath, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    return filepath


def generate_videos(storyboard: dict) -> list[Path]:
    """
    Genera tutti i video clip dallo storyboard.

    Args:
        storyboard: Dict con scenes dal generatore OpenRouter

    Returns:
        Lista di path ai video scaricati
    """
    print(f"\n{'='*60}")
    print("FASE 2: Generazione Video con Sora 2 (Kie.ai)")
    print(f"{'='*60}")

    scenes = storyboard["scenes"]
    video_paths = []
    task_ids = []

    # Create all tasks first
    print("\nCreazione task di generazione...")
    for scene in scenes:
        prompt = scene["prompt"]
        duration = scene.get("duration", 15)

        print(f"  Scena {scene['scene_number']}: Invio richiesta...")
        task_id = create_video_task(prompt, duration)
        task_ids.append((scene["scene_number"], task_id))
        print(f"  Scena {scene['scene_number']}: Task ID = {task_id}")

        # Small delay between requests to avoid rate limiting
        time.sleep(2)

    # Wait for all videos
    print("\nAttesa completamento generazione...")
    print("(Sora 2 impiega 2-5 minuti per video)")

    for scene_num, task_id in task_ids:
        try:
            video_url = wait_for_video(task_id, scene_num)

            # Download video
            filename = f"scene_{scene_num:02d}.mp4"
            filepath = download_video(video_url, filename)
            video_paths.append(filepath)
            print(f"  Scena {scene_num}: Salvato come {filename}")

        except Exception as e:
            print(f"  Scena {scene_num}: ERRORE - {e}")

    return video_paths


def create_ffmpeg_concat_script(video_paths: list[Path]) -> Path:
    """
    Crea uno script FFmpeg per concatenare i video.

    Returns:
        Path al file di script
    """
    # Create file list for FFmpeg
    filelist_path = OUTPUT_DIR / "filelist.txt"
    with open(filelist_path, "w") as f:
        for path in sorted(video_paths):
            f.write(f"file '{path.name}'\n")

    # Create batch script for Windows
    script_path = OUTPUT_DIR / "merge_videos.bat"
    output_name = f"promo_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"

    with open(script_path, "w") as f:
        f.write(f"""@echo off
echo Merging video clips...
cd /d "%~dp0"
ffmpeg -f concat -safe 0 -i filelist.txt -c copy {output_name}
echo.
echo Video finale creato: {output_name}
pause
""")

    # Also create shell script for Linux/Mac
    sh_script_path = OUTPUT_DIR / "merge_videos.sh"
    with open(sh_script_path, "w") as f:
        f.write(f"""#!/bin/bash
echo "Merging video clips..."
cd "$(dirname "$0")"
ffmpeg -f concat -safe 0 -i filelist.txt -c copy {output_name}
echo ""
echo "Video finale creato: {output_name}"
""")

    return script_path


def main():
    """Main entry point."""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║     VIDEO PROMOZIONALE GENERATOR                              ║
║     OpenRouter + Sora 2 (Kie.ai)                              ║
╚═══════════════════════════════════════════════════════════════╝
    """)

    # Check API keys
    if not OPENROUTER_API_KEY:
        print("ERRORE: OPENROUTER_API_KEY non configurata!")
        print("Crea un file .env con le tue API keys (vedi .env.example)")
        return

    if not KIE_API_KEY:
        print("ERRORE: KIE_API_KEY non configurata!")
        print("Crea un file .env con le tue API keys (vedi .env.example)")
        return

    # Get business description
    print("Descrivi il tuo servizio/business per il video promozionale:")
    print("(Esempio: 'Un'agenzia di web design che crea siti moderni e veloci")
    print(" per piccole imprese, con focus su user experience e conversioni')")
    print()

    business_description = input("Descrizione: ").strip()

    if not business_description:
        print("Nessuna descrizione fornita. Uscita.")
        return

    # Optional: number of scenes
    print("\nNumero di scene? (default: 4 scene da 15s = 1 minuto)")
    num_scenes_input = input("Numero scene [4]: ").strip()
    num_scenes = int(num_scenes_input) if num_scenes_input else 4

    try:
        # Phase 1: Generate storyboard
        storyboard = generate_storyboard(business_description, num_scenes)

        # Confirm before generating videos
        print(f"\n{'='*60}")
        print("CONFERMA GENERAZIONE VIDEO")
        print(f"{'='*60}")
        print(f"Costo stimato: ~${num_scenes * 0.15:.2f} (${0.15} per 10s video)")
        print(f"Tempo stimato: ~{num_scenes * 3}-{num_scenes * 5} minuti")

        confirm = input("\nProcedere con la generazione? [s/N]: ").strip().lower()

        if confirm != 's' and confirm != 'si' and confirm != 'y' and confirm != 'yes':
            print("Generazione annullata. Lo storyboard è stato salvato.")
            return

        # Phase 2: Generate videos
        video_paths = generate_videos(storyboard)

        if video_paths:
            # Phase 3: Create merge script
            print(f"\n{'='*60}")
            print("FASE 3: Preparazione Video Finale")
            print(f"{'='*60}")

            script_path = create_ffmpeg_concat_script(video_paths)

            print(f"\nVideo clips generati: {len(video_paths)}")
            print(f"Directory output: {OUTPUT_DIR.absolute()}")
            print(f"\nPer unire i video, installa FFmpeg e esegui:")
            print(f"  Windows: {script_path.name}")
            print(f"  Linux/Mac: ./merge_videos.sh")

            print(f"\n{'='*60}")
            print("COMPLETATO!")
            print(f"{'='*60}")
        else:
            print("\nNessun video generato con successo.")

    except Exception as e:
        print(f"\nErrore: {e}")
        raise


if __name__ == "__main__":
    main()
