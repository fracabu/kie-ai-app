# AI Video Generator

\![CI](https://github.com/fracabu/kie-ai-app/actions/workflows/ci.yml/badge.svg)

Generate promotional videos using OpenRouter (AI storyboard) + Kie.ai Sora 2 (video generation).

## 📺 Demo & Media

\![Kie AI Infographic](assets/kie-ai-infographic.png)

> 🎬 **Video Demo**: Coming soon  
> 🎙️ **Podcast**: Coming soon

## Features

- **Automated Storyboard Generation**: Uses Claude AI via OpenRouter to create cinematic scene prompts from a business description
- **AI Video Generation**: Sends prompts to Kie.ai Sora 2 for text-to-video and image-to-video generation
- **Multiple Workflows**: Full pipeline, single videos, presenter/avatar videos
- **Video Merging**: FFmpeg integration to combine clips into final video

## Quick Start

### 1. Install Dependencies

### 2. Configure API Keys

Edit \ with your keys:
Get API keys:
- OpenRouter: https://openrouter.ai/keys
- Kie.ai: https://kie.ai/api-key

### 3. Run

## Scripts

| Script | Description |
|--------|-------------|
| \ | Full workflow: storyboard generation + video creation |
| \ | Generate single 15s video with auto-download |
| \ | Generate presenter/avatar videos |
| \ | Download videos from Kie.ai URLs |
| \ | Merge video clips using FFmpeg |
| \ | Test Kie.ai API with webhook callback |

## How It Works

## Kie.ai Models

| Model | Description |
|-------|-------------|
| \ | Text prompt to 10s/15s video |
| \ | Animate an image |
| \ | Pro quality (720p/1080p) |
| \ | Pro image animation |
| \ | Remove watermarks |

## Pricing

| Service | Cost |
|---------|------|
| Sora 2 (10s) | \/usr/bin/bash.15 (30 credits) |
| Sora 2 (15s) | \/usr/bin/bash.15 (30 credits) |
| Sora 2 Pro Standard | \/usr/bin/bash.75-\.35 |
| Sora 2 Pro HD | \.65-\.15 |
| OpenRouter (Claude) | ~\/usr/bin/bash.01-0.05 per storyboard |

## Output

Generated videos are saved to the \ directory:
- \, \, ... - Individual clips
- \ - Generated storyboard
- \ - FFmpeg concat list
- \ / \ - Merge scripts

## Requirements

- Python 3.10+
- FFmpeg (for video merging)
- OpenRouter API key
- Kie.ai API key

## License

MIT
