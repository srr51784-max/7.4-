from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

from taobao_media_cli.config import load_config, update_config
from taobao_media_cli.errors import MediaGeneratorError
from taobao_media_cli.gateways.api_client import MediaApiClient
from taobao_media_cli.policies.credit_policy import estimate_credits
from taobao_media_cli.usecases.generate import build_batch_payloads, generate_image
from taobao_media_cli.usecases.prompt_builder import PromptRequest, build_prompts, request_from_dict


def _json_loads(value: str) -> Dict[str, Any]:
    path = Path(value)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return json.loads(value)


def _print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def cmd_setup_api_key(args: argparse.Namespace) -> None:
    config = update_config(
        api_key=args.api_key,
        api_base=args.api_base,
        provider=args.provider,
        image_endpoint=args.image_endpoint,
        quote_endpoint=args.quote_endpoint,
        task_endpoint_template=args.task_endpoint_template,
    )
    _print_json({"ok": True, "config": config.safe_dict()})


def cmd_config(_: argparse.Namespace) -> None:
    _print_json(load_config().safe_dict())


def cmd_prompt(args: argparse.Namespace) -> None:
    if args.json:
        req = request_from_dict(_json_loads(args.json))
    else:
        req = PromptRequest(
            product=args.product,
            image_type=args.image_type,
            style=args.style,
            ratio=args.ratio,
            count=args.count,
            platform=args.platform,
            store_name=args.store_name,
            watermark=args.watermark,
            keep_shape=not args.allow_shape_change,
            remove_packaging=args.remove_packaging,
            extra=args.extra,
        )
    _print_json({"prompts": build_prompts(req)})


def cmd_quote(args: argparse.Namespace) -> None:
    payload = _json_loads(args.json)
    if args.provider:
        client = MediaApiClient(load_config())
        _print_json(client.quote(payload))
    else:
        _print_json(estimate_credits(payload))


def cmd_generate_image(args: argparse.Namespace) -> None:
    payload = _json_loads(args.json)
    client = MediaApiClient(load_config())
    _print_json(generate_image(client, payload, dry_run=args.dry_run))


def cmd_batch(args: argparse.Namespace) -> None:
    payload = _json_loads(args.json)
    payloads = build_batch_payloads(payload)
    if args.output:
        Path(args.output).write_text(json.dumps(payloads, ensure_ascii=False, indent=2), encoding="utf-8")
        _print_json({"ok": True, "count": len(payloads), "output": args.output})
    else:
        _print_json({"count": len(payloads), "payloads": payloads})


def cmd_wait(args: argparse.Namespace) -> None:
    client = MediaApiClient(load_config())
    _print_json(client.wait_for_task(args.task_id, interval=args.interval, timeout=args.timeout))


def cmd_models(_: argparse.Namespace) -> None:
    _print_json({
        "models": [
            {"model": "draft-image", "media_type": "image", "use": "low-cost draft prompts"},
            {"model": "standard-image", "media_type": "image", "use": "default ecommerce main/detail images"},
            {"model": "premium-image", "media_type": "image", "use": "high-quality hero images"},
            {"model": "nano-banana-pro", "media_type": "image", "use": "provider-specific option if supported"},
            {"model": "gpt-image", "media_type": "image", "use": "provider-specific option if supported"},
        ],
        "note": "local model aliases; your provider may expose different exact model names",
    })


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Taobao ecommerce AI image generation helper")
    sub = parser.add_subparsers(dest="command", required=True)

    setup = sub.add_parser("setup-api-key", help="store provider API key and optional endpoint settings")
    setup.add_argument("api_key")
    setup.add_argument("--api-base")
    setup.add_argument("--provider", default="generic")
    setup.add_argument("--image-endpoint", default="/generate-image")
    setup.add_argument("--quote-endpoint", default="/quote")
    setup.add_argument("--task-endpoint-template", default="/tasks/{task_id}")
    setup.set_defaults(func=cmd_setup_api_key)

    config = sub.add_parser("config", help="show current safe configuration")
    config.set_defaults(func=cmd_config)

    prompt = sub.add_parser("prompt", help="build ecommerce image prompts")
    prompt.add_argument("--json", help="json string or path containing prompt fields")
    prompt.add_argument("--product", default="未命名产品")
    prompt.add_argument("--image-type", default="main", choices=["main", "detail", "white", "poster", "comparison", "edit"])
    prompt.add_argument("--style", default="blue-business")
    prompt.add_argument("--ratio", default="1:1")
    prompt.add_argument("--count", type=int, default=1)
    prompt.add_argument("--platform", default="淘宝")
    prompt.add_argument("--store-name")
    prompt.add_argument("--watermark")
    prompt.add_argument("--allow-shape-change", action="store_true")
    prompt.add_argument("--remove-packaging", action="store_true")
    prompt.add_argument("--extra")
    prompt.set_defaults(func=cmd_prompt)

    quote = sub.add_parser("quote", help="estimate local credits or call provider quote endpoint")
    quote.add_argument("--json", required=True, help="json string or path")
    quote.add_argument("--provider", action="store_true", help="call configured provider quote endpoint")
    quote.set_defaults(func=cmd_quote)

    generate = sub.add_parser("generate-image", help="submit image generation request to configured provider")
    generate.add_argument("--json", required=True, help="json string or path")
    generate.add_argument("--dry-run", action="store_true", help="print enriched payload without sending request")
    generate.set_defaults(func=cmd_generate_image)

    batch = sub.add_parser("batch", help="expand one ecommerce request into independent image payloads")
    batch.add_argument("--json", required=True, help="json string or path")
    batch.add_argument("--output", help="optional output path for expanded payloads")
    batch.set_defaults(func=cmd_batch)

    wait = sub.add_parser("wait", help="poll configured provider task endpoint")
    wait.add_argument("--task-id", required=True)
    wait.add_argument("--interval", type=int, default=5)
    wait.add_argument("--timeout", type=int, default=900)
    wait.set_defaults(func=cmd_wait)

    models = sub.add_parser("models", help="show local model aliases")
    models.set_defaults(func=cmd_models)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
        return 0
    except MediaGeneratorError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except (json.JSONDecodeError, ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
