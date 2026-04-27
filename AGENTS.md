# CivicComms Agent Board

## Operating Contract

- Upstream suite spec: `CivicSuite/civicsuite/docs/CivicSuiteUnifiedSpec.md`, especially the CivicComms catalog entry and suite-wide non-negotiables.
- CivicComms supports source-backed public explainers, meeting summaries, ordinance summaries, newsletters, FAQs, and audience-specific draft variants.
- Apache 2.0 for code, CC BY 4.0 for documentation.
- Every change must keep docs, tests, browser QA evidence, and version surfaces in sync.

## Hard Boundaries

- CivicComms never publishes autonomously, creates campaign or advocacy content, provides legal advice, certifies translations, posts to social media, or updates a communications system of record.
- CivicComms v0.1.0 must not call live LLMs or live publishing/social-media/communications systems.
- Every generated artifact is a draft requiring staff review, citation verification, approval, and publication through official city channels.
- CivicComms depends on CivicCore; CivicCore must never depend on CivicComms.
- CivicComms may reference CivicClerk, CivicCode, and CivicAccess concepts only through released APIs or deterministic sample data in v0.1.0.

## Verification

Run before push or release:

```bash
bash scripts/verify-release.sh
```

Browser QA evidence is required for `docs/index.html` and `/civiccomms` whenever visible UI changes.
