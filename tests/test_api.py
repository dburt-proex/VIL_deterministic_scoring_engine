from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.store import audit_store

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_score_persists_audit_record(tmp_path):
    original_path = audit_store.path
    audit_store.path = Path(tmp_path) / "audit_log.jsonl"
    audit_store.path.parent.mkdir(parents=True, exist_ok=True)

    try:
        payload = {
            "source": "website_form",
            "signal_type": "lead",
            "content": "A construction client has budget, urgency, estimate follow-up problems, and wants routing automation.",
            "metadata": {"industry": "construction", "workflow": "lead intake"},
            "source_pointers": [{"type": "form", "value": "website intake"}],
            "risk_flags": [],
        }
        response = client.post("/score", json=payload)
        assert response.status_code == 200
        body = response.json()
        assert body["route"] in {"PASS", "REVIEW", "CLARIFY", "ARCHIVE", "HALT"}
        assert body["audit"]["audit_id"].startswith("audit_")

        audit_response = client.get("/audits")
        assert audit_response.status_code == 200
        assert len(audit_response.json()) == 1

        metrics_response = client.get("/metrics")
        assert metrics_response.status_code == 200
        assert metrics_response.json()["total_signals"] == 1
    finally:
        audit_store.path = original_path


def test_config_exposes_decision_controls():
    response = client.get("/config")
    assert response.status_code == 200
    body = response.json()
    assert "weights" in body
    assert "thresholds" in body
    assert "routes" in body
    assert body["decision_rule"] == "vil_score = min(weighted_signal_score, verifiability_score)"
