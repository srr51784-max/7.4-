# Taobao Product Image Generator Skill

A GitHub-ready AI Skill project for generating Taobao and ecommerce product image prompts and API requests.

It is inspired by the structure of `Ultimate-AI-Media-Generator-Skill`: a `SKILL.md` entrypoint, reusable references, workflow templates, and a Python CLI that can configure an API key, build prompts, estimate cost, generate image payloads, and submit requests to a provider.

## Features

- Generate Taobao/Tmall/JD/Pinduoduo product image prompts
- Build 1:1 main image prompts
- Build 1440x1920 detail image prompts
- Build white-background refinement prompts
- Expand one request into 5 or 10 independent image payloads
- Preserve product shape and viewing angle by default
- Support common ecommerce styles:
  - blue business
  - deep blue business
  - red promotion
  - Apple-style minimal
  - white clean product-only
- Generic API adapter for image generation providers
- Local credit estimator before submission

## Folder Structure

```text
taobao-product-image-generator/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── scripts/
│   └── taobao_media.py
├── src/
│   └── taobao_media_cli/
│       ├── cli.py
│       ├── config.py
│       ├── errors.py
│       ├── gateways/
│       │   └── api_client.py
│       ├── policies/
│       │   └── credit_policy.py
│       └── usecases/
│           ├── generate.py
│           └── prompt_builder.py
├── references/
│   ├── api-contract.md
│   └── prompt-library.md
├── workflows/
│   ├── detail-image.md
│   └── taobao-main-image.md
└── examples/
    └── taobao-main-image.json
```

## Quick Start

### 1) Generate prompts only

```bash
python3 scripts/taobao_media.py prompt \
  --product "汽车减震器" \
  --image-type main \
  --style blue-business \
  --ratio 1:1 \
  --count 5 \
  --store-name "广州君成贸易有限公司"
```

### 2) Expand one request into batch payloads

```bash
python3 scripts/taobao_media.py batch \
  --json examples/taobao-main-image.json \
  --output batch-payloads.json
```

### 3) Estimate credits locally

```bash
python3 scripts/taobao_media.py quote --json '{"media_type":"image","model":"standard-image","count":5,"resolution":"1k"}'
```

### 4) Configure a provider API

```bash
python3 scripts/taobao_media.py setup-api-key "<your_api_key>" \
  --api-base "https://your-provider.example" \
  --image-endpoint "/generate-image" \
  --quote-endpoint "/quote" \
  --task-endpoint-template "/tasks/{task_id}"
```

The config is saved to:

```text
~/.config/taobao-media-generator/config.json
```

You can also use environment variables:

```bash
export TAOBAO_MEDIA_API_KEY="<your_api_key>"
export TAOBAO_MEDIA_API_BASE="https://your-provider.example"
```

### 5) Submit an image request

```bash
python3 scripts/taobao_media.py generate-image --json '{
  "product":"汽车减震器",
  "image_type":"main",
  "style":"blue-business",
  "ratio":"1:1",
  "model":"standard-image"
}'
```

Dry run without sending:

```bash
python3 scripts/taobao_media.py generate-image --dry-run --json examples/taobao-main-image.json
```

## Common Prompt Fields

| Field | Example | Meaning |
|---|---|---|
| `product` | `汽车减震器` | Product name or listing title |
| `image_type` | `main` | `main`, `detail`, `white`, `poster`, `comparison`, `edit` |
| `style` | `blue-business` | Visual style preset |
| `ratio` | `1:1` | Aspect ratio or target size |
| `count` | `5` | Number of independent prompts/payloads |
| `store_name` | `广州君成贸易有限公司` | Optional store name on image |
| `watermark` | `zhengpin` | Optional watermark text |
| `keep_shape` | `true` | Preserve product geometry |
| `remove_packaging` | `false` | Remove package box/background clutter |
| `extra` | `不要写质保` | Extra requirement |

## Style Presets

- `blue-business`
- `deep-blue-business`
- `red-promo`
- `apple-minimal`
- `white-clean`
- `black-premium`

## Install as a Skill

Package or upload this directory as a Skill. The required entrypoint is `SKILL.md`; `agents/openai.yaml` provides UI metadata.

If publishing on GitHub, users can install with their Skill manager, for example:

```bash
npx skills add <your-github-name>/taobao-product-image-generator --all
```

## Provider Integration

This project does not lock you into one vendor. It sends JSON to a configurable endpoint:

```json
{
  "media_type": "image",
  "model": "standard-image",
  "prompt": "...",
  "size": "1:1"
}
```

Your backend gateway should translate that payload into the exact API format required by your image provider.

## Notes

- The CLI uses Python standard library only.
- Local `quote` is an estimate. The provider’s billing is authoritative.
- Product geometry preservation is a prompt-level instruction. Final fidelity depends on the model and provider.
