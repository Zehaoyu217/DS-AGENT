from __future__ import annotations

import base64
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def files_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    root = tmp_path / "files"
    root.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("FILES_ROOT", str(root))
    return root


@pytest.fixture
def client(files_root: Path) -> TestClient:  # noqa: ARG001 — fixture sets env
    return TestClient(create_app())


def test_tree_empty_root(client: TestClient) -> None:
    r = client.get("/api/files/tree")
    assert r.status_code == 200
    body = r.json()
    assert body == {"root": "", "entries": [], "truncated": False}


def test_tree_lists_non_recursive(client: TestClient, files_root: Path) -> None:
    (files_root / "a.txt").write_text("hello", encoding="utf-8")
    (files_root / "sub").mkdir()
    (files_root / "sub" / "inner.txt").write_text("ignored at this depth", encoding="utf-8")

    r = client.get("/api/files/tree")
    assert r.status_code == 200
    entries = r.json()["entries"]
    names = [e["name"] for e in entries]
    # Dirs sorted before files.
    assert names == ["sub", "a.txt"]

    dir_node = entries[0]
    file_node = entries[1]
    assert dir_node["kind"] == "dir"
    assert dir_node["size"] is None
    assert file_node["kind"] == "file"
    assert file_node["size"] == len("hello")
    assert file_node["path"] == "a.txt"


def test_tree_subdir(client: TestClient, files_root: Path) -> None:
    (files_root / "sub").mkdir()
    (files_root / "sub" / "inner.txt").write_text("x", encoding="utf-8")

    r = client.get("/api/files/tree", params={"path": "sub"})
    assert r.status_code == 200
    entries = r.json()["entries"]
    assert len(entries) == 1
    assert entries[0]["name"] == "inner.txt"
    assert entries[0]["path"] == "sub/inner.txt"


def test_read_utf8(client: TestClient, files_root: Path) -> None:
    (files_root / "hello.txt").write_text("hello world", encoding="utf-8")
    r = client.get("/api/files/read", params={"path": "hello.txt"})
    assert r.status_code == 200
    body = r.json()
    assert body["encoding"] == "utf-8"
    assert body["content"] == "hello world"
    assert body["size"] == len("hello world")
    assert body["path"] == "hello.txt"


def test_read_binary_omits_content_by_default(
    client: TestClient, files_root: Path,
) -> None:
    """Binary files return metadata only by default — avoids shipping
    up to ~13 MB of base64 for a UI that only displays size + encoding.
    """
    blob = b"\x89PNG\r\n\x1a\n\x00\x01\x02\xff"
    (files_root / "img.bin").write_bytes(blob)
    r = client.get("/api/files/read", params={"path": "img.bin"})
    assert r.status_code == 200
    body = r.json()
    assert body["encoding"] == "base64"
    assert body["content"] == ""
    assert body["size"] == len(blob)


def test_read_binary_include_content_opt_in(
    client: TestClient, files_root: Path,
) -> None:
    blob = b"\x89PNG\r\n\x1a\n\x00\x01\x02\xff"
    (files_root / "img.bin").write_bytes(blob)
    r = client.get(
        "/api/files/read",
        params={"path": "img.bin", "include_binary_content": "1"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["encoding"] == "base64"
    assert base64.b64decode(body["content"]) == blob
    assert body["size"] == len(blob)


def test_read_reject_traversal(client: TestClient) -> None:
    r = client.get("/api/files/read", params={"path": "../etc/passwd"})
    assert r.status_code == 400


def test_tree_reject_traversal(client: TestClient) -> None:
    r = client.get("/api/files/tree", params={"path": "../"})
    assert r.status_code == 400


def test_read_reject_absolute_path(client: TestClient) -> None:
    r = client.get("/api/files/read", params={"path": "/etc/passwd"})
    assert r.status_code == 400


def test_read_reject_null_byte(client: TestClient) -> None:
    r = client.get("/api/files/read", params={"path": "ok\x00/evil"})
    assert r.status_code == 400


def test_read_size_cap_returns_413(
    client: TestClient, files_root: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("app.api.files_api._FILE_READ_CAP_BYTES", 16)
    (files_root / "big.txt").write_text("x" * 17, encoding="utf-8")
    r = client.get("/api/files/read", params={"path": "big.txt"})
    assert r.status_code == 413


def test_read_not_found_returns_404(client: TestClient) -> None:
    r = client.get("/api/files/read", params={"path": "nope.txt"})
    assert r.status_code == 404


def test_tree_not_found_returns_404(client: TestClient) -> None:
    r = client.get("/api/files/tree", params={"path": "nope"})
    assert r.status_code == 404


def test_tree_rejects_file_path(client: TestClient, files_root: Path) -> None:
    (files_root / "a.txt").write_text("x", encoding="utf-8")
    r = client.get("/api/files/tree", params={"path": "a.txt"})
    assert r.status_code == 400


def test_read_rejects_directory(client: TestClient, files_root: Path) -> None:
    (files_root / "sub").mkdir()
    r = client.get("/api/files/read", params={"path": "sub"})
    assert r.status_code == 400


def test_tree_truncates_when_over_cap(
    client: TestClient, files_root: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("app.api.files_api._TREE_ENTRIES_CAP", 3)
    for i in range(5):
        (files_root / f"f{i}.txt").write_text("x", encoding="utf-8")
    body = client.get("/api/files/tree").json()
    assert body["truncated"] is True
    assert len(body["entries"]) == 3


def test_symlink_escape_is_filtered(
    client: TestClient, files_root: Path, tmp_path: Path,
) -> None:
    outside = tmp_path / "outside.txt"
    outside.write_text("secret", encoding="utf-8")
    link = files_root / "link.txt"
    try:
        link.symlink_to(outside)
    except (OSError, NotImplementedError):
        pytest.skip("symlinks not supported in this environment")

    # Tree: the escaping symlink must not appear in entries.
    entries = client.get("/api/files/tree").json()["entries"]
    assert all(e["name"] != "link.txt" for e in entries)

    # Direct read attempt through the symlink must be rejected.
    r = client.get("/api/files/read", params={"path": "link.txt"})
    assert r.status_code == 400
