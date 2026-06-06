"""
test_full_flow.py — Teste de integração do fluxo completo
"""

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestFullFlow:
    """Testes de integração do fluxo completo: API → Agentes"""

    def test_complete_flow_plan_to_result(self):
        """
        Testa o fluxo completo:
        1. POST /api/plan com dados válidos
        2. Captura request_id
        3. GET /api/result/{request_id} até obter resultado
        4. Valida estrutura do resultado final
        """
        # 1. Envia requisição
        plan_data = {
            "cidade_destino": "Lisboa",
            "data_saida": "2026-07-10",
            "data_retorno": "2026-07-17",
            "cidade_origem": "Teresina",
            "quantidade_viajantes": 2,
            "preferencia_voo": "melhor_custo_beneficio",
            "ritmo_roteiro": "moderado",
        }

        response = client.post("/api/plan", json=plan_data)
        assert response.status_code == 200

        data = response.json()
        request_id = data["request_id"]
        assert len(request_id) > 0

        # 2. Faz polling no endpoint de resultado
        max_attempts = 30  # Tenta por até 30 segundos
        result = None

        for attempt in range(max_attempts):
            result_response = client.get(f"/api/result/{request_id}")
            assert result_response.status_code == 200

            result = result_response.json()

            # Se não estiver mais processando, sai do loop
            if result.get("status") != "processing":
                break

            time.sleep(1)  # Aguarda 1 segundo antes da próxima tentativa

        # 3. Valida estrutura do resultado final
        assert result is not None, "Resultado não foi obtido"

        # Verifica se tem os campos esperados de um TravelPlan
        assert "cidade_destino" in result or "resumo" in result
        assert "resultado" in result or "alertas" in result

        # Verifica se os agentes executaram
        if "resultado" in result:
            assert "passagens_aereas" in result["resultado"]
            assert "hoteis" in result["resultado"]
            assert "roteiro_turistico" in result["resultado"]

    def test_flow_with_different_destinations(self):
        """Testa fluxo com diferentes destinos."""
        destinations = ["Paris", "Tóquio", "Nova York"]

        for destino in destinations:
            plan_data = {
                "cidade_destino": destino,
                "data_saida": "2026-08-01",
                "data_retorno": "2026-08-10",
            }

            response = client.post("/api/plan", json=plan_data)
            assert response.status_code == 200

            data = response.json()
            assert "request_id" in data
            assert data["status"] == "processing"

    def test_flow_with_optional_fields(self):
        """Testa fluxo com todos os campos opcionais preenchidos."""
        plan_data = {
            "cidade_destino": "Rio de Janeiro",
            "data_saida": "2026-12-15",
            "data_retorno": "2026-12-22",
            "cidade_origem": "São Paulo",
            "quantidade_viajantes": 4,
            "preferencia_voo": "menor_duracao",
            "preferencia_hotel": "luxo",
            "categoria_hotel": "5 estrelas",
            "ritmo_roteiro": "intenso",
            "interesses": ["praia", "trilhas", "gastronomia"],
        }

        response = client.post("/api/plan", json=plan_data)
        assert response.status_code == 200

        data = response.json()
        request_id = data["request_id"]

        # Apenas verifica se o request_id foi gerado
        assert len(request_id) > 0

    def test_flow_result_structure(self):
        """Testa estrutura detalhada do resultado."""
        plan_data = {
            "cidade_destino": "Lisboa",
            "data_saida": "2026-07-10",
            "data_retorno": "2026-07-17",
        }

        response = client.post("/api/plan", json=plan_data)
        request_id = response.json()["request_id"]

        # Aguarda processamento (até 30 segundos)
        for _ in range(30):
            result_response = client.get(f"/api/result/{request_id}")
            result = result_response.json()

            if result.get("status") != "processing":
                # Validações de estrutura
                if "resumo" in result:
                    assert "cidade_destino" in result["resumo"]
                    assert "duracao_dias" in result["resumo"]

                if "resultado" in result:
                    resultado = result["resultado"]

                    if "passagens_aereas" in resultado:
                        assert "status" in resultado["passagens_aereas"]
                        assert "data" in resultado["passagens_aereas"]

                    if "hoteis" in resultado:
                        assert "status" in resultado["hoteis"]
                        assert "data" in resultado["hoteis"]

                    if "roteiro_turistico" in resultado:
                        assert "status" in resultado["roteiro_turistico"]
                        assert "data" in resultado["roteiro_turistico"]

                break

            time.sleep(1)


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
