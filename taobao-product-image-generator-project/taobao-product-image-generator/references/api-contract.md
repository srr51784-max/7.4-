# API Contract

The CLI uses a generic JSON-over-HTTP contract so it can connect to most image providers through a small gateway service.

## Configuration

Run:

```bash
python3 scripts/taobao_media.py setup-api-key "<api_key>" --api-base "https://your-provider.example"
```

Or set environment variables:

```bash
export TAOBAO_MEDIA_API_KEY="<api_key>"
export TAOBAO_MEDIA_API_BASE="https://your-provider.example"
```

Optional endpoint overrides:

```bash
python3 scripts/taobao_media.py setup-api-key "<api_key>" \
  --api-base "https://your-provider.example" \
  --image-endpoint "/generate-image" \
  --quote-endpoint "/quote" \
  --task-endpoint-template "/tasks/{task_id}"
```

## Generate Image Request

The CLI sends a `POST` request to the configured image endpoint.

```json
{
  "media_type": "image",
  "model": "standard-image",
  "prompt": "...",
  "size": "1:1",
  "reference_images": ["https://example.com/reference.png"],
  "batch_index": 1
}
```

Expected response can be provider-specific. Recommended fields:

```json
{
  "task_id": "task_123",
  "status": "submitted",
  "output_url": null
}
```

## Wait Request

The CLI sends `GET /tasks/{task_id}` using the configured task endpoint template.

Recommended terminal statuses:

- `succeeded`
- `success`
- `completed`
- `complete`
- `failed`
- `error`
- `cancelled`
- `canceled`

## Local Quote

`quote` defaults to local estimation. Add `--provider` to call the remote quote endpoint.
