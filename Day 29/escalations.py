"""File-backed support escalation requests for the demo application."""
from __future__ import annotations

import json
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
ESCALATIONS_PATH = DATA_DIR / "escalations.json"
_LOCK = threading.Lock()


def create_escalation(name: str, email: str, query: str, session_id: str = "") -> dict:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "ticket_id": f"SE-{uuid.uuid4().hex[:8].upper()}",
        "name": name.strip(),
        "email": email.strip(),
        "query": query.strip(),
        "session_id": session_id.strip(),
        "status": "Pending",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    with _LOCK:
        try:
            existing = json.loads(ESCALATIONS_PATH.read_text(encoding="utf-8"))
            if not isinstance(existing, list):
                existing = []
        except (FileNotFoundError, json.JSONDecodeError):
            existing = []
        existing.append(record)
        ESCALATIONS_PATH.write_text(
            json.dumps(existing, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
    return record
