"""
Automated Unit and Integration Tests for Student Management System.
Used in the CI/CD Pipeline to validate builds before containerization.
"""

import pytest
from app import app, is_valid_email


@pytest.fixture
def client():
    """Create and configure a Flask test client."""
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for test convenience
    with app.test_client() as client:
        yield client


# ── Health & Metrics Endpoint Tests ──────────────────────────────────────────

def test_health_endpoint(client):
    """Test that the /health endpoint returns 200 and expected JSON."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert "service" in data


def test_metrics_endpoint(client):
    """Test that Prometheus metrics endpoint /metrics is reachable and exports metrics."""
    response = client.get("/metrics")
    assert response.status_code == 200
    metrics_text = response.get_data(as_text=True)
    assert "flask_http_request_duration_seconds" in metrics_text or "app_info" in metrics_text


# ── Route Availability Tests ─────────────────────────────────────────────────

def test_dashboard_route(client):
    """Test that the home dashboard loads with HTTP 200."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Student Management System" in response.data or b"Dashboard" in response.data


def test_view_students_route(client):
    """Test that the students listing page returns HTTP 200."""
    response = client.get("/students")
    assert response.status_code == 200


def test_add_student_get_route(client):
    """Test that the add student page form renders with HTTP 200."""
    response = client.get("/students/add")
    assert response.status_code == 200


# ── Validation Function Tests ────────────────────────────────────────────────

def test_valid_emails():
    """Test that valid email formats pass validation."""
    assert is_valid_email("student@example.com") is True
    assert is_valid_email("john.doe@university.edu") is True
    assert is_valid_email("alex_123@college.ac.in") is True


def test_invalid_emails():
    """Test that invalid email formats fail validation."""
    assert is_valid_email("not-an-email") is False
    assert is_valid_email("missing-domain@") is False
    assert is_valid_email("@missing-user.com") is False
    assert is_valid_email("spaces in@email.com") is False
