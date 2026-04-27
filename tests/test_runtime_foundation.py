from fastapi.testclient import TestClient

import civiccomms
from civiccomms.main import app


client = TestClient(app)


def test_package_version_is_010() -> None:
    assert civiccomms.__version__ == "0.1.0"


def test_root_endpoint_states_runtime_boundary() -> None:
    payload = client.get("/").json()

    assert payload["name"] == "CivicComms"
    assert payload["version"] == "0.1.0"
    assert payload["status"] == "public communications foundation"
    assert "autonomous publication" in payload["message"]
    assert "Post-v0.1.0 roadmap" in payload["next_step"]


def test_health_endpoint_reports_versions() -> None:
    payload = client.get("/health").json()

    assert payload["status"] == "ok"
    assert payload["service"] == "civiccomms"
    assert payload["version"] == "0.1.0"
    assert payload["civiccore_version"] == "0.2.0"
