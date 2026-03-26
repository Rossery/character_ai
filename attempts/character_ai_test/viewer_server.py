#!/usr/bin/env python3

import argparse
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class ViewerHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory: str, **kwargs):
        self.root_dir = Path(directory)
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/api/latest":
            payload = self._load_latest_state()
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def _load_latest_state(self) -> dict:
        runs_dir = self.root_dir / "runs"
        if not runs_dir.exists():
            return {"status": "idle", "message": "No runs directory yet."}

        run_dirs = sorted(
            [path for path in runs_dir.iterdir() if path.is_dir()],
            key=lambda path: path.name,
            reverse=True,
        )
        for run_dir in run_dirs:
            live_state = run_dir / "live_state.json"
            if live_state.exists():
                return json.loads(live_state.read_text(encoding="utf-8"))

        return {"status": "idle", "message": "No live_state.json found yet."}


def parse_args() -> argparse.Namespace:
    base_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Serve the Character AI live viewer.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--directory", default=str(base_dir))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    handler = partial(ViewerHandler, directory=args.directory)
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Viewer running at http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
