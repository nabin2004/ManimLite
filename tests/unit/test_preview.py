"""Tests for the live YAML preview server."""

from __future__ import annotations

import json
import socket
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

from motiongram.preview.server import PreviewServer, PreviewState

ROOT = Path(__file__).resolve().parents[2]
SHOWCASE = ROOT / "examples/yaml/deeplearning_showcase.yaml"


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _fetch(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=30) as resp:
        return resp.read()


def _start_server(manifest: Path, *, video_on_save: bool = False) -> PreviewServer:
    port = _free_port()
    server = PreviewServer(
        manifest,
        host="127.0.0.1",
        port=port,
        video_on_save=video_on_save,
        watch=False,
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    deadline = time.time() + 10.0
    while time.time() < deadline:
        try:
            _fetch(f"{server.url}/status.json")
            break
        except (urllib.error.URLError, ConnectionError):
            time.sleep(0.05)
    else:
        raise RuntimeError("preview server did not start")
    return server


def test_frame_png_valid() -> None:
    server = _start_server(SHOWCASE)
    try:
        data = _fetch(f"{server.url}/frame.png?t=0")
        assert data[:8] == b"\x89PNG\r\n\x1a\n"
    finally:
        server.shutdown()


def test_status_ok_for_valid_manifest() -> None:
    server = _start_server(SHOWCASE)
    try:
        payload = json.loads(_fetch(f"{server.url}/status.json"))
        assert payload["ok"] is True
        assert payload["duration"] == 8.0
        assert payload["width"] == 1280
        assert payload["height"] == 720
    finally:
        server.shutdown()


def test_status_error_for_invalid_manifest(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text("version: '1.0'\nscenes: not-a-list\n", encoding="utf-8")
    state = PreviewState(bad)
    status = state.status()
    assert status["ok"] is False
    assert status["error"]


def test_sse_reload_after_manual_reload() -> None:
    server = _start_server(SHOWCASE)
    try:
        req = urllib.request.Request(f"{server.url}/events")
        with urllib.request.urlopen(req, timeout=10) as resp:
            # Initial reload event from SSE connect
            chunk = resp.readline()
            assert b"event: reload" in chunk or b"reload" in chunk

            server.state.reload()
            deadline = time.time() + 5.0
            saw_reload = False
            while time.time() < deadline:
                line = resp.readline()
                if b"event: reload" in line:
                    saw_reload = True
                    break
            assert saw_reload
    finally:
        server.shutdown()
