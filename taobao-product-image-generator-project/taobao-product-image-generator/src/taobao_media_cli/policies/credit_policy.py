from __future__ import annotations

from typing import Any, Dict

# Local estimate table. Replace values with provider-specific numbers if needed.
IMAGE_BASE_CREDITS = {
    "draft-image": 1.0,
    "standard-image": 2.0,
    "premium-image": 4.0,
    "nano-banana-pro": 4.0,
    "gpt-image": 4.0,
}

RESOLUTION_MULTIPLIER = {
    "512": 0.75,
    "768": 0.9,
    "1k": 1.0,
    "1024x1024": 1.0,
    "1440x1920": 1.8,
    "2k": 2.0,
    "4k": 4.0,
}


def estimate_credits(payload: Dict[str, Any]) -> Dict[str, Any]:
    media_type = str(payload.get("media_type", "image"))
    model = str(payload.get("model", "standard-image"))
    count = int(payload.get("count") or payload.get("n") or 1)
    resolution = str(payload.get("resolution") or payload.get("size") or "1k")

    if media_type != "image":
        return {
            "estimated_credits": None,
            "can_estimate": False,
            "reason": "local estimator currently supports image requests only",
        }

    base = IMAGE_BASE_CREDITS.get(model, IMAGE_BASE_CREDITS["standard-image"])
    multiplier = RESOLUTION_MULTIPLIER.get(resolution, 1.0)
    total = round(base * multiplier * count, 2)
    return {
        "estimated_credits": total,
        "can_estimate": True,
        "media_type": media_type,
        "model": model,
        "count": count,
        "resolution": resolution,
        "note": "local estimate only; provider billing is authoritative",
    }
