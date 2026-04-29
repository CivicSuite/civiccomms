CivicComms
==========

CivicComms is the CivicSuite module for source-backed public explainers, meeting summaries, ordinance summaries, newsletters, FAQs, and audience-specific draft variants.

Current state: v0.1.1 public communications foundation plus draft persistence release. This repo ships a FastAPI package, health/root endpoints, documentation gates, deterministic source-readiness review, meeting summary draft outlines, optional database-backed source review and meeting summary draft records, ordinance explainer drafts, newsletter scaffolds, FAQ prompts, audience-variant drafts, and accessible public sample UI at /civiccomms.

It does not ship autonomous publication, campaign or advocacy content, legal advice, certified translation, live LLM calls, social media posting, or communications system-of-record integrations.

API:
- GET /
- GET /health
- GET /civiccomms
- POST /api/v1/civiccomms/source-review
- GET /api/v1/civiccomms/source-review/{review_id}
- POST /api/v1/civiccomms/meeting-summary
- GET /api/v1/civiccomms/meeting-summary/{summary_id}
- POST /api/v1/civiccomms/ordinance-summary
- POST /api/v1/civiccomms/newsletter
- POST /api/v1/civiccomms/faq
- POST /api/v1/civiccomms/audience-variant

Optional persistence: set CIVICCOMMS_DRAFT_DB_URL to enable SQLAlchemy-backed source review and meeting summary draft records. Without it, CivicComms remains deterministic and stateless.

Run:

python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh
