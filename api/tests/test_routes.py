from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_valid_email():
    VALID_EMAILs = ["bsuraj11@gmail.com", "abc123@outlook.com"]
    for email in VALID_EMAILs:
        response = client.get(f"/validate?email={email}")
        assert response.status_code == 200
        assert "data" in response.json()  # No error


def test_invalid_email():
    INVALID_EMAILS = ['', 'invalid@.org', 'abc.com', 'sdjkskes@1234']
    for email in INVALID_EMAILS:
        response = client.get(f"/validate?email={email}")
        assert response.status_code == 403
        assert response.json() == {
            "error": {
                "message": "Invalid Format",
                "code": 403
            }
        }


def test_disposable_mails():
    DISPOSABLE_EMAILS = ['abc@000865j.com', 'email@007.surf', 'test@021-club.live']
    for email in DISPOSABLE_EMAILS:
        response = client.get(f"/validate?email={email}")
        assert response.status_code == 422
        assert response.json() == {
            "error": {
                "message": "Unprocessable Entity",
                "code": 422
            }
        }


def test_invalid_domains():
    INVALID_DOMAIN_EMAILS = ['bsuraj22@hjahjdh.com', 'abc@fake-domain123.com']
    for email in INVALID_DOMAIN_EMAILS:
        response = client.get(f"/validate?email={email}")
        assert response.status_code == 400
        domain = email.split('@')[-1]
        assert response.json() == {
            "error": {
                "message": f"The domain name {domain} does not exist.",
                "code": 400
            }
        }