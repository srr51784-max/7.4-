#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/taobao_media.py prompt --product "汽车减震器" --image-type main --style blue-business --ratio 1:1 --count 2 >/tmp/taobao_prompt_test.json
python3 scripts/taobao_media.py quote --json '{"media_type":"image","model":"standard-image","count":5,"resolution":"1k"}' >/tmp/taobao_quote_test.json
python3 scripts/taobao_media.py generate-image --dry-run --json examples/taobao-main-image.json >/tmp/taobao_dry_run_test.json
printf 'smoke tests passed\n'
