# Contributing to CivicComms

Thank you for helping CivicComms become useful municipal software.

## Local setup

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh
```

## Boundaries

- CivicComms gives source-backed communication draft support, not autonomous publication, campaign content, legal advice, certified translation, or official social media posting.
- Do not present generated summaries, explainers, newsletters, FAQs, or audience variants as publish-ready without staff review and citation verification.
- Do not add live LLM, social-media, publishing-system, or communications-system integrations without updating docs, tests, browser QA evidence, and the release gate.

## Pull requests

- Keep tests and docs with the code change.
- Run `bash scripts/verify-release.sh`.
- Include browser QA evidence for any visible UI or landing-page change.
