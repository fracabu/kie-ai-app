"""
Genera un singolo video da 15 secondi per YouTube loop.
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

PROMPT = """Slow motion cinematic shot of massive rusty chains shattering into particles, abandoned industrial temple with overgrown vines, warm magenta and orange light breaking through cracks, dust and debris floating in air, camera slowly pushing forward, painterly dreamlike atmosphere, dystopian ruins, soft ethereal lighting, 16:9 cinematic"""


def create_video_task():
    """Crea il task di generazione video."""
    url = "https://api.kie.ai/api/v1/jobs/createTask"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {KIE_API_KEY}"
    }

    payload = {
        "model": "sora-2-text-to-video",
        "input": {
            "prompt": PROMPT,
            "aspect_ratio": "landscape",  # 16:9
            "n_frames": "15",  # 15 secondi
            "remove_watermark": True
        }
    }

    print("Invio richiesta a Kie.ai...")
    print(f"Prompt: {PROMPT[:80]}...")
    print(f"Durata: 15 secondi | Aspect: 16:9 landscape")

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()

    if result.get("code") == 200:
        task_id = result["data"]["taskId"]
        print(f"\n✓ Task creato: {task_id}")
        return task_id
    else:
        print(f"\n✗ Errore: {result}")
        return None


def check_status(task_id):
    """Controlla lo stato del task."""
    url = "https://api.kie.ai/api/v1/jobs/queryTask"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {KIE_API_KEY}"
    }

    response = requests.post(url, headers=headers, json={"taskId": task_id})
    return response.json()


def wait_and_download(task_id):
    """Attende il completamento e scarica il video."""
    print("\nAttesa generazione (2-5 minuti)...")

    start = time.time()
    while time.time() - start < 600:  # max 10 min
        result = check_status(task_id)

        # Parse status from response
        data = result.get("data", {})
        state = data.get("state", "").lower()

        if state == "success":
            # Parse resultJson per ottenere URL
            result_json = json.loads(data.get("resultJson", "{}"))
            video_urls = result_json.get("resultUrls", [])

            if video_urls:
                video_url = video_urls[0]
                print(f"\n✓ Video pronto!")
                print(f"URL: {video_url}")

                # Download
                print("\nDownload in corso...")
                response = requests.get(video_url, stream=True)
                filepath = OUTPUT_DIR / "loop_video_15s.mp4"

                with open(filepath, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                size_mb = filepath.stat().st_size / (1024 * 1024)
                print(f"✓ Salvato: {filepath} ({size_mb:.1f} MB)")
                return filepath

        elif state == "fail":
            error = data.get("failMsg", "Errore sconosciuto")
            print(f"\n✗ Generazione fallita: {error}")
            return None

        # Progress
        elapsed = int(time.time() - start)
        print(f"  In elaborazione... ({elapsed}s)", end="\r")
        time.sleep(10)

    print("\n✗ Timeout dopo 10 minuti")
    return None


def main():
    print("=" * 60)
    print("GENERA VIDEO LOOP 15s PER YOUTUBE")
    print("=" * 60)

    if not KIE_API_KEY:
        print("Errore: KIE_API_KEY non configurata in .env")
        return

    print(f"\nCosto: ~$0.15 (30 credits)")
    confirm = input("Procedere? [s/N]: ").strip().lower()

    if confirm not in ['s', 'si', 'y', 'yes']:
        print("Annullato.")
        return

    task_id = create_video_task()
    if task_id:
        result = wait_and_download(task_id)
        if result:
            print("\n" + "=" * 60)
            print("COMPLETATO!")
            print(f"Video: {result}")
            print("Pronto per upload su YouTube!")
            print("=" * 60)


if __name__ == "__main__":
    main()
