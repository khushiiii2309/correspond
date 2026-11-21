import uuid

from app.models.email_analysis import EmailAnalysis
from app.models.enums import EmailCategory, PriorityLevel


def _first_email_id(client):
    client.post("/api/emails/demo/seed")
    return client.get("/api/emails").json()[0]["id"]


def test_set_category_creates_analysis_row(client):
    email_id = _first_email_id(client)

    response = client.patch(f"/api/emails/{email_id}/analysis", json={"category": "important"})
    assert response.status_code == 200

    detail = response.json()
    assert detail["analysis"]["category"] == "important"
    assert detail["analysis"]["category_overridden"] is True
    assert detail["analysis"]["ai_category"] is None
    assert detail["analysis"]["priority_overridden"] is False


def test_set_priority_only_does_not_touch_category(client):
    email_id = _first_email_id(client)

    client.patch(f"/api/emails/{email_id}/analysis", json={"category": "requires_action"})
    response = client.patch(f"/api/emails/{email_id}/analysis", json={"priority": "high"})

    detail = response.json()
    assert detail["analysis"]["category"] == "requires_action"
    assert detail["analysis"]["priority"] == "high"
    assert detail["analysis"]["priority_overridden"] is True


def test_user_override_takes_precedence_over_ai_suggestion(client, db_session):
    email_id = _first_email_id(client)

    analysis = EmailAnalysis(
        email_id=uuid.UUID(email_id),
        ai_category=EmailCategory.PROMOTIONAL,
        ai_priority=PriorityLevel.LOW,
        summary="AI generated summary",
    )
    db_session.add(analysis)
    db_session.commit()

    detail = client.get(f"/api/emails/{email_id}").json()
    assert detail["analysis"]["category"] == "promotional"
    assert detail["analysis"]["category_overridden"] is False

    response = client.patch(f"/api/emails/{email_id}/analysis", json={"category": "important"})
    updated = response.json()
    assert updated["analysis"]["category"] == "important"
    assert updated["analysis"]["ai_category"] == "promotional"
    assert updated["analysis"]["category_overridden"] is True
    # Priority was never overridden, so the AI suggestion still applies.
    assert updated["analysis"]["priority"] == "low"
    assert updated["analysis"]["priority_overridden"] is False


def test_update_classification_requires_at_least_one_field(client):
    email_id = _first_email_id(client)
    response = client.patch(f"/api/emails/{email_id}/analysis", json={})
    assert response.status_code == 400


def test_update_classification_not_found(client):
    response = client.patch(f"/api/emails/{uuid.uuid4()}/analysis", json={"category": "important"})
    assert response.status_code == 404


def test_category_filter_reflects_user_override(client):
    client.post("/api/emails/demo/seed")
    emails = client.get("/api/emails").json()

    target_id = emails[0]["id"]
    client.patch(f"/api/emails/{target_id}/analysis", json={"category": "potentially_suspicious"})

    results = client.get("/api/emails?category=potentially_suspicious").json()
    assert any(item["id"] == target_id for item in results)
    assert all(item["category"] == "potentially_suspicious" for item in results)


def test_priority_filter_reflects_user_override(client):
    email_id = _first_email_id(client)
    client.patch(f"/api/emails/{email_id}/analysis", json={"priority": "high"})

    results = client.get("/api/emails?priority=high").json()
    assert any(item["id"] == email_id for item in results)
