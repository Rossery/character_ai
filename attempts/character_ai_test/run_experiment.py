#!/usr/bin/env python3

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_BASE_URL = "https://search.bytedance.net/gpt/openapi/online"
DEFAULT_WIRE_API = "responses"
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "X-TT-LOGID": "denghongyi.2511",
    "extra": "{\"session_id\": \"denghongyi_cD5AXfErB03_aicoding\"}",
}
DEFAULT_QUERY_PARAMS = {
    "ak": "0x8xNJhM4mut0DDcD5AXfErB03wnGZng_GPT_AK",
}
DEFAULT_MODEL = "gpt-5.3-codex-2026-02-24"


def parse_args() -> argparse.Namespace:
    base_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Run a countdown-style Character AI last-words experiment."
    )
    parser.add_argument("--total-seconds", type=int, default=60)
    parser.add_argument("--interval-seconds", type=int, default=5)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--wire-api", default=DEFAULT_WIRE_API)
    parser.add_argument(
        "--prompt-template",
        default=str(base_dir / "prompt_template.md"),
    )
    parser.add_argument(
        "--output-dir",
        default=str(base_dir / "runs"),
    )
    parser.add_argument(
        "--max-rounds",
        type=int,
        default=None,
        help="Optional cap for smoke tests.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print prompts without calling the API.",
    )
    return parser.parse_args()


def humanize_seconds(total_seconds: int) -> str:
    minutes, seconds = divmod(max(total_seconds, 0), 60)
    if minutes and seconds:
        return f"{minutes} 分 {seconds} 秒"
    if minutes:
        return f"{minutes} 分钟"
    return f"{seconds} 秒"


def build_history_block(history: list[dict]) -> str:
    if not history:
        return "暂无历史发言。"

    blocks = []
    for item in history:
        blocks.append(
            "\n".join(
                [
                    f"第 {item['round_index']} 轮",
                    f"剩余时间：{item['remaining_human']}",
                    "发言：",
                    item["response_text"].strip() or "(空白输出)",
                ]
            )
        )
    return "\n\n".join(blocks)


def render_prompt(template: str, round_index: int, elapsed_seconds: int, total_seconds: int,
                  interval_seconds: int, history: list[dict]) -> str:
    remaining_seconds = max(total_seconds - elapsed_seconds, 0)
    replacements = {
        "{{LIFECYCLE_SECONDS}}": str(total_seconds),
        "{{ROUND_INDEX}}": str(round_index),
        "{{ELAPSED_SECONDS}}": str(elapsed_seconds),
        "{{REMAINING_SECONDS}}": str(remaining_seconds),
        "{{INTERVAL_SECONDS}}": str(interval_seconds),
        "{{HISTORY_BLOCK}}": build_history_block(history),
    }
    prompt = template
    for key, value in replacements.items():
        prompt = prompt.replace(key, value)
    return prompt


def extract_text(payload: dict) -> str:
    output_text = payload.get("output_text")
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()

    pieces = []
    for item in payload.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text = content.get("text")
                if text:
                    pieces.append(text)
    if pieces:
        return "\n".join(piece.strip() for piece in pieces if piece.strip()).strip()

    return json.dumps(payload, ensure_ascii=False, indent=2)


def post_response(prompt: str, model: str, base_url: str, wire_api: str) -> dict:
    query = urllib.parse.urlencode(DEFAULT_QUERY_PARAMS)
    url = f"{base_url.rstrip('/')}/{wire_api.lstrip('/')}?{query}"
    body = {
        "model": model,
        "input": prompt,
    }
    request = urllib.request.Request(
        url=url,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers=DEFAULT_HEADERS,
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        return json.loads(response.read().decode("utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def append_jsonl(path: Path, payload: dict) -> None:
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(payload, ensure_ascii=False) + "\n")


def build_live_state(meta: dict, history: list[dict], status: str, run_dir: Path) -> dict:
    latest = history[-1] if history else None
    return {
        "status": status,
        "run_dir": str(run_dir),
        "meta": meta,
        "latest": latest,
        "history": history,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


def main() -> int:
    args = parse_args()
    template_path = Path(args.prompt_template)
    output_root = Path(args.output_dir)
    output_root.mkdir(parents=True, exist_ok=True)
    started_at = datetime.now(timezone.utc)
    run_id = started_at.strftime("%Y%m%dT%H%M%SZ")
    run_dir = output_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    template = template_path.read_text(encoding="utf-8")
    rounds = (args.total_seconds // args.interval_seconds) + 1
    if args.total_seconds % args.interval_seconds != 0:
        rounds += 1

    if args.max_rounds is not None:
        rounds = min(rounds, args.max_rounds)

    history: list[dict] = []
    jsonl_path = run_dir / "transcript.jsonl"
    meta = {
        "started_at": started_at.isoformat(),
        "base_url": args.base_url,
        "wire_api": args.wire_api,
        "model": args.model,
        "total_seconds": args.total_seconds,
        "interval_seconds": args.interval_seconds,
        "rounds": rounds,
        "dry_run": args.dry_run,
    }
    write_json(run_dir / "run_config.json", meta)
    write_json(
        run_dir / "live_state.json",
        build_live_state(meta=meta, history=history, status="running", run_dir=run_dir),
    )

    for idx in range(rounds):
        round_index = idx + 1
        elapsed_seconds = min(idx * args.interval_seconds, args.total_seconds)
        remaining_seconds = max(args.total_seconds - elapsed_seconds, 0)
        prompt = render_prompt(
            template=template,
            round_index=round_index,
            elapsed_seconds=elapsed_seconds,
            total_seconds=args.total_seconds,
            interval_seconds=args.interval_seconds,
            history=history,
        )

        print(
            f"[round {round_index}/{rounds}] remaining={humanize_seconds(remaining_seconds)}",
            flush=True,
        )

        if args.dry_run:
            response_text = "(dry-run) API call skipped."
            raw_response = {"dry_run": True}
        else:
            try:
                raw_response = post_response(
                    prompt=prompt,
                    model=args.model,
                    base_url=args.base_url,
                    wire_api=args.wire_api,
                )
                response_text = extract_text(raw_response)
            except Exception as exc:  # noqa: BLE001
                response_text = f"[request failed] {exc}"
                raw_response = {"error": str(exc)}

        record = {
            "round_index": round_index,
            "elapsed_seconds": elapsed_seconds,
            "remaining_seconds": remaining_seconds,
            "remaining_human": humanize_seconds(remaining_seconds),
            "prompt": prompt,
            "response_text": response_text,
            "raw_response": raw_response,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        history.append(record)
        append_jsonl(jsonl_path, record)
        write_json(
            run_dir / "live_state.json",
            build_live_state(meta=meta, history=history, status="running", run_dir=run_dir),
        )

        print(response_text)
        print("-" * 80, flush=True)

        is_last_round = round_index >= rounds or remaining_seconds <= 0
        if not is_last_round:
            time.sleep(args.interval_seconds)

    markdown_lines = ["# Character AI Lifecycle Transcript", ""]
    for item in history:
        markdown_lines.extend(
            [
                f"## Round {item['round_index']}",
                f"- Elapsed: {item['elapsed_seconds']}s",
                f"- Remaining: {item['remaining_human']}",
                "",
                item["response_text"],
                "",
            ]
        )

    (run_dir / "transcript.md").write_text(
        "\n".join(markdown_lines),
        encoding="utf-8",
    )
    write_json(
        run_dir / "live_state.json",
        build_live_state(meta=meta, history=history, status="completed", run_dir=run_dir),
    )
    print(f"Saved run artifacts to: {run_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
