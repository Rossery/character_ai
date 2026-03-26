import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent

from model.chat_model import init_chat_model
from tools import (
    bash_tool,
    edit_tool,
    glob_tool,
    grep_tool,
    ls_tool,
    read_tool,
    todo_write_tool,
    tree_tool,
    write_tool,
)


class StopAfterPayload(Exception):
    pass


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_yaml_config() -> Dict[str, Any]:
    config_path = Path(os.getenv("MOLMAN_CONFIG", "")) if os.getenv("MOLMAN_CONFIG") else project_root() / "molman.yaml"
    raw = config_path.read_text(encoding="utf-8")
    parsed = yaml.safe_load(raw) if raw.strip() else {}
    return parsed if isinstance(parsed, dict) else {}


def read_prompt(prompt_path: str) -> str:
    p = Path(prompt_path)
    if not p.is_absolute():
        p = project_root() / p
    return p.read_text(encoding="utf-8")


def _safe_print(text: str) -> None:
    try:
        sys.stdout.write(text)
        if not text.endswith("\n"):
            sys.stdout.write("\n")
        sys.stdout.flush()
    except BrokenPipeError:
        try:
            sys.stdout.close()
        finally:
            raise SystemExit(0)


def _format_messages(payload: Dict[str, Any]) -> str:
    lines = []
    lines.append(f"model: {payload.get('model')}")
    if "temperature" in payload:
        lines.append(f"temperature: {payload.get('temperature')}")
    if "max_tokens" in payload:
        lines.append(f"max_tokens: {payload.get('max_tokens')}")
    lines.append("")

    messages = payload.get("messages") or []
    for i, m in enumerate(messages):
        role = m.get("role", "?")
        content = m.get("content")
        lines.append(f"[{i}] role={role}")
        if content is None:
            lines.append("content: <null>")
        elif isinstance(content, str):
            lines.append("content:")
            lines.append(content)
        else:
            lines.append("content:")
            lines.append(json.dumps(content, ensure_ascii=False, indent=2))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main(argv: Optional[List[str]] = None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["full", "messages"], default="messages")
    parser.add_argument("--stop-after-payload", action="store_true")
    parsed = parser.parse_args(argv)

    config = load_yaml_config()
    prompts_cfg = config.get("prompts") or {}
    system_prompt_path = prompts_cfg.get("coding_system") or "src/prompts/system/coding_agent.txt"
    system_prompt = read_prompt(system_prompt_path)

    model = init_chat_model(config)

    original_get_payload = model._get_request_payload
    printed = False

    def wrapped_get_payload(*args, **kwargs):
        nonlocal printed
        payload = original_get_payload(*args, **kwargs)
        if not printed:
            printed = True
            if parsed.mode == "full":
                _safe_print(json.dumps(payload, ensure_ascii=False, indent=2))
            else:
                _safe_print(_format_messages(payload))
            if parsed.stop_after_payload:
                raise StopAfterPayload()
        return payload

    model._get_request_payload = wrapped_get_payload

    agent = create_react_agent(
        model=model,
        tools=[
            bash_tool,
            grep_tool,
            ls_tool,
            glob_tool,
            tree_tool,
            read_tool,
            edit_tool,
            write_tool,
            todo_write_tool,
        ],
        prompt=system_prompt,
        checkpointer=InMemorySaver(),
    )

    try:
        result = agent.invoke(
            {"messages": [("user", "你是谁？请用一句话回答。")]},
            config={"configurable": {"thread_id": "inspect-request-payload"}},
        )
    except StopAfterPayload:
        return
    except Exception as e:
        _safe_print(f"ERROR: {type(e).__name__}: {e}")
        raise

    messages = result.get("messages") if isinstance(result, dict) else None
    if messages:
        last = messages[-1]
        content = getattr(last, "content", None)
        if content is None:
            _safe_print(f"reply: <{type(last).__name__} content=None>")
        else:
            _safe_print("reply:")
            _safe_print(str(content))


if __name__ == "__main__":
    main()
