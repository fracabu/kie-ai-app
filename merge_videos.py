"""
Script per unire i video clip in un unico video finale.
Metti i video scaricati nella cartella 'output' e esegui questo script.
"""

import os
import subprocess
from pathlib import Path

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

def find_videos():
    """Trova tutti i video mp4 nella cartella output."""
    videos = list(OUTPUT_DIR.glob("*.mp4"))
    videos.sort()  # Ordina per nome
    return videos

def create_filelist(videos):
    """Crea il file filelist.txt per FFmpeg."""
    filelist_path = OUTPUT_DIR / "filelist.txt"
    with open(filelist_path, "w") as f:
        for video in videos:
            # Usa percorso assoluto con slash forward (FFmpeg preferisce)
            abs_path = str(video.absolute()).replace("\\", "/")
            f.write(f"file '{abs_path}'\n")
    return filelist_path

def merge_videos(filelist_path, output_name="video_promo_finale.mp4"):
    """Unisce i video usando FFmpeg."""
    output_path = OUTPUT_DIR / output_name

    # Usa percorsi assoluti
    filelist_abs = filelist_path.absolute()
    output_abs = output_path.absolute()

    cmd = [
        "ffmpeg",
        "-y",  # Sovrascrivi se esiste
        "-f", "concat",
        "-safe", "0",
        "-i", str(filelist_abs),
        "-c", "copy",
        str(output_abs)
    ]

    print(f"Esecuzione: {' '.join(cmd)}")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print(f"\nSuccesso!")
    else:
        print(f"\nErrore FFmpeg (codice {result.returncode})")

    return output_path

def main():
    print("=" * 50)
    print("MERGE VIDEO CLIPS")
    print("=" * 50)

    videos = find_videos()

    if not videos:
        print("\nNessun video trovato nella cartella 'output'!")
        print("Scarica i video da Kie.ai e mettili nella cartella output/")
        print("\nRinomina i file in ordine:")
        print("  - scene_01.mp4 (apertura)")
        print("  - scene_02.mp4 (caos vs calma)")
        print("  - scene_03.mp4 (tour appartamento) - da rigenerare")
        print("  - scene_04.mp4 (chiusura emotiva)")
        return

    print(f"\nVideo trovati ({len(videos)}):")
    for i, v in enumerate(videos, 1):
        print(f"  {i}. {v.name}")

    # Crea filelist
    filelist = create_filelist(videos)
    print(f"\nCreato: {filelist}")

    # Conferma
    confirm = input("\nUnire questi video? [s/N]: ").strip().lower()
    if confirm not in ['s', 'si', 'y', 'yes']:
        print("Operazione annullata.")
        return

    # Merge
    print("\nUnione in corso...")
    output = merge_videos(filelist)

    print(f"\n{'=' * 50}")
    print(f"VIDEO FINALE CREATO: {output}")
    print(f"{'=' * 50}")

if __name__ == "__main__":
    main()
