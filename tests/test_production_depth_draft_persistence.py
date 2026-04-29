from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from civiccomms.main import app, _dispose_draft_repository
from civiccomms.persistence import CommunicationsDraftRepository


client = TestClient(app)


def test_repository_persists_source_review_and_meeting_summary(tmp_path: Path) -> None:
    db_path = tmp_path / "civiccomms.db"
    db_url = f"sqlite+pysqlite:///{db_path.as_posix()}"

    repository = CommunicationsDraftRepository(db_url=db_url)
    review = repository.create_source_review(
        source_titles=["Council packet"],
        citations=["packet p. 2"],
    )
    summary = repository.create_meeting_summary(
        meeting_title="Council",
        actions=["approved item 4"],
        citations=["minutes p. 3"],
    )
    repository.engine.dispose()

    reloaded = CommunicationsDraftRepository(db_url=db_url)
    stored_review = reloaded.get_source_review(review.review_id)
    stored_summary = reloaded.get_meeting_summary(summary.summary_id)
    reloaded.engine.dispose()

    assert stored_review is not None
    assert stored_review.ready_for_draft is True
    assert stored_review.source_titles == ("Council packet",)
    assert stored_summary is not None
    assert stored_summary.title == "Public summary draft: Council"
    assert stored_summary.citations == ("minutes p. 3",)
    db_path.unlink()


def test_draft_persistence_api_round_trip(monkeypatch, tmp_path: Path) -> None:
    db_path = tmp_path / "civiccomms-api.db"
    monkeypatch.setenv("CIVICCOMMS_DRAFT_DB_URL", f"sqlite+pysqlite:///{db_path.as_posix()}")
    _dispose_draft_repository()

    created_review = client.post(
        "/api/v1/civiccomms/source-review",
        json={"source_titles": ["Council packet"], "citations": ["packet p. 2"]},
    )
    review_id = created_review.json()["review_id"]
    fetched_review = client.get(f"/api/v1/civiccomms/source-review/{review_id}")
    created_summary = client.post(
        "/api/v1/civiccomms/meeting-summary",
        json={"meeting_title": "Council", "actions": ["approved item 4"], "citations": ["minutes p. 3"]},
    )
    summary_id = created_summary.json()["summary_id"]
    fetched_summary = client.get(f"/api/v1/civiccomms/meeting-summary/{summary_id}")

    _dispose_draft_repository()
    monkeypatch.delenv("CIVICCOMMS_DRAFT_DB_URL")

    assert created_review.status_code == 200
    assert review_id
    assert fetched_review.status_code == 200
    assert fetched_review.json()["ready_for_draft"] is True
    assert created_summary.status_code == 200
    assert summary_id
    assert fetched_summary.status_code == 200
    assert fetched_summary.json()["title"] == "Public summary draft: Council"
    db_path.unlink()


def test_get_source_review_without_persistence_returns_actionable_503(monkeypatch) -> None:
    monkeypatch.delenv("CIVICCOMMS_DRAFT_DB_URL", raising=False)
    _dispose_draft_repository()

    response = client.get("/api/v1/civiccomms/source-review/example")

    assert response.status_code == 503
    detail = response.json()["detail"]
    assert detail["message"] == "CivicComms draft persistence is not configured."
    assert "Set CIVICCOMMS_DRAFT_DB_URL" in detail["fix"]


def test_get_meeting_summary_missing_id_returns_actionable_404(monkeypatch, tmp_path: Path) -> None:
    db_path = tmp_path / "civiccomms-missing.db"
    monkeypatch.setenv("CIVICCOMMS_DRAFT_DB_URL", f"sqlite+pysqlite:///{db_path.as_posix()}")
    _dispose_draft_repository()

    response = client.get("/api/v1/civiccomms/meeting-summary/missing")

    _dispose_draft_repository()
    monkeypatch.delenv("CIVICCOMMS_DRAFT_DB_URL")

    assert response.status_code == 404
    detail = response.json()["detail"]
    assert detail["message"] == "Meeting summary record not found."
    assert "POST /api/v1/civiccomms/meeting-summary" in detail["fix"]
    db_path.unlink()
