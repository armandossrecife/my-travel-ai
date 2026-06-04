"""
test_api_health.py — Testes para o endpoint /api/health
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Testes para o endpoint GET /api/health"""

    def test_health_endpoint_returns_200(self):
        """Testa se o endpoint retorna status 200."""
        response = client.get("/api/health")
        assert response.status_code == 200

    def test_health_endpoint_returns_json(self):
        """Testa se o endpoint retorna JSON válido."""
        response = client.get("/api/health")
        assert response.headers["content-type"] == "application/json"

    def test_health_response_structure(self):
        """Testa se a resposta tem a estrutura esperada."""
        response = client.get("/api/health")
        data = response.json()

        # Verifica campos obrigatórios
        assert "status" in data
        assert "service" in data
        assert "version" in data
        assert "llm_enabled" in data
        assert "active_logs" in data

    def test_health_status_ok(self):
        """Testa se o status retornado é 'ok'."""
        response = client.get("/api/health")
        data = response.json()
        assert data["status"] == "ok"

    def test_health_service_name(self):
        """Testa se o nome do serviço está correto."""
        response = client.get("/api/health")
        data = response.json()
        assert "Travel Planner" in data["service"]

    def test_health_version_present(self):
        """Testa se a versão está presente."""
        response = client.get("/api/health")
        data = response.json()
        assert data["version"] == "1.0.0"

    def test_health_llm_enabled_is_boolean(self):
        """Testa se llm_enabled é um booleano."""
        response = client.get("/api/health")
        data = response.json()
        assert isinstance(data["llm_enabled"], bool)

    def test_health_active_logs_is_integer(self):
        """Testa se active_logs é um inteiro."""
        response = client.get("/api/health")
        data = response.json()
        assert isinstance(data["active_logs"], int)
        assert data["active_logs"] >= 0

    def test_health_llm_enabled_depends_on_env(self):
        """Testa se llm_enabled reflete a presença da GEMINI_API_KEY."""
        response = client.get("/api/health")
        data = response.json()

        # Verifica se a lógica está correta (sem alterar env real)
        has_api_key = bool(os.environ.get("GEMINI_API_KEY"))
        assert data["llm_enabled"] == has_api_key
