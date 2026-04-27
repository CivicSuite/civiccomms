"""Newsletter and public update draft helper for CivicComms."""

from dataclasses import dataclass


@dataclass(frozen=True)
class NewsletterDraft:
    headline: str
    sections: list[str]
    approval_checklist: list[str]
    boundary: str


def draft_newsletter(
    *,
    week_of: str,
    source_items: list[str],
) -> NewsletterDraft:
    """Build a deterministic newsletter outline from source items."""

    sections = [f"Source-backed update: {item}" for item in source_items[:6]]
    if not sections:
        sections = ["No source-backed updates provided yet."]

    return NewsletterDraft(
        headline=f"City update draft for week of {week_of}",
        sections=sections,
        approval_checklist=[
            "Confirm source links for every claim.",
            "Run accessibility/plain-language review before publication.",
            "Confirm no campaign, advocacy, or electioneering language is present.",
        ],
        boundary="Draft only; staff controls edits, approval, and publication.",
    )
