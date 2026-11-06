import json
import escalations


def test_create_escalation_saves_ticket(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    ticket_file = data_dir / "escalations.json"
    monkeypatch.setattr(escalations, "DATA_DIR", data_dir)
    monkeypatch.setattr(escalations, "ESCALATIONS_PATH", ticket_file)

    ticket = escalations.create_escalation(
        name="A Customer",
        email="customer@example.com",
        query="My order has not arrived",
        session_id="session-123",
    )

    saved = json.loads(ticket_file.read_text(encoding="utf-8"))
    assert ticket["ticket_id"].startswith("SE-")
    assert ticket["status"] == "Pending"
    assert saved[0]["query"] == "My order has not arrived"
    assert saved[0]["session_id"] == "session-123"
