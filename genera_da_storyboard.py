"""
Genera video da un file storyboard esistente.
Usa polling per attendere il completamento.
"""

import requests
import os
import time
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

KIE_API_KEY = os.getenv("KIE_API_KEY")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

KIE_CREATE_TASK = "https://api.kie.ai/api/v1/jobs/createTask"
KIE_QUERY_TASK = "https://api.kie.ai/api/v1/jobs/queryTask"


def create_video_task(prompt, duration=15):
    """Crea il task di generazione video."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {KIE_API_KEY}"
    }

    payload = {
        "model": "sora-2-text-to-video",
        "input": {
            "prompt": prompt,
            "aspect_ratio": "landscape",
            "n_frames": str(duration) if duration >= 15 else "10",
            "remove_watermark": True
        }
    }

    response = requests.post(KIE_CREATE_TASK, headers=headers, json=payload)
    result = response.json()

    if result.get("code") == 200:
        return result["data"]["taskId"]
    else:
        print(f"Errore creazione task: {result}")
        return None


def check_status(task_id):
    """Controlla lo stato del task."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {KIE_API_KEY}"
    }

    response = requests.post(KIE_QUERY_TASK, headers=headers, json={"taskId": task_id})
    return response.json()


def wait_and_download(task_id, scene_num, max_wait=600):
    """Attende il completamento e scarica il video."""
    start = time.time()

    while time.time() - start < max_wait:
        result = check_status(task_id)
        data = result.get("data", {})
        state = data.get("state", "").lower()

        if state == "success":
            result_json = json.loads(data.get("resultJson", "{}"))
            video_urls = result_json.get("resultUrls", [])

            if video_urls:
                video_url = video_urls[0]
                print(f"  Scena {scene_num}: Completata!")

                # Download
                response = requests.get(video_url, stream=True)
                filepath = OUTPUT_DIR / f"scene_{scene_num:02d}.mp4"

                with open(filepath, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                size_mb = filepath.stat().st_size / (1024 * 1024)
                print(f"  Scena {scene_num}: Salvato {filepath.name} ({size_mb:.1f} MB)")
                return filepath

        elif state == "fail":
            error = data.get("failMsg", "Errore sconosciuto")
            print(f"  Scena {scene_num}: FALLITA - {error}")
            return None

        elapsed = int(time.time() - start)
        print(f"  Scena {scene_num}: In elaborazione... ({elapsed}s)", end="\r")
        time.sleep(10)

    print(f"  Scena {scene_num}: Timeout dopo {max_wait}s")
    return None


def main():
    print("=" * 60)
    print("GENERA VIDEO DA STORYBOARD")
    print("=" * 60)

    if not KIE_API_KEY:
        print("Errore: KIE_API_KEY non configurata in .env")
        return

    # Trova l'ultimo storyboard
    storyboards = sorted(OUTPUT_DIR.glob("storyboard_*.json"), reverse=True)
    if not storyboards:
        print("Nessun storyboard trovato in output/")
        return

    storyboard_path = storyboards[0]
    print(f"\nUsando: {storyboard_path.name}")

    with open(storyboard_path, "r", encoding="utf-8") as f:
        storyboard = json.load(f)

    scenes = storyboard["scenes"]
    print(f"Titolo: {storyboard.get('title', 'N/A')}")
    print(f"Scene: {len(scenes)}")
    print(f"Costo stimato: ~${len(scenes) * 0.15:.2f}")

    # Crea tutti i task
    print("\n" + "-" * 60)
    print("Creazione task...")
    tasks = []

    for scene in scenes:
        scene_num = scene["scene_number"]
        prompt = scene["prompt"]
        duration = scene.get("duration", 15)

        print(f"  Scena {scene_num}: Invio richiesta...")
        task_id = create_video_task(prompt, duration)

        if task_id:
            tasks.append((scene_num, task_id))
            print(f"  Scena {scene_num}: Task ID = {task_id[:20]}...")
        else:
            print(f"  Scena {scene_num}: ERRORE creazione task")

        time.sleep(2)  # Rate limiting

    # Attendi e scarica
    print("\n" + "-" * 60)
    print("Attesa generazione (2-5 min per video)...")
    video_paths = []

    for scene_num, task_id in tasks:
        filepath = wait_and_download(task_id, scene_num)
        if filepath:
            video_paths.append(filepath)

    # Riepilogo
    print("\n" + "=" * 60)
    print(f"COMPLETATO: {len(video_paths)}/{len(tasks)} video generati")
    print("=" * 60)

    if video_paths:
        print("\nVideo generati:")
        for p in video_paths:
            print(f"  - {p.name}")
        print(f"\nPer unire: python merge_videos.py")


if __name__ == "__main__":
    main()
