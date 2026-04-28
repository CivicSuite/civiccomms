#!/usr/bin/env bash
set -euo pipefail

VERSION="0.1.1"

python_cmd() {
  local candidates=()
  if [[ -n "${CIVICCOMMS_RELEASE_PYTHON:-}" ]]; then
    candidates+=("${CIVICCOMMS_RELEASE_PYTHON}")
  fi
  candidates+=("/mnt/c/Users/scott/AppData/Local/Microsoft/WindowsApps/python.exe")
  candidates+=(python python3 "py -3")

  for candidate in "${candidates[@]}"; do
    if $candidate -c "import build, pytest, ruff" >/dev/null 2>&1
    then
      echo "$candidate"
      return
    fi
  done

  echo "ERROR: no Python candidate has build, pytest, and ruff installed" >&2
  exit 1
}

PYTHON="$(python_cmd)"

echo "==> Version surface check"
"$PYTHON" - <<'PY'
from pathlib import Path
import tomllib

root = Path.cwd()
pyproject = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
version = pyproject["project"]["version"]
init = (root / "civiccomms" / "__init__.py").read_text(encoding="utf-8")
readme = (root / "README.md").read_text(encoding="utf-8")
changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
assert version == "0.1.1", version
assert '__version__ = "0.1.1"' in init
assert "v0.1.1" in readme
assert "## [0.1.1] - 2026-04-28" in changelog
assert "civiccore==0.3.0" in readme
print("PASS: version surfaces synchronized")
PY

echo "==> Test suite"
"$PYTHON" -m pytest -q

echo "==> Documentation gate"
bash scripts/verify-docs.sh

echo "==> Placeholder import gate"
"$PYTHON" scripts/check-civiccore-placeholder-imports.py

echo "==> Ruff"
"$PYTHON" -m ruff check .

echo "==> Build artifacts"
rm -rf dist
"$PYTHON" -m build
(
  cd dist
  sha256sum civiccomms-0.1.1-py3-none-any.whl civiccomms-0.1.1.tar.gz > SHA256SUMS.txt
)
test -f dist/civiccomms-0.1.1-py3-none-any.whl
test -f dist/civiccomms-0.1.1.tar.gz
test -s dist/SHA256SUMS.txt
echo "PASS: build artifacts and SHA256SUMS.txt created"

echo "VERIFY-RELEASE: PASSED"
