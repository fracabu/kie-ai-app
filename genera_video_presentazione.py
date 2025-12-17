"""
Genera video di presentazione appartamento con avatar donna.
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

KIE_API_KEY = os.getenv("KIE_API_KEY")
# Get your webhook URL from https://webhook.site (free, for testing)
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://webhook.site/YOUR-UUID-HERE")

def create_video_task(prompt, model="sora-2-text-to-video", duration="10", image_url=None):
    """Crea un task di generazione video."""

    url = "https://api.kie.ai/api/v1/jobs/createTask"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {KIE_API_KEY}"
    }

    input_data = {
        "prompt": prompt,
        "aspect_ratio": "landscape",
        "n_frames": duration,
        "remove_watermark": True
    }

    # Se c'è un'immagine, usa image-to-video
    if image_url:
        model = "sora-2-image-to-video"
        input_data["image_urls"] = [image_url]

    payload = {
        "model": model,
        "callBackUrl": WEBHOOK_URL,
        "input": input_data
    }

    print(f"Invio richiesta: {model}")
    print(f"Prompt: {prompt[:100]}...")

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()

    if result.get("code") == 200:
        task_id = result["data"]["taskId"]
        print(f"Task creato: {task_id}")
        return task_id
    else:
        print(f"Errore: {result}")
        return None


def main():
    print("=" * 60)
    print("GENERA VIDEO PRESENTAZIONE APPARTAMENTO")
    print("=" * 60)

    # Prompt per la presentatrice
    presenter_prompt = """
    A beautiful young Italian woman with long dark hair, wearing an elegant white blouse,
    standing in a bright cozy bedroom with natural sunlight streaming through wooden shuttered windows.
    She smiles warmly at the camera and gestures gracefully towards a comfortable double bed with white linens.
    The room has wooden parquet floors and a colorful artwork on the white wall.
    Real estate presentation style, professional lighting, cinematic quality,
    she appears welcoming and friendly like a vacation rental host.
    Smooth camera movement, 4K quality.
    """.strip()

    print("\n" + "-" * 60)
    print("OPZIONI DISPONIBILI:")
    print("-" * 60)
    print("1. Video con presentatrice (text-to-video)")
    print("2. Anima la tua foto (image-to-video) - richiede URL pubblico")
    print("3. Entrambi")

    choice = input("\nScelta [1/2/3]: ").strip()

    if choice in ["1", "3"]:
        print("\n--- Generazione video presentatrice ---")
        task1 = create_video_task(presenter_prompt, duration="10")
        if task1:
            print(f"Controlla risultato su: {WEBHOOK_URL}")

    if choice in ["2", "3"]:
        print("\n--- Animazione foto ---")
        image_url = input("Inserisci URL pubblico della foto: ").strip()

        if image_url:
            animation_prompt = """
            Smooth cinematic camera pan across the bedroom,
            natural sunlight gently shifting through the windows,
            soft breeze moving the curtains slightly,
            warm inviting atmosphere, professional real estate video style.
            """
            task2 = create_video_task(animation_prompt, duration="10", image_url=image_url)
            if task2:
                print(f"Controlla risultato su: {WEBHOOK_URL}")
        else:
            print("URL non fornito, skip.")

    print("\n" + "=" * 60)
    print("Task inviati! Controlla Kie.ai Logs o webhook.site tra 2-5 minuti.")
    print("=" * 60)


if __name__ == "__main__":
    main()
