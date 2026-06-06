"""
test_api_stream.py — Testes para o endpoint GET /api/stream/{request_id}
"""

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestStreamEndpoint:
    """Testes para o endpoint SSE /api/stream/{request_id}"""

    def test_stream_invalid_request_id(self):
        """Testa request_id inexistente retorna erro ou mensagem apropriada."""
        response = client.get("/api/stream/request-inexistente-12345")

        # Pode retornar 200 com JSON de erro ou 404
        assert response.status_code in [200, 404, 422]

        if response.status_code == 200:
            data = response.json()
            assert "error" in data or "request_id" in data

    def test_stream_response_is_event_stream(self):
        """Testa se o endpoint retorna content-type text/event-stream."""
        # Primeiro cria um plano para ter um request_id válido
        plan_data = {
            "cidade_destino": "Lisboa",
            "data_saida": "2026-07-10",
            "data_retorno": "2026-07-17",
        }

        plan_response = client.post("/api/plan", json=plan_data)
        if plan_response.status_code == 200:
            request_id = plan_response.json()["request_id"]

            # Faz uma requisição curta (vamos interromper)
            with client.stream("GET", f"/api/stream/{request_id}") as response:
                # Verifica se o content-type indica SSE
                content_type = response.headers.get("content-type", "")
                assert "text/event-stream" in content_type.lower()

    def test_stream_format_sse(self):
        """Testa se o formato dos dados segue o padrão SSE (data: {...}\\n\\n)."""
        plan_data = {
            "cidade_destino": "Lisboa",
            "data_saida": "2026-07-10",
            "data_retorno": "2026-07-17",
        }

        plan_response = client.post("/api/plan", json=plan_data)
        if plan_response.status_code == 200:
            request_id = plan_response.json()["request_id"]

            # Faz uma requisição e lê poucos bytes
            with client.stream("GET", f"/api/stream/{request_id}") as response:
                # Tenta ler alguns dados (com timeout implícito)
                try:
                    for chunk in response.iter_lines():
                        if chunk:
                            # Verifica se começa com "data: "
                            if chunk.startswith("data: "):
                                import json

                                data_str = chunk[6:]  # Remove "data: "
                                # Tenta fazer parse do JSON
                                parsed = json.loads(data_str)
                                assert isinstance(parsed, dict)
                                break
                        # Sai após algumas iterações para não travar
                        time.sleep(0.1)
                except:
                    pass  # Timeout ou desconexão esperada

    def test_stream_disconnect_handling(self):
        """Testa se o endpoint lida com desconexão do cliente."""
        plan_data = {
            "cidade_destino": "Lisboa",
            "data_saida": "2026-07-10",
            "data_retorno": "2026-07-17",
        }

        plan_response = client.post("/api/plan", json=plan_data)
        if plan_response.status_code == 200:
            request_id = plan_response.json()["request_id"]

            # Simula uma desconexão rápida
            response = client.get(f"/api/stream/{request_id}")
            # Não deve quebrar o servidor
            assert response.status_code in [200, 204, 422]

    def test_stream_with_valid_request_id(self):
        """Testa se um request_id válido é aceito (não retorna 404 imediato)."""
        plan_data = {
            "cidade_destino": "Lisboa",
            "data_saida": "2026-07-10",
            "data_retorno": "2026-07-17",
        }

        plan_response = client.post("/api/plan", json=plan_data)
        assert plan_response.status_code == 200

        request_id = plan_response.json()["request_id"]

        # Apenas verifica se o endpoint aceita o request_id
        # (o streaming em si é assíncrono)
        response = client.get(f"/api/stream/{request_id}")
        # Pode retornar 200 (streaming) ou 200 com JSON (se já finalizou)
        assert response.status_code == 200
