# AI Video Generator

Generate promotional videos using OpenRouter (AI storyboard) + Kie.ai Sora 2 (video generation).

## Features

- **Automated Storyboard Generation**: Uses Claude AI via OpenRouter to create cinematic scene prompts from a business description
- **AI Video Generation**: Sends prompts to Kie.ai Sora 2 for text-to-video and image-to-video generation
- **Multiple Workflows**: Full pipeline, single videos, presenter/avatar videos
- **Video Merging**: FFmpeg integration to combine clips into final video

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
cp .env.example .env
```

Edit `.env` with your keys:
```
OPENROUTER_API_KEY=sk-or-v1-xxx
KIE_API_KEY=your-kie-key
```

Get API keys:
- OpenRouter: https://openrouter.ai/keys
- Kie.ai: https://kie.ai/api-key

### 3. Run

```bash
python video_generator.py
```

## Scripts

| Script | Description |
|--------|-------------|
| `video_generator.py` | Full workflow: storyboard generation + video creation |
| `genera_loop_video.py` | Generate single 15s video with auto-download |
| `genera_video_presentazione.py` | Generate presenter/avatar videos |
| `download_videos.py` | Download videos from Kie.ai URLs |
| `merge_videos.py` | Merge video clips using FFmpeg |
| `test_callback.py` | Test Kie.ai API with webhook callback |

## How It Works

```
Business Description
        │
        ▼
┌───────────────────┐
│    OpenRouter     │  Claude AI generates
│  (Storyboard AI)  │  cinematic prompts
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│     Kie.ai        │  Sora 2 generates
│   (Sora 2 API)    │  video clips
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│      FFmpeg       │  Merge clips into
│   (Video Merge)   │  final video
└─────────┬─────────┘
          │
          ▼
    Final Video
```

## Kie.ai Models

| Model | Description |
|-------|-------------|
| `sora-2-text-to-video` | Text prompt to 10s/15s video |
| `sora-2-image-to-video` | Animate an image |
| `sora-2-pro-text-to-video` | Pro quality (720p/1080p) |
| `sora-2-pro-image-to-video` | Pro image animation |
| `sora-watermark-remover` | Remove watermarks |

## Pricing

| Service | Cost |
|---------|------|
| Sora 2 (10s) | $0.15 (30 credits) |
| Sora 2 (15s) | $0.15 (30 credits) |
| Sora 2 Pro Standard | $0.75-$1.35 |
| Sora 2 Pro HD | $1.65-$3.15 |
| OpenRouter (Claude) | ~$0.01-0.05 per storyboard |

## Output

Generated videos are saved to the `output/` directory:
- `scene_01.mp4`, `scene_02.mp4`, ... - Individual clips
- `storyboard_*.json` - Generated storyboard
- `filelist.txt` - FFmpeg concat list
- `merge_videos.bat` / `merge_videos.sh` - Merge scripts

## Requirements

- Python 3.10+
- FFmpeg (for video merging)
- OpenRouter API key
- Kie.ai API key

## License

MIT

