"""Audience variant draft helper for CivicComms."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AudienceVariantDraft:
    audience: str
    message: str
    review_notes: list[str]
    boundary: str


def draft_audience_variant(
    *,
    base_message: str,
    audience: str,
) -> AudienceVariantDraft:
    """Adapt a source-backed message for a named audience without changing facts."""

    return AudienceVariantDraft(
        audience=audience,
        message=f"For {audience}: {base_message}",
        review_notes=[
            "Verify this version preserves the source facts.",
            "Confirm tone is neutral, factual, and non-advocacy.",
            "Send multilingual or accessibility variants through CivicAccess review.",
        ],
        boundary="Variant draft only; no autonomous posting or translation certification.",
    )
