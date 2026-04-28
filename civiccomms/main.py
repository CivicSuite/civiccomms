"""FastAPI runtime foundation for CivicComms."""

from civiccore import __version__ as CIVICCORE_VERSION
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from civiccomms import __version__
from civiccomms.audience_variants import draft_audience_variant
from civiccomms.faq import generate_faq
from civiccomms.meeting_summary import draft_meeting_summary
from civiccomms.newsletter import draft_newsletter
from civiccomms.ordinance_summary import draft_ordinance_summary
from civiccomms.public_ui import render_public_lookup_page
from civiccomms.source_review import review_sources


app = FastAPI(
    title="CivicComms",
    version=__version__,
    description="Source-backed public explainers, meeting summaries, newsletters, FAQs, and audience-variant draft support for CivicSuite.",
)

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
        "status": "public communications foundation",
        "message": (
            "CivicComms package, API foundation, source review, meeting summary drafts, "
            "ordinance explainers, newsletter outlines, FAQ prompts, audience variants, "
            "and public UI foundation are online; autonomous publication, campaign content, "
            "legal advice, certified translation, live LLM calls, social media posting, and "
            "communications system-of-record integrations are not implemented yet."
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
    return review_sources(
        source_titles=request.source_titles,
        citations=request.citations,
    ).__dict__


@app.post("/api/v1/civiccomms/meeting-summary")
def meeting_summary(request: MeetingSummaryRequest) -> dict[str, object]:
    return draft_meeting_summary(
        meeting_title=request.meeting_title,
        actions=request.actions,
        citations=request.citations,
        audience=request.audience,
    ).__dict__


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
