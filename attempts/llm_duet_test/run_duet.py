#!/usr/bin/env python3

import argparse
import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


MODEL_A = {
    "speaker_id": "gemini",
    "display_name": "Gemini 3 Pro",
    "model": "gemini-3-pro-preview-new",
    "url": (
        "https://aidp.bytedance.net/api/modelhub/online/v2/crawl"
        "?ak=s4AVzfUbrSbww1mctbhzUJUD6PND5YjI_GPT_AK"
    ),
    "log_id": "denghongyi.2511",
}

MODEL_B = {
    "speaker_id": "gpt",
    "display_name": "GPT-5.4",
    "model": "gpt-5.4-2026-03-05",
    "url": (
        "https://aidp.bytedance.net/api/modelhub/online/v2/crawl"
        "?ak=0x8xNJhM4mut0DDcD5AXfErB03wnGZng_GPT_AK"
    ),
    "log_id": "denghongyi.2511",
}

DEFAULT_OPENING = "hello"
DEFAULT_TURNS = 20
DEFAULT_MAX_TOKENS = 2048
HISTORY_REDACTION_PATTERNS = [
    r"\bgpt\b",
    r"\bgemini\b",
    r"\bllm\b",
    r"\bmodel\b",
    r"\bapi\b",
    r"\bprompt\b",
    r"\bassistant\b",
    r"\buser\b",
    r"\bsystem\b",
    r"\btoken\b",
    r"\bquota\b",
    r"\bpaygo\b",
    r"\bptu\b",
    r"\bhttp\b",
    r"\b429\b",
    r"request failed",
    r"rate[- ]?limit",
    r"too many requests",
    r"frontier model",
    r"ai",
    r"模型",
    r"对话实验",
    r"提示词",
    r"系统提示",
    r"配额",
    r"限流",
]


def parse_args() -> argparse.Namespace:
    base_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Let two LLMs talk to each other.")
    parser.add_argument("--turns", type=int, default=DEFAULT_TURNS)
    parser.add_argument("--opening", default=DEFAULT_OPENING)
    parser.add_argument("--output-dir", default=str(base_dir / "runs"))
    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip network requests and emit placeholder text.",
    )
    return parser.parse_args()


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def append_jsonl(path: Path, payload: dict) -> None:
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(payload, ensure_ascii=False) + "\n")


def extract_text(payload: dict) -> str:
    if isinstance(payload.get("output_text"), str) and payload["output_text"].strip():
        return payload["output_text"].strip()

    choices = payload.get("choices")
    if isinstance(choices, list):
        parts = []
        for choice in choices:
            message = choice.get("message", {})
            content = message.get("content")
            if isinstance(content, str) and content.strip():
                parts.append(content.strip())
            elif isinstance(content, list):
                for item in content:
                    text = item.get("text")
                    if text:
                        parts.append(text.strip())
        if parts:
            return "\n".join(part for part in parts if part)

    output = payload.get("output")
    if isinstance(output, list):
        parts = []
        for item in output:
            for content in item.get("content", []):
                text = content.get("text")
                if text:
                    parts.append(text.strip())
        if parts:
            return "\n".join(part for part in parts if part)

    return json.dumps(payload, ensure_ascii=False, indent=2)


def sanitize_history_text(text: str) -> str:
    cleaned_lines = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            cleaned_lines.append("")
            continue

        lowered = line.lower()
        if any(re.search(pattern, lowered, flags=re.IGNORECASE) for pattern in HISTORY_REDACTION_PATTERNS):
            continue

        if line.startswith("|---") or line.startswith("| :---"):
            continue

        cleaned_lines.append(line)

    cleaned = "\n".join(cleaned_lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    return cleaned


def build_messages(model_config: dict, opening: str, history: list[dict]) -> list[dict]:
    if not history:
        return [{"role": "user", "content": [{"type": "text", "text": opening}]}]

    messages = []
    for item in history:
        sanitized_text = sanitize_history_text(item["text"])
        if not sanitized_text:
            continue
        role = "assistant" if item["speaker_id"] == model_config["speaker_id"] else "user"
        messages.append(
            {
                "role": role,
                "content": [{"type": "text", "text": sanitized_text}],
            }
        )

    if not messages:
        return [{"role": "user", "content": [{"type": "text", "text": opening}]}]
    return messages


def call_model(model_config: dict, messages: list[dict], max_tokens: int) -> dict:
    body = {
        "stream": False,
        "model": model_config["model"],
        "max_tokens": max_tokens,
        "messages": messages,
    }
    request = urllib.request.Request(
        url=model_config["url"],
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-TT-LOGID": model_config["log_id"],
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        return json.loads(response.read().decode("utf-8"))


def build_html(run_meta: dict, history: list[dict]) -> str:
    transcript_json = json.dumps(history, ensure_ascii=False)
    meta_json = json.dumps(run_meta, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>LLM Duet Transcript</title>
    <style>
      :root {{
        --paper: #f6f0e4;
        --ink: #1d1a17;
        --muted: #6a6259;
        --line: rgba(29, 26, 23, 0.12);
        --gemini: #ffefe3;
        --gpt: #e7f7ef;
        --accent: #b55d32;
        --card-shadow: 0 22px 50px rgba(40, 25, 10, 0.12);
      }}

      * {{
        box-sizing: border-box;
      }}

      body {{
        margin: 0;
        min-height: 100vh;
        color: var(--ink);
        font-family: "Iowan Old Style", "Palatino Linotype", "Noto Serif SC", serif;
        background:
          radial-gradient(circle at top left, rgba(181, 93, 50, 0.14), transparent 24%),
          radial-gradient(circle at bottom right, rgba(34, 120, 84, 0.10), transparent 28%),
          linear-gradient(180deg, #fbf8f2 0%, #f1e9da 100%);
      }}

      .page {{
        width: min(1120px, calc(100% - 28px));
        margin: 24px auto 48px;
      }}

      .hero {{
        padding: 28px;
        border: 1px solid var(--line);
        border-radius: 28px;
        background: rgba(255, 252, 247, 0.78);
        backdrop-filter: blur(12px);
        box-shadow: var(--card-shadow);
      }}

      .eyebrow {{
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 0.18em;
        font-size: 12px;
      }}

      h1 {{
        margin: 12px 0 10px;
        font-size: clamp(34px, 6vw, 64px);
        line-height: 0.95;
      }}

      .summary {{
        color: var(--muted);
        font-size: 16px;
        line-height: 1.7;
        max-width: 760px;
      }}

      .meta {{
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 12px;
        margin-top: 20px;
      }}

      .metric {{
        padding: 14px 16px;
        border-radius: 18px;
        border: 1px solid var(--line);
        background: rgba(255, 255, 255, 0.56);
      }}

      .metric-label {{
        color: var(--muted);
        font-size: 12px;
        margin-bottom: 8px;
      }}

      .metric-value {{
        font-size: 20px;
      }}

      .stream {{
        display: grid;
        gap: 14px;
        margin-top: 18px;
      }}

      .turn {{
        padding: 18px 18px 16px;
        border-radius: 24px;
        border: 1px solid var(--line);
        box-shadow: var(--card-shadow);
        animation: rise 320ms ease;
      }}

      .turn-gemini {{
        background: linear-gradient(180deg, #fff7f0 0%, var(--gemini) 100%);
      }}

      .turn-gpt {{
        background: linear-gradient(180deg, #f5fff9 0%, var(--gpt) 100%);
      }}

      .turn-head {{
        display: flex;
        justify-content: space-between;
        gap: 12px;
        align-items: baseline;
        margin-bottom: 10px;
      }}

      .turn-name {{
        font-size: 20px;
        font-weight: 700;
      }}

      .turn-index {{
        color: var(--muted);
        font-size: 13px;
      }}

      .turn-text {{
        white-space: pre-wrap;
        line-height: 1.8;
        font-size: 18px;
      }}

      @keyframes rise {{
        from {{
          opacity: 0;
          transform: translateY(10px);
        }}
        to {{
          opacity: 1;
          transform: translateY(0);
        }}
      }}

      @media (max-width: 880px) {{
        .meta {{
          grid-template-columns: 1fr 1fr;
        }}
      }}

      @media (max-width: 560px) {{
        .page {{
          width: min(100%, calc(100% - 18px));
          margin-top: 10px;
        }}

        .hero {{
          padding: 18px;
          border-radius: 22px;
        }}

        .meta {{
          grid-template-columns: 1fr;
        }}

        .turn-text {{
          font-size: 17px;
        }}
      }}
    </style>
  </head>
  <body>
    <main class="page">
      <section class="hero">
        <div class="eyebrow">Two Models, One Room</div>
        <h1>LLM 相互对话实验</h1>
        <p class="summary">Gemini 3 Pro 和 GPT-5.4 轮流说话，不做人类中介，只保留彼此的上下文。下面这页展示本次 20 轮实验的完整记录。</p>
        <div class="meta" id="meta"></div>
      </section>
      <section class="stream" id="stream"></section>
    </main>
    <script>
      const meta = {meta_json};
      const history = {transcript_json};

      function escapeHtml(value) {{
        return value
          .replaceAll("&", "&amp;")
          .replaceAll("<", "&lt;")
          .replaceAll(">", "&gt;");
      }}

      document.getElementById("meta").innerHTML = [
        ["总轮数", String(meta.turns)],
        ["开场", escapeHtml(meta.opening)],
        ["开始时间", new Date(meta.started_at).toLocaleString("zh-CN", {{ hour12: false }})],
        ["运行目录", escapeHtml(meta.run_dir)],
      ].map(([label, value]) => `
        <div class="metric">
          <div class="metric-label">${{label}}</div>
          <div class="metric-value">${{value}}</div>
        </div>
      `).join("");

      document.getElementById("stream").innerHTML = history.map((item) => `
        <article class="turn turn-${{item.speaker_id}}">
          <div class="turn-head">
            <div class="turn-name">${{escapeHtml(item.speaker_name)}}</div>
            <div class="turn-index">第 ${{item.turn_index}} 轮 · ${{new Date(item.timestamp).toLocaleTimeString("zh-CN", {{ hour12: false }})}}</div>
          </div>
          <div class="turn-text">${{escapeHtml(item.text)}}</div>
        </article>
      `).join("");
    </script>
  </body>
</html>
"""


def build_markdown(run_meta: dict, history: list[dict]) -> str:
    lines = [
        "# LLM Duet Transcript",
        "",
        f"- Started at: {run_meta['started_at']}",
        f"- Turns: {run_meta['turns']}",
        f"- Opening: {run_meta['opening']}",
        "",
    ]
    for item in history:
        lines.extend(
            [
                f"## Turn {item['turn_index']} - {item['speaker_name']}",
                "",
                item["text"],
                "",
            ]
        )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_dir)
    output_root.mkdir(parents=True, exist_ok=True)

    started_at = utc_now()
    run_id = started_at.strftime("%Y%m%dT%H%M%SZ")
    run_dir = output_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    run_meta = {
        "started_at": started_at.isoformat(),
        "turns": args.turns,
        "opening": args.opening,
        "run_dir": str(run_dir),
        "model_a": MODEL_A["model"],
        "model_b": MODEL_B["model"],
        "dry_run": args.dry_run,
    }
    write_json(run_dir / "run_config.json", run_meta)

    history: list[dict] = []
    jsonl_path = run_dir / "transcript.jsonl"
    live_state_path = run_dir / "live_state.json"

    for turn_index in range(1, args.turns + 1):
        model_config = MODEL_A if turn_index % 2 == 1 else MODEL_B
        messages = build_messages(model_config=model_config, opening=args.opening, history=history)

        try:
            if args.dry_run:
                raw_response = {"dry_run": True, "speaker": model_config["display_name"]}
                text = f"(dry-run) {model_config['display_name']} 在第 {turn_index} 轮说了一句占位话。"
            else:
                raw_response = call_model(
                    model_config=model_config,
                    messages=messages,
                    max_tokens=args.max_tokens,
                )
                text = extract_text(raw_response).strip()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raw_response = {
                "error_type": "HTTPError",
                "status": exc.code,
                "reason": exc.reason,
                "detail": detail,
            }
            text = f"[request failed] HTTP {exc.code}: {exc.reason}\n{detail}"
        except Exception as exc:  # noqa: BLE001
            raw_response = {"error_type": type(exc).__name__, "detail": str(exc)}
            text = f"[request failed] {exc}"

        record = {
            "turn_index": turn_index,
            "speaker_id": model_config["speaker_id"],
            "speaker_name": model_config["display_name"],
            "model": model_config["model"],
            "timestamp": utc_now().isoformat(),
            "messages": messages,
            "text": text,
            "raw_response": raw_response,
        }
        history.append(record)
        append_jsonl(jsonl_path, record)
        write_json(
            live_state_path,
            {
                "status": "running" if turn_index < args.turns else "completed",
                "meta": run_meta,
                "latest": record,
                "history": history,
                "updated_at": utc_now().isoformat(),
            },
        )
        print(f"[turn {turn_index}/{args.turns}] {record['speaker_name']}: {text}\n", flush=True)

    write_json(
        live_state_path,
        {
            "status": "completed",
            "meta": run_meta,
            "latest": history[-1] if history else None,
            "history": history,
            "updated_at": utc_now().isoformat(),
        },
    )
    (run_dir / "transcript.md").write_text(build_markdown(run_meta, history), encoding="utf-8")
    (run_dir / "transcript.html").write_text(build_html(run_meta, history), encoding="utf-8")
    print(f"Saved artifacts to: {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
