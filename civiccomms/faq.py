"""FAQ draft helper for CivicComms."""

from dataclasses import dataclass


@dataclass(frozen=True)
class FAQDraft:
    topic: str
    questions: list[str]
    citations_required: bool
    boundary: str


def generate_faq(*, topic: str, source_facts: list[str]) -> FAQDraft:
    """Generate deterministic FAQ question prompts from source facts."""

    questions = [f"What should residents know about {fact}?" for fact in source_facts[:5]]
    if not questions:
        questions = [f"What source-backed information is available about {topic}?"]

    return FAQDraft(
        topic=topic,
        questions=questions,
        citations_required=True,
        boundary="FAQ answers must cite city source material before publication.",
    )
