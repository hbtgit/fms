def _account(client, code, name, type_):
    return client.post("/api/v1/accounts", json={"code": code, "name": name, "type": type_}).json()


def test_create_draft_entry(client):
    cash = _account(client, "1000", "Cash", "asset")
    sales = _account(client, "4000", "Sales", "revenue")

    resp = client.post(
        "/api/v1/journal-entries",
        json={
            "entry_date": "2026-01-15",
            "description": "Cash sale",
            "lines": [
                {"account_id": cash["id"], "debit": "250.00"},
                {"account_id": sales["id"], "credit": "250.00"},
            ],
        },
    )
    assert resp.status_code == 201
    entry = resp.json()
    assert entry["status"] == "draft"
    assert len(entry["lines"]) == 2

    fetched = client.get(f"/api/v1/journal-entries/{entry['id']}").json()
    assert fetched["lines"][0]["debit"] == "250.00"


def test_unknown_account_rejected(client):
    resp = client.post(
        "/api/v1/journal-entries",
        json={
            "entry_date": "2026-01-15",
            "description": "Bad",
            "lines": [{"account_id": 42, "debit": "10.00"}],
        },
    )
    assert resp.status_code == 422


def test_negative_amount_rejected(client):
    cash = _account(client, "1000", "Cash", "asset")
    resp = client.post(
        "/api/v1/journal-entries",
        json={
            "entry_date": "2026-01-15",
            "description": "Bad",
            "lines": [{"account_id": cash["id"], "debit": "-5.00"}],
        },
    )
    assert resp.status_code == 422
