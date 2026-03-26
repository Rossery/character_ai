"""Chat model initialization for the code agent."""
import os
from typing import Any, Dict, List, Optional

from langchain_core.language_models import LanguageModelInput
from langchain_openai import ChatOpenAI

class ByteChatOpenAI(ChatOpenAI):
    """
    ByteChatOpenAI model for the code agent.
    """

    def _get_request_payload(
            self,
            input_: LanguageModelInput,
            *,
            stop: Optional[List[str]] = None,
            **kwargs: Any,
    ) -> dict:
        payload = super()._get_request_payload(input_, stop=stop, **kwargs)
        # 字节内部平台，不能直接使用 max_completion_tokens 参数，需要使用 max_tokens 参数
        if "max_tokens" not in payload:
            payload["max_tokens"] = self.max_tokens
            if "max_completion_tokens" in payload:
                payload.pop('max_completion_tokens', None)
        return payload


def init_chat_model(config: Dict[str, Any]) -> ChatOpenAI:
    """Initialize ChatOpenAI model with the given configuration dict.
    
    Args:
        config: Config dictionary loaded from YAML.
        
    Returns:
        Configured ChatOpenAI instance.
    """
    model_cfg = ((config.get("models") or {}).get("chat_model") or {}) if isinstance(config, dict) else {}
    model = model_cfg.get("model") or os.getenv("MOLMAN_CHAT_MODEL") or os.getenv("OPENAI_MODEL") or "gpt-4o-mini"
    base_url = model_cfg.get("api_base") or os.getenv("MOLMAN_API_BASE") or os.getenv("OPENAI_BASE_URL") or None
    api_key = model_cfg.get("api_key") or os.getenv("MOLMAN_API_KEY") or os.getenv("OPENAI_API_KEY") or None
    temperature = float(model_cfg.get("temperature", 0.2))
    max_tokens = int(model_cfg.get("max_tokens", 2048))
    extra_body = model_cfg.get("extra_body") or {}
    return ByteChatOpenAI(
        model=model,
        base_url=base_url,
        temperature=temperature,
        max_tokens=max_tokens,
        model_kwargs=extra_body,
        api_key=api_key,
    )

if __name__ == "__main__":
    import yaml
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent.parent
    cfg = yaml.safe_load((root / "molman.yaml").read_text(encoding="utf-8"))
    chat_model = init_chat_model(cfg if isinstance(cfg, dict) else {})
    response = chat_model.invoke("What is the capital of France?")
    print(response.content)
