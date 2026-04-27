# CivicComms Implementation Plan

## v0.1.0 Foundation

1. Ship FastAPI health/root/public UI surfaces.
2. Pin `civiccore==0.2.0`.
3. Add deterministic source-review, meeting-summary, ordinance-summary, newsletter, FAQ, and audience-variant helpers.
4. Document shipped/planned boundaries honestly.
5. Verify tests, docs, placeholder imports, Ruff, build artifacts, and browser QA.

## Future Work

- Source connector imports from CivicClerk, CivicCode, calendars, and prior communications.
- CivicAccess handoff for multilingual/accessibility review.
- Approval queues and publication audit trail.
- Live LLM drafting only after citation and human-approval gates exist.
