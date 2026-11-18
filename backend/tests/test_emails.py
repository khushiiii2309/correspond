import uuid
from datetime import datetime, timezone

from app.models.email import Email
from app.models.enums import EmailSource
from app.models.user import User
from app.services.sample_emails_data import SAMPLE_EMAILS


def test_seed_demo_inbox_creates_sample_emails(client):
    response = client.post("/api/emails/demo/seed")
    assert response.status_code == 200
    body = response.json()
    assert body["created"] == len(SAMPLE_EMAILS)
    assert body["skipped"] == 0


def test_seed_demo_inbox_is_idempotent(client):
    client.post("/api/emails/demo/seed")
    response = client.post("/api/emails/demo/seed")
    body = response.json()
    assert body["created"] == 0
    assert body["skipped"] == len(SAMPLE_EMAILS)


def test_list_emails_returns_seeded_emails(client):
    client.post("/api/emails/demo/seed")
    response = client.get("/api/emails")
    assert response.status_code == 200
    emails = response.json()
    assert len(emails) == len(SAMPLE_EMAILS)
    assert all("preview" in item and "subject" in item for item in emails)


def test_list_emails_sorted_by_date_descending(client):
    client.post("/api/emails/demo/seed")
    response = client.get("/api/emails?sort=date")
    received_dates = [item["received_at"] for item in response.json()]
    assert received_dates == sorted(received_dates, reverse=True)


def test_get_email_detail(client):
    client.post("/api/emails/demo/seed")
    email_id = client.get("/api/emails").json()[0]["id"]

    response = client.get(f"/api/emails/{email_id}")
    assert response.status_code == 200
    detail = response.json()
    assert detail["id"] == email_id
    assert "body_text" in detail


def test_get_email_detail_not_found_returns_404(client):
    response = client.get(f"/api/emails/{uuid.uuid4()}")
    assert response.status_code == 404


def test_update_read_status(client):
    client.post("/api/emails/demo/seed")
    email_id = client.get("/api/emails").json()[0]["id"]

    response = client.patch(f"/api/emails/{email_id}/read-status", json={"is_read": True})
    assert response.status_code == 200
    assert response.json()["is_read"] is True

    detail = client.get(f"/api/emails/{email_id}").json()
    assert detail["is_read"] is True


def test_unread_only_filter(client):
    client.post("/api/emails/demo/seed")
    emails = client.get("/api/emails").json()
    client.patch(f"/api/emails/{emails[0]['id']}/read-status", json={"is_read": True})

    unread = client.get("/api/emails?unread_only=true").json()
    assert len(unread) == len(SAMPLE_EMAILS) - 1
    assert all(not item["is_read"] for item in unread)


def test_search_filters_by_subject_and_sender(client):
    client.post("/api/emails/demo/seed")
    response = client.get("/api/emails?search=contract")
    results = response.json()
    assert len(results) >= 1
    assert all("contract" in item["subject"].lower() or "contract" in item["preview"].lower() for item in results)


def test_emails_are_isolated_per_user(client, db_session):
    client.post("/api/emails/demo/seed")

    other_user = User(email="other-user@correspond.app", password_hash=None)
    db_session.add(other_user)
    db_session.commit()

    other_email = Email(
        user_id=other_user.id,
        sender="someone@elsewhere.com",
        recipient=other_user.email,
        subject="Private to the other user",
        body_text="This should never be visible to the demo user.",
        received_at=datetime.now(timezone.utc),
        is_read=False,
        source=EmailSource.SAMPLE,
    )
    db_session.add(other_email)
    db_session.commit()

    response = client.get("/api/emails")
    subjects = [item["subject"] for item in response.json()]
    assert "Private to the other user" not in subjects
