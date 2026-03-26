import asyncio
import uuid
from typing import Any, Dict, Optional

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import Footer, Header, Input, RichLog

from agents.agent import coding_agent


def _new_thread_id() -> str:
    return uuid.uuid4().hex


def _extract_assistant_text(result: Any) -> str:
    if not isinstance(result, dict):
        return str(result)
    messages = result.get("messages")
    if not messages:
        return str(result)
    for m in reversed(messages):
        if getattr(m, "type", None) == "ai" and getattr(m, "content", None):
            return str(m.content)
    last = messages[-1]
    content = getattr(last, "content", None)
    return str(content) if content is not None else str(last)


class MolmanChatApp(App):
    CSS = """
    #root { height: 100%; }
    #log { height: 1fr; }
    #input { dock: bottom; }
    """

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit"),
        Binding("ctrl+r", "reset_thread", "Reset Thread"),
    ]

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.thread_id = _new_thread_id()
        self._busy = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(id="root"):
            yield RichLog(id="log", wrap=True, markup=True)
            yield Input(placeholder="输入消息，回车发送。/reset 重开会话，/exit 退出", id="input")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#input", Input).focus()
        self._log_meta()

    def action_reset_thread(self) -> None:
        self.thread_id = _new_thread_id()
        self._log_meta("已重置会话")

    def _log(self, text: str) -> None:
        self.query_one("#log", RichLog).write(text)

    def _log_meta(self, msg: Optional[str] = None) -> None:
        base = f"[bold cyan]thread_id[/]: {self.thread_id}"
        if msg:
            base = f"{base}  [dim]{msg}[/]"
        self._log(base)

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        text = event.value.strip()
        event.input.value = ""
        if not text:
            return

        if text in {"/exit", "/quit"}:
            self.exit()
            return
        if text == "/reset":
            self.action_reset_thread()
            return

        if self._busy:
            self._log("[dim]Busy: 上一个请求还在运行[/]")
            return

        self._busy = True
        self._log(f"[bold green]You:[/] {text}")
        self._log("[dim]Molman 正在思考...[/]")

        try:
            result = await asyncio.to_thread(
                coding_agent.invoke,
                {"messages": [("user", text)]},
                {"configurable": {"thread_id": self.thread_id}},
            )
            reply = _extract_assistant_text(result)
            self._log(f"[bold magenta]Molman:[/] {reply}")
        except Exception as e:
            self._log(f"[bold red]Error:[/] {type(e).__name__}: {e}")
        finally:
            self._busy = False


def main() -> None:
    MolmanChatApp().run()
