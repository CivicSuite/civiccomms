"""Meeting summary draft helper for CivicComms."""

from dataclasses import dataclass


@dataclass(frozen=True)
class MeetingSummaryDraft:
    title: str
    audience: str
    draft_points: list[str]
    required_review_steps: list[str]
    citations: list[str]
    boundary: str


def draft_meeting_summary(
    *,
    meeting_title: str,
    actions: list[str],
    citations: list[str],
    audience: str = "residents",
) -> MeetingSummaryDraft:
    """Create a deterministic public-facing meeting summary outline."""

    points = [f"{meeting_title}: {action}" for action in actions[:5]]
    if not points:
        points = [f"{meeting_title}: no action items were provided for drafting."]

    return MeetingSummaryDraft(
        title=f"Public summary draft: {meeting_title}",
        audience=audience,
        draft_points=points,
        required_review_steps=[
            "Confirm every point against adopted minutes or packet source material.",
            "Remove partisan, campaign, or advocacy language.",
            "Route through communications staff before publication.",
        ],
        citations=citations,
        boundary="Draft only; not an official minute, finding, or publication.",
    )
