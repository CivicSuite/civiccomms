"""Source validation helpers for CivicComms draft workflows."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceReview:
    source_count: int
    ready_for_draft: bool
    missing_items: list[str]
    boundary: str


def review_sources(*, source_titles: list[str], citations: list[str]) -> SourceReview:
    """Validate minimum source and citation material before drafting."""

    missing: list[str] = []
    if not source_titles:
        missing.append("Add at least one source title before drafting.")
    if not citations:
        missing.append("Add at least one citation or source link before drafting.")

    return SourceReview(
        source_count=len(source_titles),
        ready_for_draft=not missing,
        missing_items=missing,
        boundary=(
            "CivicComms drafts from named source material only. Staff must review, "
            "approve, and publish through the city's official channels."
        ),
    )
