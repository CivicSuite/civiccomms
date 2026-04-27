from fastapi.testclient import TestClient

from civiccomms.audience_variants import draft_audience_variant
from civiccomms.faq import generate_faq
from civiccomms.main import app
from civiccomms.meeting_summary import draft_meeting_summary
from civiccomms.newsletter import draft_newsletter
from civiccomms.ordinance_summary import draft_ordinance_summary
from civiccomms.source_review import review_sources


client = TestClient(app)


def test_source_review_requires_named_sources_and_citations() -> None:
    result = review_sources(source_titles=[], citations=[])

    assert result.ready_for_draft is False
    assert "source title" in result.missing_items[0]
    assert "Staff must review" in result.boundary


def test_meeting_summary_keeps_human_approval_boundary() -> None:
    result = draft_meeting_summary(
        meeting_title="April Council",
        actions=["approved the park grant"],
        citations=["packet p. 4"],
    )

    assert result.draft_points == ["April Council: approved the park grant"]
    assert "Remove partisan" in result.required_review_steps[1]
    assert "Draft only" in result.boundary


def test_ordinance_summary_warns_without_citations() -> None:
    result = draft_ordinance_summary(
        ordinance_id="ORD-2026-04",
        topic="short-term rental registration",
        citations=[],
    )

    assert "short-term rental" in result.plain_language_summary
    assert any("Add citations" in warning for warning in result.warnings)
    assert "not legal interpretation" in result.boundary


def test_newsletter_draft_blocks_advocacy_language_by_checklist() -> None:
    result = draft_newsletter(
        week_of="2026-04-27",
        source_items=["Council adopted the budget calendar"],
    )

    assert result.headline.endswith("2026-04-27")
    assert result.sections[0].startswith("Source-backed update")
    assert any("campaign" in item for item in result.approval_checklist)


def test_faq_requires_citations_for_answers() -> None:
    result = generate_faq(
        topic="water main work",
        source_facts=["planned night work on Pine Street"],
    )

    assert result.citations_required is True
    assert "planned night work" in result.questions[0]


def test_audience_variant_preserves_review_boundary() -> None:
    result = draft_audience_variant(
        base_message="The library roof project starts Monday.",
        audience="downtown businesses",
    )

    assert result.message.startswith("For downtown businesses")
    assert any("neutral" in note for note in result.review_notes)
    assert "no autonomous posting" in result.boundary


def test_civiccomms_support_apis_success_shape() -> None:
    assert client.post(
        "/api/v1/civiccomms/source-review",
        json={"source_titles": ["Council packet"], "citations": ["packet p. 2"]},
    ).json()["ready_for_draft"] is True
    assert client.post(
        "/api/v1/civiccomms/meeting-summary",
        json={"meeting_title": "Council", "actions": ["approved item 4"], "citations": ["minutes p. 3"]},
    ).status_code == 200
    assert client.post(
        "/api/v1/civiccomms/ordinance-summary",
        json={"ordinance_id": "ORD-1", "topic": "trees", "citations": ["code 12.01"]},
    ).status_code == 200
    assert client.post(
        "/api/v1/civiccomms/newsletter",
        json={"week_of": "2026-04-27", "source_items": ["park opening"]},
    ).status_code == 200
    assert client.post(
        "/api/v1/civiccomms/faq",
        json={"topic": "parks", "source_facts": ["new hours"]},
    ).status_code == 200
    assert client.post(
        "/api/v1/civiccomms/audience-variant",
        json={"base_message": "New hours begin Monday.", "audience": "families"},
    ).status_code == 200


def test_public_ui_route_is_accessible_and_honest() -> None:
    response = client.get("/civiccomms")

    assert response.status_code == 200
    assert "CivicComms v0.1.0" in response.text
    assert "Human approval required" in response.text
    assert "no campaign" in response.text.lower()
    assert "live LLM calls" in response.text
