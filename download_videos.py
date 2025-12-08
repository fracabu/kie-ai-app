"""
Script per scaricare i video generati da Kie.ai.
Inserisci gli URL dei video qui sotto.
"""

import requests
from pathlib import Path

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# URL dei video generati da Kie.ai
VIDEOS = {
    "scene_01_apertura.mp4": "https://tempfile.aiquickdraw.com/f/390523ea47b5e5ac52f67e8aadf918a4/d1bfbaf9-f49f-4782-875a-b5f6bda2fa9d.mp4",
    "scene_02_caos_calma.mp4": "https://tempfile.aiquickdraw.com/f/5b36b65e2d60e2c5887a70b88f68d922/05edef63-78ac-48d5-9064-0832b0337867.mp4",
    # scene_03 - FALLITA, da rigenerare
    "scene_04_chiusura.mp4": "https://tempfile.aiquickdraw.com/f/b41b867d3661e2b8ccc8970b992b6061/372c324d-4306-4347-ae79-ee5f2e2e9c84.mp4",
}

def download_video(url, filename):
    """Scarica un video da URL."""
    if not url:
        print(f"  Skipping {filename} - URL mancante")
        return False

    filepath = OUTPUT_DIR / filename
    print(f"  Scaricando {filename}...")

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        size_mb = filepath.stat().st_size / (1024 * 1024)
        print(f"  Salvato: {filepath} ({size_mb:.1f} MB)")
        return True

    except Exception as e:
        print(f"  Errore: {e}")
        return False

def main():
    print("=" * 50)
    print("DOWNLOAD VIDEO DA KIE.AI")
    print("=" * 50)

    print("\nVideo da scaricare:")
    for name, url in VIDEOS.items():
        status = "OK" if url else "MANCANTE"
        print(f"  - {name}: {status}")

    print("\n" + "-" * 50)

    downloaded = 0
    for name, url in VIDEOS.items():
        if download_video(url, name):
            downloaded += 1

    print("\n" + "=" * 50)
    print(f"Scaricati: {downloaded}/{len(VIDEOS)} video")
    print(f"Cartella: {OUTPUT_DIR.absolute()}")
    print("=" * 50)

    if downloaded > 0:
        print("\nOra esegui: python merge_videos.py")

if __name__ == "__main__":
    main()
