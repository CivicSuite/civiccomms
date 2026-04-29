# Production Depth: Communications Draft Persistence

## Summary

CivicComms now supports optional SQLAlchemy-backed source review and meeting summary draft records through `CIVICCOMMS_DRAFT_DB_URL`.

## Shipped

- `CommunicationsDraftRepository` with schema-aware SQLAlchemy tables.
- Persisted source review records with `review_id`.
- Persisted meeting summary records with `summary_id`.
- Retrieval endpoints:
  - `GET /api/v1/civiccomms/source-review/{review_id}`
  - `GET /api/v1/civiccomms/meeting-summary/{summary_id}`
- Actionable `503` guidance when persistence is not configured.
- Regression tests for repository reload, API round trip, missing-record `404`, no-config `503`, and stateless fallback behavior.

## Still Not Shipped

- Autonomous publication.
- Campaign or advocacy content.
- Legal advice.
- Certified translation.
- Live LLM calls.
- Social media posting.
- Communications system-of-record integrations.
