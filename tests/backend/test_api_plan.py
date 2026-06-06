"""
test_api_plan.py — Testes para o endpoint POST /api/plan
"""

import os
import sys
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestPlanEndpoint:
    """Testes para o endpoint POST /api/plan"""

    def test_plan_valid_request(self, sample_plan_request_data):
        """Testa requisição válida retorna request_id e status processing."""
        response = client.post("/api/plan", json=sample_plan_request_data)
        assert response.status_code == 200

        data = response.json()
        assert "request_id" in data
        assert len(data["request_id"]) > 0
        assert data["status"] == "processing"
        assert "message" in data

    def test_plan_returns_valid_uuid(self, sample_plan_request_data):
        """Testa se o request_id retornado é um UUID válido."""
        import uuid

        response = client.post("/api/plan", json=sample_plan_request_data)
        data = response.json()

        # Tenta fazer parse do UUID (deve funcionar se for válido)
        try:
            uuid.UUID(data["request_id"], version=4)
            is_valid_uuid = True
        except ValueError:
            is_valid_uuid = False

        assert is_valid_uuid is True

    def test_plan_missing_cidade_destino(self):
        """Testa se cidade_destino é obrigatório."""
        invalid_data = {"data_saida": "2026-08-01", "data_retorno": "2026-08-10"}

        response = client.post("/api/plan", json=invalid_data)
        # FastAPI deve retornar 422 (Unprocessable Entity)
        assert response.status_code == 422

    def test_plan_missing_dates(self):
        """Testa se datas são obrigatórias."""
        invalid_data = {"cidade_destino": "Paris"}

        response = client.post("/api/plan", json=invalid_data)
        assert response.status_code == 422

    def test_plan_invalid_date_format(self):
        """Testa se formato inválido de data é rejeitado."""
        invalid_data = {
            "cidade_destino": "Paris",
            "data_saida": "01/08/2026",  # Formato inválido (deveria ser YYYY-MM-DD)
            "data_retorno": "2026-08-10",
        }

        response = client.post("/api/plan", json=invalid_data)
        assert response.status_code == 422

    def test_plan_with_optional_fields(self):
        """Testa requisição com todos os campos opcionais."""
        full_data = {
            "cidade_destino": "Tóquio",
            "data_saida": "2026-09-01",
            "data_retorno": "2026-09-15",
            "cidade_origem": "São Paulo",
            "quantidade_viajantes": 3,
            "preferencia_voo": "menor_duracao",
            "preferencia_hotel": "luxo",
            "categoria_hotel": "5 estrelas",
            "ritmo_roteiro": "intenso",
            "interesses": ["cultura", "tecnologia", "gastronomia"],
        }

        response = client.post("/api/plan", json=full_data)
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "processing"

    def test_plan_quantidade_viajantes_default(self, sample_plan_request_data):
        """Testa se quantidade_viajantes tem valor padrão 1."""
        # Remove quantidade_viajantes do request
        data = sample_plan_request_data.copy()
        del data["quantidade_viajantes"]

        response = client.post("/api/plan", json=data)
        # Deve aceitar pois tem default=1
        assert response.status_code == 200

    def test_plan_negative_quantidade_viajantes(self):
        """Testa se quantidade_viajantes negativa é rejeitada."""
        invalid_data = {
            "cidade_destino": "Paris",
            "data_saida": "2026-08-01",
            "data_retorno": "2026-08-10",
            "quantidade_viajantes": -1,  # Inválido: deve ser >= 1
        }

        response = client.post("/api/plan", json=invalid_data)
        assert response.status_code == 422

    def test_plan_response_message_format(self, sample_plan_request_data):
        """Testa se a mensagem de resposta contém informações úteis"""
        response = client.post("/api/plan", json=sample_plan_request_data)
        data = response.json()

        # Verifica se a mensagem contém o request_id ou instruções de uso
        assert "request_id" in data or "message" in data

        # Se tem message, verifica se contém o request_id ou instruções
        if "message" in data:
            assert "request_id" in data["message"] or "/api/stream/" in data["message"]
