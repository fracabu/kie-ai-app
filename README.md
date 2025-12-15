<h1 align="center">AI Video Generator</h1>
<h3 align="center">Generate promotional videos with AI storyboards and Kie.ai Sora 2</h3>

<p align="center">
  <img src="https://github.com/fracabu/kie-ai-app/actions/workflows/ci.yml/badge.svg" alt="CI" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Claude_AI-8B5CF6?style=flat-square&logo=anthropic&logoColor=white" alt="Claude AI" />
  <img src="https://img.shields.io/badge/Kie.ai-Sora_2-FF6B6B?style=flat-square" alt="Kie.ai" />
</p>

<p align="center">
  :gb: <a href="#english">English</a> | :it: <a href="#italiano">Italiano</a>
</p>

---

## Overview

![AI Video Generator Overview](assets/ai-video-generator-overview.png)

---

<a name="english"></a>
## :gb: English

### What is AI Video Generator?

A Python tool that automates promotional video creation using **Claude AI** for storyboard generation and **Kie.ai Sora 2** for text-to-video generation.

### Features

- **Automated Storyboard Generation**: Uses Claude AI via OpenRouter to create cinematic scene prompts
- **AI Video Generation**: Sends prompts to Kie.ai Sora 2 for text-to-video and image-to-video
- **Multiple Workflows**: Full pipeline, single videos, presenter/avatar videos
- **Video Merging**: FFmpeg integration to combine clips into final video

### Quick Start

```bash
# Clone
git clone https://github.com/fracabu/kie-ai-app.git
cd kie-ai-app

# Install
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your API keys

# Run
python video_generator.py
```

### API Keys

| Service | Get Key |
|---------|---------|
| OpenRouter | https://openrouter.ai/keys |
| Kie.ai | https://kie.ai/api-key |

### Scripts

| Script | Description |
|--------|-------------|
| `video_generator.py` | Full workflow: storyboard + video creation |
| `genera_loop_video.py` | Generate single 15s video with auto-download |
| `genera_video_presentazione.py` | Generate presenter/avatar videos |
| `download_videos.py` | Download videos from Kie.ai URLs |
| `merge_videos.py` | Merge video clips using FFmpeg |

### How It Works

```
Business Description
        |
        v
+-------------------+
|    OpenRouter     |  Claude AI generates
|  (Storyboard AI)  |  cinematic prompts
+-------------------+
        |
        v
+-------------------+
|     Kie.ai        |  Sora 2 generates
|   (Sora 2 API)    |  video clips
+-------------------+
        |
        v
+-------------------+
|      FFmpeg       |  Merge clips into
|   (Video Merge)   |  final video
+-------------------+
        |
        v
    Final Video
```

### Pricing

| Service | Cost |
|---------|------|
| Sora 2 (10s/15s) | $0.15 (30 credits) |
| Sora 2 Pro HD | $1.65-$3.15 |
| OpenRouter (Claude) | ~$0.01-0.05 per storyboard |

---

<a name="italiano"></a>
## :it: Italiano

### Cos'e AI Video Generator?

Uno strumento Python che automatizza la creazione di video promozionali usando **Claude AI** per la generazione dello storyboard e **Kie.ai Sora 2** per la generazione video da testo.

### Funzionalita

- **Generazione Automatica Storyboard**: Usa Claude AI via OpenRouter per creare prompt cinematografici
- **Generazione Video AI**: Invia i prompt a Kie.ai Sora 2 per text-to-video e image-to-video
- **Workflow Multipli**: Pipeline completa, video singoli, video presenter/avatar
- **Unione Video**: Integrazione FFmpeg per combinare le clip nel video finale

### Quick Start

```bash
# Clona
git clone https://github.com/fracabu/kie-ai-app.git
cd kie-ai-app

# Installa
pip install -r requirements.txt

# Configura
cp .env.example .env
# Modifica .env con le tue API key

# Esegui
python video_generator.py
```

### Chiavi API

| Servizio | Ottieni Chiave |
|----------|----------------|
| OpenRouter | https://openrouter.ai/keys |
| Kie.ai | https://kie.ai/api-key |

### Script Disponibili

| Script | Descrizione |
|--------|-------------|
| `video_generator.py` | Workflow completo: storyboard + creazione video |
| `genera_loop_video.py` | Genera singolo video 15s con auto-download |
| `genera_video_presentazione.py` | Genera video presenter/avatar |
| `download_videos.py` | Scarica video da URL Kie.ai |
| `merge_videos.py` | Unisce clip video usando FFmpeg |

### Come Funziona

```
Descrizione Business
        |
        v
+-------------------+
|    OpenRouter     |  Claude AI genera
|  (Storyboard AI)  |  prompt cinematografici
+-------------------+
        |
        v
+-------------------+
|     Kie.ai        |  Sora 2 genera
|   (Sora 2 API)    |  clip video
+-------------------+
        |
        v
+-------------------+
|      FFmpeg       |  Unisce clip nel
|   (Video Merge)   |  video finale
+-------------------+
        |
        v
    Video Finale
```

### Prezzi

| Servizio | Costo |
|----------|-------|
| Sora 2 (10s/15s) | $0.15 (30 crediti) |
| Sora 2 Pro HD | $1.65-$3.15 |
| OpenRouter (Claude) | ~$0.01-0.05 per storyboard |

---

## Requirements

- Python 3.10+
- FFmpeg (for video merging)
- OpenRouter API key
- Kie.ai API key

---

## License

MIT

---

<p align="center">
  <strong>AI Video Generator</strong> — Powered by Claude AI + Kie.ai Sora 2
</p>

<p align="center">
  <a href="https://github.com/fracabu">
    <img src="https://img.shields.io/badge/Made_by-fracabu-8B5CF6?style=flat-square" alt="Made by fracabu" />
  </a>
</p>
