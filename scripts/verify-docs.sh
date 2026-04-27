#!/usr/bin/env bash
set -euo pipefail

required=(
  README.md
  README.txt
  USER-MANUAL.md
  USER-MANUAL.txt
  CHANGELOG.md
  CONTRIBUTING.md
  LICENSE
  LICENSE-CODE
  LICENSE-DOCS
  SECURITY.md
  SUPPORT.md
  CODE_OF_CONDUCT.md
  docs/index.html
  docs/IMPLEMENTATION_PLAN.md
  docs/MILESTONES.md
  docs/RECONCILIATION.md
  docs/github-discussions-seed.md
)

echo "==> Required-artifact check"
for file in "${required[@]}"; do
  if [[ ! -s "$file" ]]; then
    echo "FAIL: required artifact missing or empty: $file" >&2
    exit 1
  fi
done

echo "==> Current-facing shipped/planned truth check"
if grep -RInE 'Civic311|civic311|Open311|system-of-record integrations are online|autonomous publication is implemented|campaign content is supported|legal advice is implemented|live LLM calls are online' README.md README.txt USER-MANUAL.md USER-MANUAL.txt docs/index.html CHANGELOG.md; then
  echo "FAIL: stale or overstated CivicComms copy found" >&2
  exit 1
fi

for token in CivicComms civiccomms "v0.1.0" "civiccore==0.2.0"; do
  if ! grep -RIn "$token" README.md USER-MANUAL.md docs/index.html CHANGELOG.md >/dev/null; then
    echo "FAIL: expected token missing from current-facing docs: $token" >&2
    exit 1
  fi
done

echo "VERIFY-DOCS: PASSED"
