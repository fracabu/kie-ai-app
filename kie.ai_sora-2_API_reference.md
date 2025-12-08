# Kie.ai Sora 2 API Reference

## Authentication

All APIs require authentication via Bearer Token.

```
Authorization: Bearer YOUR_API_KEY
```

Get API Key: https://kie.ai/api-key

## Endpoints

### POST /api/v1/jobs/createTask

Create a new generation task.

**Base URL:** `https://api.kie.ai`

#### Request Body Structure

```json
{
  "model": "string",
  "callBackUrl": "string (optional)",
  "input": {
    "prompt": "string",
    "aspect_ratio": "portrait | landscape",
    "n_frames": "10 | 15",
    "remove_watermark": true
  }
}
```

#### Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| model | Yes | string | Model name: `sora-2-text-to-video` |
| callBackUrl | No | string | Callback URL for task completion notifications |
| input.prompt | Yes | string | Text prompt (max 10000 chars) |
| input.aspect_ratio | No | string | `portrait` or `landscape` |
| input.n_frames | No | string | `10` (10s) or `15` (15s) |
| input.remove_watermark | No | boolean | Remove watermark (true/false) |

#### Request Example (cURL)

```bash
curl -X POST "https://api.kie.ai/api/v1/jobs/createTask" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "model": "sora-2-text-to-video",
    "callBackUrl": "https://your-domain.com/api/callback",
    "input": {
      "prompt": "A professor stands at the front of a lively classroom...",
      "aspect_ratio": "landscape",
      "n_frames": "10",
      "remove_watermark": true
    }
}'
```

#### Response Example

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "taskId": "task_12345678"
  }
}
```

#### Response Fields

| Field | Description |
|-------|-------------|
| code | Status code, 200 for success |
| message | Response message |
| data.taskId | Task ID for querying status |

---

## Callback Notifications

When `callBackUrl` is provided, the system sends POST requests to that URL upon task completion.

### Success Callback Example

```json
{
    "code": 200,
    "data": {
        "completeTime": 1755599644000,
        "consumeCredits": 100,
        "costTime": 8,
        "createTime": 1755599634000,
        "model": "sora-2-text-to-video",
        "param": "{...original request params...}",
        "remainedCredits": 2510330,
        "resultJson": "{\"resultUrls\":[\"https://example.com/video.mp4\"],\"resultWaterMarkUrls\":[\"https://example.com/video-watermark.mp4\"]}",
        "state": "success",
        "taskId": "e989621f54392584b05867f87b160672",
        "updateTime": 1755599644000
    },
    "msg": "Playground task completed successfully."
}
```

### Failure Callback Example

```json
{
    "code": 501,
    "data": {
        "completeTime": 1755597081000,
        "consumeCredits": 0,
        "costTime": 0,
        "createTime": 1755596341000,
        "failCode": "500",
        "failMsg": "Internal server error",
        "model": "sora-2-text-to-video",
        "param": "{...original request params...}",
        "remainedCredits": 2510430,
        "state": "fail",
        "taskId": "bd3a37c523149e4adf45a3ddb5faf1a8",
        "updateTime": 1755597097000
    },
    "msg": "Playground task failed."
}
```

### Callback Data Fields

| Field | Description |
|-------|-------------|
| state | `success` or `fail` |
| taskId | Task identifier |
| resultJson | JSON string with `resultUrls` (video URLs) |
| consumeCredits | Credits used |
| remainedCredits | Remaining credits |
| costTime | Processing time (seconds) |
| failCode | Error code (on failure) |
| failMsg | Error message (on failure) |

---

## POST /api/v1/jobs/queryTask

Query task status (endpoint to be confirmed).

```bash
curl -X POST "https://api.kie.ai/api/v1/jobs/queryTask" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"taskId": "your-task-id"}'
```

---

## Models Available

| Model | Description |
|-------|-------------|
| sora-2-text-to-video | Text to video (10s) |
| sora-2-image-to-video | Image to video |
| sora-2-pro-text-to-video | Pro text to video (10s/15s, 720p/1080p) |
| sora-2-pro-image-to-video | Pro image to video |
| sora-watermark-remover | Remove watermarks |
| sora-2-pro-storyboard | Multi-scene storyboard |

---

## Pricing

| Model | Cost |
|-------|------|
| Sora 2 | 30 credits ($0.15) per 10s video |
| Sora 2 Pro Standard | 150 credits ($0.75) per 10s, 270 credits ($1.35) per 15s |
| Sora 2 Pro HD | 330 credits ($1.65) per 10s, 630 credits ($3.15) per 15s |
| Watermark Remover | 10 credits ($0.05) per use |

---

## Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 401 | Unauthorized - Invalid API key |
| 402 | Insufficient Credits |
| 404 | Not Found |
| 422 | Validation Error |
| 429 | Rate Limited |
| 455 | Service Unavailable |
| 500 | Server Error |
| 505 | Feature Disabled |
