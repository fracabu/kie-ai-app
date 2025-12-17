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

streamlit run app.py                      # Launch web UI
python video_generator.py                 # Full workflow: storyboard + video generation
python genera_da_storyboard.py            # Generate videos from existing storyboard JSON
python genera_video_presentazione.py      # Generate presenter/avatar videos (text or image-to-video)
python genera_loop_video.py               # Generate single 15s loop video with polling
python download_videos.py                 # Download videos from URLs (edit VIDEOS dict)
python merge_videos.py                    # Merge clips with FFmpeg
python test_callback.py                   # Test Kie.ai callback with webhook.site
```

## Architecture

**Scripts overview:**

| Script | Purpose | Kie.ai Method |
|--------|---------|---------------|
| `app.py` | **Web UI** - Streamlit interface | Polling |
| `video_generator.py` | Full storyboard-to-video pipeline | Polling |
| `genera_da_storyboard.py` | Generate videos from saved storyboard | Polling |
| `genera_loop_video.py` | Single video with auto-download | Polling |
| `genera_video_presentazione.py` | Avatar/presenter videos | Callback |
| `download_videos.py` | Manual download from URLs | N/A |
| `merge_videos.py` | Merge clips via FFmpeg | N/A |
| `test_callback.py` | API connectivity test | Callback |

**Main workflow (`video_generator.py`):**
1. `generate_storyboard()` - Calls OpenRouter to create scene prompts from business description
2. `create_video_task()` / `wait_for_video()` - Sends prompts to Kie.ai, polls for completion
3. `download_video()` - Downloads completed videos to `output/`
4. `create_ffmpeg_concat_script()` - Generates merge scripts (.bat and .sh)

**API patterns:**
- OpenRouter: Standard chat completions endpoint, model `anthropic/claude-sonnet-4`
- Kie.ai: Task-based async API - create task, poll/callback for results
  - Base URL: `https://api.kie.ai/api/v1/jobs`
  - Create: `POST /createTask` → returns `taskId`
  - Query: `POST /queryTask` with `{"taskId": "..."}`
  - **Polling**: Loop on queryTask until `state` is `success` or `fail` (2-5 min typical)
  - **Callback**: Add `callBackUrl` to createTask; Kie.ai POSTs result when done (use webhook.site for testing)

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
| Sora 2 Pro | $0.75-$3.15 (varies by duration/resolution) |
| OpenRouter (Claude Sonnet) | ~$0.01-0.05 per storyboard |

## Kie.ai API Details

See `docs/kie_api_reference.md` for full API documentation.

**Key request parameters:**
- `n_frames`: `"10"` (10s) or `"15"` (15s) - **must be string, not int**
- `aspect_ratio`: `"portrait"` or `"landscape"`
- `remove_watermark`: boolean
- `image_urls`: array of URLs (required for image-to-video models)

**Callback response parsing:**
```python
result_json = json.loads(callback_data["data"]["resultJson"])
video_url = result_json["resultUrls"][0]
```

**Polling response parsing:**
```python
data = result.get("data", {})
state = data.get("state")  # "success" or "fail"
result_json = json.loads(data.get("resultJson", "{}"))
video_urls = result_json.get("resultUrls", [])
```

**Response codes:** 200=success, 401=auth error, 402=insufficient credits, 429=rate limit
