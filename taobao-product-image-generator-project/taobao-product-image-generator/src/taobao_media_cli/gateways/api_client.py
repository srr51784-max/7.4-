from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional

from taobao_media_cli.config import MediaConfig
from taobao_media_cli.errors import ApiError, ConfigError


class MediaApiClient:
    """Small generic HTTP client for media-generation providers.

    This client intentionally keeps the provider contract simple and configurable.
    Set `api_base` and endpoint paths in config, then the CLI will POST JSON to
    the configured endpoint. It works with internal gateways, CyberBara-style
    wrappers, or any service that accepts bearer-token JSON requests.
    """

    def __init__(self, config: MediaConfig):
        self.config = config

    def _url(self, endpoint: str) -> str:
        if not self.config.api_base:
            raise ConfigError("Missing api_base. Run setup-api-key with --api-base or set TAOBAO_MEDIA_API_BASE.")
        base = self.config.api_base.rstrip("/")
        endpoint = endpoint if endpoint.startswith("/") else f"/{endpoint}"
        return f"{base}{endpoint}"

    def _headers(self) -> Dict[str, str]:
        if not self.config.api_key:
            raise ConfigError("Missing api_key. Run setup-api-key or set TAOBAO_MEDIA_API_KEY.")
        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "taobao-product-image-generator/0.1.0",
        }

    def post_json(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        request = urllib.request.Request(self._url(endpoint), data=body, headers=self._headers(), method="POST")
        try:
            with urllib.request.urlopen(request, timeout=self.config.timeout_seconds) as response:
                text = response.read().decode("utf-8")
                return json.loads(text) if text.strip() else {}
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ApiError(f"Provider HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise ApiError(f"Provider request failed: {exc.reason}") from exc

    def get_json(self, endpoint: str) -> Dict[str, Any]:
        request = urllib.request.Request(self._url(endpoint), headers=self._headers(), method="GET")
        try:
            with urllib.request.urlopen(request, timeout=self.config.timeout_seconds) as response:
                text = response.read().decode("utf-8")
                return json.loads(text) if text.strip() else {}
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ApiError(f"Provider HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise ApiError(f"Provider request failed: {exc.reason}") from exc

    def generate_image(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.post_json(self.config.image_endpoint, payload)

    def quote(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.post_json(self.config.quote_endpoint, payload)

    def wait_for_task(self, task_id: str, interval: int = 5, timeout: int = 900) -> Dict[str, Any]:
        start = time.time()
        while True:
            endpoint = self.config.task_endpoint_template.format(task_id=urllib.parse.quote(task_id, safe=""))
            result = self.get_json(endpoint)
            status = str(result.get("status", "")).lower()
            if status in {"succeeded", "success", "completed", "complete", "failed", "error", "cancelled", "canceled"}:
                return result
            if time.time() - start > timeout:
                raise ApiError(f"Timed out waiting for task {task_id}")
            time.sleep(interval)
