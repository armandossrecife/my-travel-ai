"""
test_api_result.py — Testes para o endpoint GET /api/result/{request_id}
"""

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestResultEndpoint:
    """Testes para o endpoint GET /api/result/{request_id}"""

    def test_result_invalid_request_id(self):
        """Testa request_id inexistente."""
        response = client.get("/api/result/request-inexistente-12345")
        assert response.status_code == 200

        data = response.json()
        # Deve retornar status "processing" ou similar para IDs inexistentes
        assert "status" in data or "error" in data

    def test_result_valid_request_id_processing(self):
        """Testa se retorna status 'processing' durante processamento."""
        plan_data = {
            "cidade_destino": "Lisboa",
            "data_saida": "2026-07-10",
            "data_retorno": "2026-07-17",
        }

        plan_response = client.post("/api/plan", json=plan_data)
        assert plan_response.status_code == 200

        request_id = plan_response.json()["request_id"]

        # Consulta o resultado (pode estar processando ainda)
        result_response = client.get(f"/api/result/{request_id}")
        assert result_response.status_code == 200

        data = result_response.json()
        # Pode ser "processing" ou o resultado final
        assert "status" in data or "request_id" in data or "cidade_destino" in data

    def test_result_response_structure(self):
        """Testa se a estrutura da resposta está correta."""
        plan_data = {
            "cidade_destino": "Lisboa",
            "data_saida": "2026-07-10",
            "data_retorno": "2026-07-17",
        }

        plan_response = client.post("/api/plan", json=plan_data)
        assert plan_response.status_code == 200

        request_id = plan_response.json()["request_id"]

        result_response = client.get(f"/api/result/{request_id}")
        assert result_response.status_code == 200

        data = result_response.json()

        # Verifica se é um JSON válido
        assert isinstance(data, dict)

        # Pode estar processando ou já ter concluído, pois a heurística local é rápida.
        if "status" in data:
            assert data["status"] in ("processing", "sucesso", "parcial", "erro")

    def test_result_request_id_format(self):
        """Testa se o request_id tem formato válido (UUID)."""
        plan_data = {
            "cidade_destino": "Lisboa",
            "data_saida": "2026-07-10",
            "data_retorno": "2026-07-17",
        }

        plan_response = client.post("/api/plan", json=plan_data)
        assert plan_response.status_code == 200

        request_id = plan_response.json()["request_id"]

        # Verifica se é um UUID válido (formato)
        import re

        uuid_pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
        assert re.match(uuid_pattern, request_id, re.IGNORECASE)

    def test_result_multiple_requests_different_ids(self):
        """Testa se requisições diferentes geram IDs diferentes."""
        plan_data_1 = {
            "cidade_destino": "Lisboa",
            "data_saida": "2026-07-10",
            "data_retorno": "2026-07-17",
        }

        plan_data_2 = {
            "cidade_destino": "Paris",
            "data_saida": "2026-08-01",
            "data_retorno": "2026-08-10",
        }

        response_1 = client.post("/api/plan", json=plan_data_1)
        response_2 = client.post("/api/plan", json=plan_data_2)

        assert response_1.status_code == 200
        assert response_2.status_code == 200

        request_id_1 = response_1.json()["request_id"]
        request_id_2 = response_2.json()["request_id"]

        assert request_id_1 != request_id_2

    def test_result_endpoint_returns_json(self):
        """Testa se o endpoint retorna JSON."""
        plan_data = {
            "cidade_destino": "Lisboa",
            "data_saida": "2026-07-10",
            "data_retorno": "2026-07-17",
        }

        plan_response = client.post("/api/plan", json=plan_data)
        assert plan_response.status_code == 200

        request_id = plan_response.json()["request_id"]

        result_response = client.get(f"/api/result/{request_id}")
        assert result_response.status_code == 200
        assert result_response.headers["content-type"] == "application/json"
