---
name: taobao-product-image-generator
description: generate taobao, tmall, jd, pinduoduo, and ecommerce product images with ai. use when the user asks for product main images, 1:1 listing visuals, 1440x1920 detail images, white-background product refinements, batch ecommerce images, product background replacement, product poster copy, or api-based image generation workflows for online store assets.
---

# Taobao Product Image Generator

## Objective

Use this skill to turn ecommerce product requirements into platform-ready image generation requests. Prioritize Taobao-style commercial clarity: product-first composition, short selling points, clean layout, accurate aspect ratio, and consistent visual identity.

## Standard Workflow

1. Identify the requested output type: `main`, `detail`, `white`, `poster`, `comparison`, or `batch`.
2. Preserve concrete product constraints from the user, especially product shape, angle, visible accessories, packaging removal, watermark text, store name, ratio, and platform.
3. Build a concise ecommerce prompt using `references/prompt-library.md` and `workflows/taobao-main-image.md` when needed.
4. Use `scripts/taobao_media.py prompt` for prompt-only work, `quote` for local cost estimate, or `generate-image` for an API submission.
5. Return each requested image as an independent output. Do not merge multiple requested images into a collage unless the user explicitly asks for a combined display image.

## Image Type Rules

### Main image
- Default ratio: `1:1`.
- Keep the product large, centered, and clear.
- Use short text blocks only; avoid dense copy.
- Make the first image more click-driven than the rest.

### Detail image
- Default size: `1440x1920`.
- Use vertical spacing, section labels, and one idea per image.
- Do not repeat the same selling point across a batch unless the user requests repetition.

### White-background refinement
- Show the product only on a pure or near-pure white background.
- Do not add text, badges, icons, decorations, props, packaging, or scene elements.
- Improve sharpness and lighting without changing the product structure.

### Product edit
- Keep the provided product’s visible geometry intact.
- Remove only the requested region or background elements.
- When the user says “不要改变产品形状”, treat product structure preservation as the highest priority.

## Ecommerce Copy Rules

Use compact Chinese copy for Chinese marketplace assets. Prefer 4–8 Chinese characters per badge and no more than 2–4 badges per main image.

Good short phrases:
- 品牌正版授权
- 高清实拍质感
- 精准适配车型
- 加厚耐用材质
- 蓝色商务风
- 白底精修展示
- 店铺名露出

Avoid unverified claims such as official authorization, warranty, original factory status, or brand history unless the user provided the information or asked to include it as marketing copy. If a claim is uncertain, phrase it as a design label only, or omit it.

## CLI Usage

Generate prompts only:

```bash
python3 scripts/taobao_media.py prompt --product "汽车减震器" --image-type main --style blue-business --ratio 1:1 --count 5 --store-name "广州君成贸易有限公司"
```

Estimate local credits:

```bash
python3 scripts/taobao_media.py quote --json '{"media_type":"image","model":"standard-image","count":5,"resolution":"1k"}'
```

Submit a request to a configured API provider:

```bash
python3 scripts/taobao_media.py generate-image --json '{"prompt":"淘宝主图，蓝色商务风，汽车减震器居中放大展示","size":"1024x1024"}'
```

Configure API key:

```bash
python3 scripts/taobao_media.py setup-api-key "<api_key>" --api-base "https://your-provider.example"
```

## References

- Use `references/prompt-library.md` for reusable ecommerce prompts.
- Use `references/api-contract.md` for the configurable API payload contract.
- Use `workflows/taobao-main-image.md` for batch main-image procedure.
- Use `workflows/detail-image.md` for vertical detail-page procedure.
