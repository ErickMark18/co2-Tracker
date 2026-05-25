"""Tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient

from src.api import app, verify_api_key
from src.database import init_db, get_session, Deploy, Base, engine


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def client():
    return TestClient(app)


class TestHealthEndpoint:
    def test_health_returns_ok(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data


class TestDeploysEndpoints:
    def test_create_deploy_without_auth_fails(self, client):
        response = client.post("/deploys", json={
            "repo": "owner/repo",
            "branch": "main",
            "region": "eu-north-1",
            "duration_s": 300,
        })
        assert response.status_code == 401

    def test_create_deploy_with_auth_success(self, client):
        response = client.post(
            "/deploys",
            json={
                "repo": "owner/repo",
                "branch": "main",
                "region": "eu-north-1",
                "provider": "aws",
                "duration_s": 300,
                "runner_size": "medium",
            },
            headers={"x-api-key": "dev-api-key-change-me"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["repo"] == "owner/repo"
        assert data["branch"] == "main"
        assert data["region"] == "eu-north-1"
        assert data["co2_grams"] > 0
        assert "id" in data

    def test_create_deploy_invalid_data(self, client):
        response = client.post(
            "/deploys",
            json={"repo": "owner/repo"},
            headers={"x-api-key": "dev-api-key-change-me"},
        )
        assert response.status_code == 422

    def test_list_deploys_empty(self, client):
        response = client.get("/deploys")
        assert response.status_code == 200
        data = response.json()
        assert data["deploys"] == []
        assert data["total"] == 0

    def test_list_deploys_with_data(self, client):
        client.post(
            "/deploys",
            json={
                "repo": "owner/repo",
                "branch": "main",
                "region": "eu-north-1",
                "duration_s": 300,
            },
            headers={"x-api-key": "dev-api-key-change-me"},
        )
        response = client.get("/deploys")
        assert response.status_code == 200
        data = response.json()
        assert len(data["deploys"]) == 1
        assert data["total"] == 1

    def test_list_deploys_filter_by_repo(self, client):
        client.post(
            "/deploys",
            json={
                "repo": "owner/repo1",
                "branch": "main",
                "region": "eu-north-1",
                "duration_s": 300,
            },
            headers={"x-api-key": "dev-api-key-change-me"},
        )
        client.post(
            "/deploys",
            json={
                "repo": "owner/repo2",
                "branch": "main",
                "region": "eu-north-1",
                "duration_s": 300,
            },
            headers={"x-api-key": "dev-api-key-change-me"},
        )
        response = client.get("/deploys?repo=owner/repo1")
        assert response.status_code == 200
        data = response.json()
        assert len(data["deploys"]) == 1
        assert data["deploys"][0]["repo"] == "owner/repo1"

    def test_get_deploy_by_id(self, client):
        created = client.post(
            "/deploys",
            json={
                "repo": "owner/repo",
                "branch": "main",
                "region": "eu-north-1",
                "duration_s": 300,
            },
            headers={"x-api-key": "dev-api-key-change-me"},
        )
        deploy_id = created.json()["id"]
        response = client.get(f"/deploys/{deploy_id}")
        assert response.status_code == 200
        assert response.json()["id"] == deploy_id

    def test_get_deploy_not_found(self, client):
        response = client.get("/deploys/99999")
        assert response.status_code == 404


class TestStatsEndpoint:
    def test_stats_empty(self, client):
        response = client.get("/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_deploys"] == 0
        assert data["total_co2_g"] == 0.0

    def test_stats_with_data(self, client):
        client.post(
            "/deploys",
            json={
                "repo": "owner/repo",
                "branch": "main",
                "region": "eu-north-1",
                "duration_s": 300,
            },
            headers={"x-api-key": "dev-api-key-change-me"},
        )
        client.post(
            "/deploys",
            json={
                "repo": "owner/repo",
                "branch": "main",
                "region": "ap-southeast-2",
                "duration_s": 300,
            },
            headers={"x-api-key": "dev-api-key-change-me"},
        )
        response = client.get("/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_deploys"] == 2
        assert data["total_co2_g"] > 0
        assert len(data["by_region"]) == 2

    def test_stats_filter_by_repo(self, client):
        client.post(
            "/deploys",
            json={
                "repo": "owner/repo1",
                "branch": "main",
                "region": "eu-north-1",
                "duration_s": 300,
            },
            headers={"x-api-key": "dev-api-key-change-me"},
        )
        client.post(
            "/deploys",
            json={
                "repo": "owner/repo2",
                "branch": "main",
                "region": "eu-north-1",
                "duration_s": 300,
            },
            headers={"x-api-key": "dev-api-key-change-me"},
        )
        response = client.get("/stats?repo=owner/repo1")
        assert response.status_code == 200
        data = response.json()
        assert data["total_deploys"] == 1