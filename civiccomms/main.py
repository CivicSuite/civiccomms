"""FastAPI runtime foundation for CivicComms."""

import os

from civiccore import __version__ as CIVICCORE_VERSION
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from civiccomms import __version__
from civiccomms.audience_variants import draft_audience_variant
from civiccomms.faq import generate_faq
from civiccomms.meeting_summary import draft_meeting_summary
from civiccomms.newsletter import draft_newsletter
from civiccomms.ordinance_summary import draft_ordinance_summary
from civiccomms.persistence import (
    CommunicationsDraftRepository,
    StoredMeetingSummary,
    StoredSourceReview,
)
from civiccomms.public_ui import render_public_lookup_page
from civiccomms.source_review import review_sources


app = FastAPI(
    title="CivicComms",
    version=__version__,
    description="Source-backed public explainers, meeting summaries, newsletters, FAQs, and audience-variant draft support for CivicSuite.",
)

_draft_repository: CommunicationsDraftRepository | None = None
_draft_db_url: str | None = None


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> Response:
    """Return an empty favicon response so browser QA has a clean console."""

    return Response(status_code=204)


class SourceReviewRequest(BaseModel):
    source_titles: list[str]
    citations: list[str]


class MeetingSummaryRequest(BaseModel):
    meeting_title: str
    actions: list[str]
    citations: list[str]
    audience: str = "residents"


class OrdinanceSummaryRequest(BaseModel):
    ordinance_id: str
    topic: str
    citations: list[str]


class NewsletterRequest(BaseModel):
    week_of: str
    source_items: list[str]


class FAQRequest(BaseModel):
    topic: str
    source_facts: list[str]


class AudienceVariantRequest(BaseModel):
    base_message: str
    audience: str


@app.get("/")
def root() -> dict[str, str]:
    """Return current product state without overstating unshipped behavior."""

    return {
        "name": "CivicComms",
        "version": __version__,
        "status": "public communications foundation plus draft persistence",
        "message": (
            "CivicComms package, API foundation, source review, meeting summary drafts, "
            "ordinance explainers, newsletter outlines, FAQ prompts, audience variants, optional "
            "database-backed source review and meeting summary draft records, and public UI foundation "
            "are online; autonomous publication, campaign content, legal advice, certified translation, "
            "live LLM calls, social media posting, and communications system-of-record integrations are "
            "not implemented yet."
        ),
        "next_step": "Post-v0.1.1 roadmap: source connector imports, CivicAccess review handoff, and approval queues",
    }


@app.get("/health")
def health() -> dict[str, str]:
    """Return dependency/version health for deployment smoke checks."""

    return {
        "status": "ok",
        "service": "civiccomms",
        "version": __version__,
        "civiccore_version": CIVICCORE_VERSION,
    }


@app.get("/civiccomms", response_class=HTMLResponse)
def public_civiccomms_page() -> str:
    """Return the public sample communications support UI."""

    return render_public_lookup_page()


@app.post("/api/v1/civiccomms/source-review")
def source_review(request: SourceReviewRequest) -> dict[str, object]:
    if _draft_database_url() is not None:
        stored = _get_draft_repository().create_source_review(
            source_titles=request.source_titles,
            citations=request.citations,
        )
        return _stored_source_review_response(stored)

    result = review_sources(
        source_titles=request.source_titles,
        citations=request.citations,
    )
    payload = result.__dict__
    payload["review_id"] = None
    return payload


@app.get("/api/v1/civiccomms/source-review/{review_id}")
def get_source_review(review_id: str) -> dict[str, object]:
    if _draft_database_url() is None:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "CivicComms draft persistence is not configured.",
                "fix": "Set CIVICCOMMS_DRAFT_DB_URL to retrieve persisted source review records.",
            },
        )
    stored = _get_draft_repository().get_source_review(review_id)
    if stored is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Source review record not found.",
                "fix": "Use a review_id returned by POST /api/v1/civiccomms/source-review.",
            },
        )
    return _stored_source_review_response(stored)


@app.post("/api/v1/civiccomms/meeting-summary")
def meeting_summary(request: MeetingSummaryRequest) -> dict[str, object]:
    if _draft_database_url() is not None:
        stored = _get_draft_repository().create_meeting_summary(
            meeting_title=request.meeting_title,
            actions=request.actions,
            citations=request.citations,
            audience=request.audience,
        )
        return _stored_meeting_summary_response(stored)

    result = draft_meeting_summary(
        meeting_title=request.meeting_title,
        actions=request.actions,
        citations=request.citations,
        audience=request.audience,
    )
    payload = result.__dict__
    payload["summary_id"] = None
    return payload


@app.get("/api/v1/civiccomms/meeting-summary/{summary_id}")
def get_meeting_summary(summary_id: str) -> dict[str, object]:
    if _draft_database_url() is None:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "CivicComms draft persistence is not configured.",
                "fix": "Set CIVICCOMMS_DRAFT_DB_URL to retrieve persisted meeting summary records.",
            },
        )
    stored = _get_draft_repository().get_meeting_summary(summary_id)
    if stored is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Meeting summary record not found.",
                "fix": "Use a summary_id returned by POST /api/v1/civiccomms/meeting-summary.",
            },
        )
    return _stored_meeting_summary_response(stored)


@app.post("/api/v1/civiccomms/ordinance-summary")
def ordinance_summary(request: OrdinanceSummaryRequest) -> dict[str, object]:
    return draft_ordinance_summary(
        ordinance_id=request.ordinance_id,
        topic=request.topic,
        citations=request.citations,
    ).__dict__


@app.post("/api/v1/civiccomms/newsletter")
def newsletter(request: NewsletterRequest) -> dict[str, object]:
    return draft_newsletter(
        week_of=request.week_of,
        source_items=request.source_items,
    ).__dict__


@app.post("/api/v1/civiccomms/faq")
def faq(request: FAQRequest) -> dict[str, object]:
    return generate_faq(
        topic=request.topic,
        source_facts=request.source_facts,
    ).__dict__


@app.post("/api/v1/civiccomms/audience-variant")
def audience_variant(request: AudienceVariantRequest) -> dict[str, object]:
    return draft_audience_variant(
        base_message=request.base_message,
        audience=request.audience,
    ).__dict__


def _draft_database_url() -> str | None:
    return os.environ.get("CIVICCOMMS_DRAFT_DB_URL")


def _get_draft_repository() -> CommunicationsDraftRepository:
    global _draft_db_url, _draft_repository
    db_url = _draft_database_url()
    if db_url is None:
        raise RuntimeError("CIVICCOMMS_DRAFT_DB_URL is not configured.")
    if _draft_repository is None or db_url != _draft_db_url:
        _dispose_draft_repository()
        _draft_db_url = db_url
        _draft_repository = CommunicationsDraftRepository(db_url=db_url)
    return _draft_repository


def _dispose_draft_repository() -> None:
    global _draft_repository
    if _draft_repository is not None:
        _draft_repository.engine.dispose()
        _draft_repository = None


def _stored_source_review_response(stored: StoredSourceReview) -> dict[str, object]:
    return {
        "review_id": stored.review_id,
        "source_titles": list(stored.source_titles),
        "citations": list(stored.citations),
        "source_count": stored.source_count,
        "ready_for_draft": stored.ready_for_draft,
        "missing_items": list(stored.missing_items),
        "boundary": stored.boundary,
        "created_at": stored.created_at.isoformat(),
    }


def _stored_meeting_summary_response(stored: StoredMeetingSummary) -> dict[str, object]:
    return {
        "summary_id": stored.summary_id,
        "meeting_title": stored.meeting_title,
        "actions": list(stored.actions),
        "title": stored.title,
        "audience": stored.audience,
        "draft_points": list(stored.draft_points),
        "required_review_steps": list(stored.required_review_steps),
        "citations": list(stored.citations),
        "boundary": stored.boundary,
        "created_at": stored.created_at.isoformat(),
    }
