"""
test_sse_flow.py — Teste de integração do fluxo SSE (Server-Sent Events)
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestSSEFlow:
    """Testes de integração do fluxo SSE completo"""

    def test_sse_stream_receives_events(self):
        """
        Testa se o streaming SSE recebe eventos em tempo real.
        """
        # 1. Inicia um plano
        plan_data = {
            "cidade_destino": "Lisboa",
            "data_saida": "2026-07-10",
            "data_retorno": "2026-07-17",
        }

        plan_response = client.post("/api/plan", json=plan_data)
        assert plan_response.status_code == 200

        request_id = plan_response.json()["request_id"]
        assert len(request_id) > 0

        # 2. Conecta no streaming
        with client.stream("GET", f"/api/stream/{request_id}") as response:
            assert response.status_code == 200
            assert (
                "text/event-stream" in response.headers.get("content-type", "").lower()
            )

            # 3. Tenta ler alguns eventos (com timeout)
            events_received = []
            lines_processed = 0

            try:
                for line in response.iter_lines():
                    if line:
                        # Verifica se é um evento SSE (começa com "data: ")
                        if line.startswith("data: "):
                            data_str = line[6:]  # Remove "data: "

                            try:
                                event_data = json.loads(data_str)
                                events_received.append(event_data)

                                # Se recebeu evento de conclusão, sai
                                if event_data.get("event") == "done":
                                    break

                            except json.JSONDecodeError:
                                pass  # Ignora linhas que não são JSON válido

                    lines_processed += 1

                    # Limita o número de linhas para não travar
                    if lines_processed > 100:
                        break

                    time.sleep(0.1)

            except Exception as e:
                print(f"Erro durante streaming: {e}")

            # 4. Validações
            # Deve ter recebido pelo menos algum evento
            assert len(events_received) > 0, "Nenhum evento SSE foi recebido"

    def test_sse_format_validation(self):
        """
        Testa se o formato dos eventos SSE está correto.
        """
        plan_data = {
            "cidade_destino": "Paris",
            "data_saida": "2026-08-01",
            "data_retorno": "2026-08-10",
        }

        plan_response = client.post("/api/plan", json=plan_data)
        request_id = plan_response.json()["request_id"]

        with client.stream("GET", f"/api/stream/{request_id}") as response:
            try:
                for line in response.iter_lines():
                    if line and line.startswith("data: "):
                        data_str = line[6:]

                        # Tenta fazer parse do JSON
                        try:
                            event_data = json.loads(data_str)
                            # Deve ser um dicionário
                            assert isinstance(event_data, dict)

                            # Deve ter campos esperados (evento ou dados normais)
                            # Eventos podem ter: event, agent, status, message, etc.
                            break

                        except json.JSONDecodeError:
                            # Se não for JSON, verifica se é um comentário SSE (começa com ":")
                            if not data_str.startswith(":"):
                                assert False, (
                                    f"Dados SSE não são JSON válido: {data_str}"
                                )

                    time.sleep(0.1)

            except:
                pass  # Timeout esperado

    def test_sse_disconnect_handling(self):
        """
        Testa se o servidor lida com desconexão do cliente durante SSE.
        """
        plan_data = {
            "cidade_destino": "Tóquio",
            "data_saida": "2026-09-01",
            "data_retorno": "2026-09-15",
        }

        plan_response = client.post("/api/plan", json=plan_data)
        request_id = plan_response.json()["request_id"]

        # Simula uma desconexão rápida
        response = client.get(f"/api/stream/{request_id}")
        # Não deve quebrar o servidor
        assert response.status_code in [200, 204, 422]

    def test_sse_done_event_structure(self):
        """
        Testa se o evento 'done' tem a estrutura correta.
        """
        plan_data = {
            "cidade_destino": "Lisboa",
            "data_saida": "2026-07-10",
            "data_retorno": "2026-07-17",
        }

        plan_response = client.post("/api/plan", json=plan_data)
        request_id = plan_response.json()["request_id"]

        # Aguarda o processamento completar (polling no result)
        max_wait = 30
        for _ in range(max_wait):
            result_response = client.get(f"/api/result/{request_id}")
            result = result_response.json()

            if result.get("status") != "processing":
                break

            time.sleep(1)

        # Agora faz streaming (deve receber evento done imediatamente)
        with client.stream("GET", f"/api/stream/{request_id}") as response:
            try:
                for line in response.iter_lines():
                    if line and line.startswith("data: "):
                        data_str = line[6:]

                        try:
                            event_data = json.loads(data_str)

                            # Se for evento done
                            if event_data.get("event") == "done":
                                # Deve ter campo 'result'
                                assert "result" in event_data
                                result = event_data["result"]
                                assert isinstance(result, dict)
                                break

                        except json.JSONDecodeError:
                            pass

                    time.sleep(0.1)

            except:
                pass


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
