"""Plain-language ordinance summary helper for CivicComms."""

from dataclasses import dataclass


@dataclass(frozen=True)
class OrdinanceSummaryDraft:
    ordinance_id: str
    plain_language_summary: str
    citations: list[str]
    warnings: list[str]
    boundary: str


def draft_ordinance_summary(
    *,
    ordinance_id: str,
    topic: str,
    citations: list[str],
) -> OrdinanceSummaryDraft:
    """Return a cautious, citation-forward ordinance explainer draft."""

    warnings = [
        "Do not present this as legal advice.",
        "Verify adopted-effective-date language before publishing.",
    ]
    if not citations:
        warnings.append("Add citations before staff publication review.")

    return OrdinanceSummaryDraft(
        ordinance_id=ordinance_id,
        plain_language_summary=(
            f"Draft explainer: {ordinance_id} concerns {topic}. Staff should attach "
            "the exact adopted ordinance text and any affected municipal code sections."
        ),
        citations=citations,
        warnings=warnings,
        boundary="Human-approved public explainer only; not legal interpretation.",
    )
