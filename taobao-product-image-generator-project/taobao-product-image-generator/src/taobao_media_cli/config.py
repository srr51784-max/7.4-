from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Optional

CONFIG_DIR = Path.home() / ".config" / "taobao-media-generator"
CONFIG_FILE = CONFIG_DIR / "config.json"


@dataclass
class MediaConfig:
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    provider: str = "generic"
    image_endpoint: str = "/generate-image"
    quote_endpoint: str = "/quote"
    task_endpoint_template: str = "/tasks/{task_id}"
    timeout_seconds: int = 120

    def safe_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if data.get("api_key"):
            data["api_key"] = "***" + data["api_key"][-4:]
        return data


def load_config() -> MediaConfig:
    data: Dict[str, Any] = {}
    if CONFIG_FILE.exists():
        data.update(json.loads(CONFIG_FILE.read_text(encoding="utf-8")))

    env_key = os.getenv("TAOBAO_MEDIA_API_KEY") or os.getenv("MEDIA_API_KEY") or os.getenv("CYBERBARA_API_KEY")
    env_base = os.getenv("TAOBAO_MEDIA_API_BASE") or os.getenv("MEDIA_API_BASE")
    env_provider = os.getenv("TAOBAO_MEDIA_PROVIDER")

    if env_key:
        data["api_key"] = env_key
    if env_base:
        data["api_base"] = env_base
    if env_provider:
        data["provider"] = env_provider

    return MediaConfig(**{k: v for k, v in data.items() if k in MediaConfig.__annotations__})


def save_config(config: MediaConfig) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(asdict(config), ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        CONFIG_FILE.chmod(0o600)
    except OSError:
        pass


def update_config(**kwargs: Any) -> MediaConfig:
    config = load_config()
    for key, value in kwargs.items():
        if value is not None and hasattr(config, key):
            setattr(config, key, value)
    save_config(config)
    return config
