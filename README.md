# CivicComms

CivicComms is the CivicSuite module for source-backed public explainers, meeting summaries, ordinance summaries, newsletters, FAQs, and audience-specific draft variants.

Current state: **v0.1.1 public communications foundation plus draft persistence release**. This repo ships a FastAPI package, health/root endpoints, documentation gates, deterministic source-readiness review, meeting summary draft outlines, optional database-backed source review and meeting summary draft records, ordinance explainer drafts, newsletter scaffolds, FAQ prompts, audience-variant drafts, and accessible public sample UI at `/civiccomms`. It does **not** ship autonomous publication, campaign or advocacy content, legal advice, certified translation, live LLM calls, social media posting, or communications system-of-record integrations.

## What CivicComms Does

- Check that draft work starts from named source material and citations.
- Create deterministic meeting summary draft outlines.
- Persist source review and meeting summary draft records when `CIVICCOMMS_DRAFT_DB_URL` is configured.
- Create plain-language ordinance explainer draft scaffolds.
- Build newsletter and FAQ draft structures from source items.
- Produce audience-specific variants without changing source facts.
- Demonstrate a public communications-support UI at `/civiccomms`.

## What CivicComms Does Not Do

- It does not publish or post autonomously.
- It does not produce campaign, advocacy, or partisan content.
- It does not provide legal advice.
- It does not certify translations or accessibility compliance.
- It does not call live LLMs in v0.1.1.
- It does not replace a communications system of record.

## API Surface

- `GET /` returns the shipped/planned boundary.
- `GET /health` returns package and CivicCore versions.
- `GET /civiccomms` returns the accessible public sample UI.
- `POST /api/v1/civiccomms/source-review` returns source-readiness checks.
- `GET /api/v1/civiccomms/source-review/{review_id}` retrieves a persisted source review when `CIVICCOMMS_DRAFT_DB_URL` is configured.
- `POST /api/v1/civiccomms/meeting-summary` returns a meeting summary draft outline and a `summary_id` when persistence is configured.
- `GET /api/v1/civiccomms/meeting-summary/{summary_id}` retrieves a persisted meeting summary when `CIVICCOMMS_DRAFT_DB_URL` is configured.
- `POST /api/v1/civiccomms/ordinance-summary` returns a plain-language explainer draft.
- `POST /api/v1/civiccomms/newsletter` returns a newsletter draft outline.
- `POST /api/v1/civiccomms/faq` returns source-backed FAQ prompts.
- `POST /api/v1/civiccomms/audience-variant` returns an audience-specific draft variant.

## Optional Persistence

Set `CIVICCOMMS_DRAFT_DB_URL` to enable local SQLAlchemy-backed source review and meeting summary records. Without that variable, CivicComms remains deterministic and stateless. Retrieval endpoints return actionable `503` responses that name the required configuration.

## Local Development

CivicComms v0.1.1 is pinned to `civiccore==0.3.0`.

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh
```

## License

Code is Apache License 2.0. Documentation is CC BY 4.0.
