import requests
import os
from dotenv import load_dotenv

load_dotenv()

KIE_API_KEY = os.getenv("KIE_API_KEY")
WEBHOOK_URL = "https://webhook.site/20fe2216-0076-4bd4-a676-59e66ae90134"

url = "https://api.kie.ai/api/v1/jobs/createTask"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {KIE_API_KEY}"
}

payload = {
    "model": "sora-2-text-to-video",
    "callBackUrl": WEBHOOK_URL,
    "input": {
        "prompt": "A beautiful sunrise over Rome with the Colosseum in the background, birds flying, cinematic golden hour lighting",
        "aspect_ratio": "landscape",
        "n_frames": "10",
        "remove_watermark": True
    }
}

print("Invio richiesta a Kie.ai...")
response = requests.post(url, headers=headers, json=payload)
result = response.json()
print(f"Risposta: {result}")

if result.get("code") == 200:
    task_id = result.get("data", {}).get("taskId")
    print(f"\nTask creato! ID: {task_id}")
    print(f"\nControlla qui tra 2-5 minuti:")
    print(f"  {WEBHOOK_URL}")
else:
    print(f"Errore: {result}")
