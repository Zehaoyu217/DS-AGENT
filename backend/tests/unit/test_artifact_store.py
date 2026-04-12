from __future__ import annotations

from pathlib import Path

import pytest

from app.artifacts.models import Artifact
from app.artifacts.store import ArtifactStore


@pytest.fixture
def store(tmp_path: Path) -> ArtifactStore:
    return ArtifactStore(db_path=tmp_path / "a.db", disk_root=tmp_path / "blobs")


def test_add_and_get_round_trip(store: ArtifactStore) -> None:
    a = Artifact(type="table", title="Rows per country", content="<table/>", format="html")
    saved = store.add_artifact("s1", a)
    assert saved.id
    assert saved.name == "rows_per_country"

    again = store.get_artifact("s1", saved.id)
    assert again is not None
    assert again.content == "<table/>"


def test_slug_collision_is_suffixed(store: ArtifactStore) -> None:
    store.add_artifact("s1", Artifact(type="table", title="Revenue", content="<table/>"))
    second = store.add_artifact("s1", Artifact(type="table", title="Revenue", content="<table/>"))
    assert second.name == "revenue_2"


def test_get_by_name(store: ArtifactStore) -> None:
    saved = store.add_artifact("s1", Artifact(type="chart", title="Trend", content="{}", format="vega-lite"))
    hit = store.get_artifact_by_name("s1", "trend")
    assert hit is not None
    assert hit.id == saved.id


def test_survives_new_instance(tmp_path: Path) -> None:
    db = tmp_path / "a.db"
    blobs = tmp_path / "blobs"
    s1 = ArtifactStore(db_path=db, disk_root=blobs)
    saved = s1.add_artifact("s1", Artifact(type="table", title="Persist", content="<t/>"))

    s2 = ArtifactStore(db_path=db, disk_root=blobs)
    again = s2.get_artifact("s1", saved.id)
    assert again is not None
    assert again.content == "<t/>"


def test_update_preserves_id(store: ArtifactStore) -> None:
    saved = store.add_artifact("s1", Artifact(type="table", title="Live", content="<t/>"))
    updated = store.update_artifact("s1", saved.id, content="<t2/>")
    assert updated is not None
    assert updated.id == saved.id
    assert updated.content == "<t2/>"


def test_disk_split_above_threshold(tmp_path: Path) -> None:
    store = ArtifactStore(db_path=tmp_path / "a.db", disk_root=tmp_path / "blobs", inline_threshold=100)
    big = "x" * 500
    saved = store.add_artifact("s1", Artifact(type="file", title="Big", content=big, format="txt"))
    again = store.get_artifact("s1", saved.id)
    assert again is not None
    assert again.content == big
    assert (tmp_path / "blobs" / "s1" / f"{saved.id}.txt").exists()


def test_disk_split_survives_reload(tmp_path: Path) -> None:
    db = tmp_path / "a.db"
    blobs = tmp_path / "blobs"
    s1 = ArtifactStore(db_path=db, disk_root=blobs, inline_threshold=100)
    big = "y" * 500
    saved = s1.add_artifact("s1", Artifact(type="file", title="Big", content=big, format="txt"))

    s2 = ArtifactStore(db_path=db, disk_root=blobs, inline_threshold=100)
    again = s2.get_artifact("s1", saved.id)
    assert again is not None
    assert again.content == big


def test_accepts_profile_type(store: ArtifactStore) -> None:
    saved = store.add_artifact(
        "s1",
        Artifact(type="profile", title="customers_v1 profile", content="{}", format="profile-json"),
    )
    assert saved.type == "profile"
