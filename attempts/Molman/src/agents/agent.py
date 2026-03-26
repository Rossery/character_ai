import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from langchain_core.tools import BaseTool
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

def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def _load_yaml_config(path: Optional[str] = None) -> Dict[str, Any]:
    config_path = Path(path) if path else Path(os.getenv("MOLMAN_CONFIG", "") or (_project_root() / "molman.yaml"))
    if not config_path.exists() or not config_path.is_file():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    raw = config_path.read_text(encoding="utf-8")
    parsed = yaml.safe_load(raw) if raw.strip() else {}
    return parsed if isinstance(parsed, dict) else {}


def _read_prompt_file(path: str) -> str:
    p = Path(path)
    if not p.is_absolute():
        p = _project_root() / p
    return p.read_text(encoding="utf-8")


def create_coding_agent(plugin_tools: Optional[List[BaseTool]] = None, **kwargs):
    """Create a coding agent.

    Args:
        plugin_tools: Additional tools to add to the agent.
        **kwargs: Additional keyword arguments to pass to the agent.

    Returns:
        The coding agent.
    """
    plugin_tools = plugin_tools or []
    config = _load_yaml_config()
    prompts_cfg = config.get("prompts") or {}
    system_prompt_path = prompts_cfg.get("coding_system") or "src/prompts/system/coding_agent.txt"
    system_prompt = _read_prompt_file(system_prompt_path)
    return create_react_agent(
        model=init_chat_model(config),
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
            *plugin_tools,
        ],
        prompt=system_prompt,
        **kwargs,
    )
    
memory = InMemorySaver() # 为多轮对话做准备
coding_agent = create_coding_agent(checkpointer=memory)
