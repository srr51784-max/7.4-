from __future__ import annotations

from typing import Any, Dict, List

from taobao_media_cli.gateways.api_client import MediaApiClient
from taobao_media_cli.usecases.prompt_builder import build_prompts, request_from_dict


def enrich_generation_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Build a provider payload from ecommerce fields when prompt is absent."""
    enriched = dict(payload)
    if "prompt" not in enriched:
        req = request_from_dict(enriched)
        prompts = build_prompts(req)
        enriched["prompt"] = prompts[0]["prompt"]
        enriched["prompt_batch"] = prompts
    enriched.setdefault("media_type", "image")
    enriched.setdefault("size", enriched.get("ratio", "1:1"))
    return enriched


def generate_image(client: MediaApiClient, payload: Dict[str, Any], dry_run: bool = False) -> Dict[str, Any]:
    enriched = enrich_generation_payload(payload)
    if dry_run:
        return {"dry_run": True, "payload": enriched}
    return client.generate_image(enriched)


def build_batch_payloads(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    req = request_from_dict(payload)
    prompts = build_prompts(req)
    base = dict(payload)
    base.pop("prompt", None)
    base.setdefault("media_type", "image")
    base.setdefault("size", req.ratio)
    return [{**base, "prompt": item["prompt"], "batch_index": idx + 1} for idx, item in enumerate(prompts)]
