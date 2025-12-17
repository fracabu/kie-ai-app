# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Video Generator - Creates promotional videos using OpenRouter (storyboard generation) and Kie.ai Sora 2 (video generation). Videos are output to the `output/` directory.

## Requirements

- Python 3.10+
- FFmpeg (for video merging only)
- API keys: OpenRouter + Kie.ai

## Commands

```bash
pip install -r requirements.txt          # Install dependencies
cp .env.example .env                      # Setup environment (edit with your keys)

streamlit run app.py                      # Launch web UI (http://localhost:8501)
python video_generator.py                 # Full workflow: storyboard + video generation
python genera_da_storyboard.py            # Generate videos from existing storyboard JSON
python genera_video_presentazione.py      # Generate presenter/avatar videos
python genera_loop_video.py               # Generate single 15s loop video
python download_videos.py                 # Download videos from URLs (edit VIDEOS dict)
python merge_videos.py                    # Merge clips with FFmpeg
```

## Architecture

**Scripts overview:**

| Script | Purpose | Notes |
|--------|---------|-------|
| `app.py` | **Web UI** - Streamlit interface | Creates task, shows link to Kie.ai dashboard |
| `video_generator.py` | Full storyboard-to-video pipeline | Polling (may timeout) |
| `genera_da_storyboard.py` | Generate videos from saved storyboard | Polling |
| `genera_loop_video.py` | Single video with auto-download | Polling |
| `genera_video_presentazione.py` | Avatar/presenter videos | Callback |
| `download_videos.py` | Manual download from URLs | N/A |
| `merge_videos.py` | Merge clips via FFmpeg | N/A |

**Web UI (`app.py`) workflow:**
1. User enters prompt, selects duration and aspect ratio
2. App creates task via Kie.ai API
3. App shows task ID and link to Kie.ai dashboard
4. User checks video status on https://kie.ai/it/logs

**CLI workflow (`video_generator.py`):**
1. `generate_storyboard()` - Calls OpenRouter to create scene prompts
2. `create_video_task()` / `wait_for_video()` - Sends prompts to Kie.ai, polls for completion
3. `download_video()` - Downloads completed videos to `output/`
4. `create_ffmpeg_concat_script()` - Generates merge scripts

**Kie.ai API:**
- Base URL: `https://api.kie.ai/api/v1/jobs`
- Create task: `POST /createTask` returns `taskId`
- Query status: Not reliably available - use dashboard or callback
- Dashboard (logs): https://kie.ai/it/logs

**Kie.ai models:** `sora-2-text-to-video`, `sora-2-image-to-video`, `sora-2-pro-text-to-video`, `sora-2-pro-image-to-video`, `sora-watermark-remover`

## Configuration

Required in `.env`:
```
OPENROUTER_API_KEY=sk-or-v1-xxx
KIE_API_KEY=your-kie-key
```

Optional:
```
SITE_URL=https://your-site.com
SITE_NAME=YourAppName
```

## Costs

| Service | Cost |
|---------|------|
| Sora 2 (10s/15s) | $0.15 (30 credits) |
| Sora 2 Pro | $0.75-$3.15 (varies) |
| OpenRouter (Claude Sonnet) | ~$0.01-0.05 per storyboard |

**Credits:** 1 credit = $0.005

## Kie.ai API Details

See `docs/kie_api_reference.md` for full API documentation.

**Key request parameters:**
- `n_frames`: `"10"` (10s) or `"15"` (15s) - **must be string, not int**
- `aspect_ratio`: `"portrait"` or `"landscape"`
- `remove_watermark`: boolean
- `image_urls`: array of URLs (for image-to-video models)

**Response codes:** 200=success, 401=auth error, 402=insufficient credits, 429=rate limit

## Output Files

Generated files in `output/`:
- `scene_01.mp4`, `scene_02.mp4`, ... - Individual video clips
- `storyboard_YYYYMMDD_HHMMSS.json` - Generated storyboard
- `filelist.txt` - FFmpeg concat input
- `merge_videos.bat` / `merge_videos.sh` - Merge scripts
