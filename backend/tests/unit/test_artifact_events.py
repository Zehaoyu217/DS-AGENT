from __future__ import annotations

from pathlib import Path

from app.artifacts.events import EventBus
from app.artifacts.models import Artifact
from app.artifacts.store import ArtifactStore


def test_emit_calls_subscriber() -> None:
    bus = EventBus()
    seen: list[dict] = []
    bus.subscribe(lambda ev: seen.append(ev))
    bus.emit("artifact.saved", {"artifact_id": "abc"})
    assert seen and seen[0]["type"] == "artifact.saved"
    assert seen[0]["data"]["artifact_id"] == "abc"


def test_store_emits_on_add(tmp_path: Path) -> None:
    bus = EventBus()
    seen: list[dict] = []
    bus.subscribe(lambda ev: seen.append(ev))
    store = ArtifactStore(db_path=tmp_path / "a.db", disk_root=tmp_path / "blobs", event_bus=bus)

    store.add_artifact("s1", Artifact(type="table", title="x", content="<t/>"))
    assert any(ev["type"] == "artifact.saved" for ev in seen)


def test_store_emits_on_update(tmp_path: Path) -> None:
    bus = EventBus()
    seen: list[dict] = []
    bus.subscribe(lambda ev: seen.append(ev))
    store = ArtifactStore(db_path=tmp_path / "a.db", disk_root=tmp_path / "blobs", event_bus=bus)

    saved = store.add_artifact("s1", Artifact(type="table", title="x", content="<t/>"))
    store.update_artifact("s1", saved.id, content="<t2/>")
    assert any(ev["type"] == "artifact.updated" for ev in seen)
