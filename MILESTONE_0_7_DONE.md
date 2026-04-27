# CivicComms v0.1.0 Foundation Complete

## Criteria Covered

- FastAPI runtime shell.
- `civiccore==0.2.0` dependency pin.
- Source-readiness, meeting-summary, ordinance-summary, newsletter, FAQ, and audience-variant helpers.
- Public sample UI at `/civiccomms`.
- Documentation, release, and placeholder-import gates.
- Browser QA evidence for docs and runtime surfaces.

## Verification

- `python -m pytest -q`: 11 passed.
- `bash scripts/verify-release.sh`: passed.
- `python -m ruff check .`: passed.

## Boundaries

CivicComms v0.1.0 does not publish autonomously, create campaign or advocacy content, provide legal advice, certify translations, call live LLMs, post to social media, or replace a communications system of record.
