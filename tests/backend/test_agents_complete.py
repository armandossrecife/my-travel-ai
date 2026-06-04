"""
tests/test_agents.py — Testes unitários da aplicação multiagente de viagens.

Cobre validação do Maestro, resiliência do fluxo e contratos dos agentes.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date, timedelta

import pytest

from agents import aereo, hotel, maestro, turismo
from models import ExecutionMetadata, TravelContext, TravelPreferences, TravelRequest

# ── Fixtures ──────────────────────────────────────────────────────


def make_request(**kwargs) -> TravelRequest:
    defaults = {
        "cidade_destino": "Lisboa",
        "data_saida": date(2026, 7, 10),
        "data_retorno": date(2026, 7, 17),
        "cidade_origem": "Teresina",
    }
    defaults.update(kwargs)
    return TravelRequest(**defaults)


def make_context(**kwargs) -> TravelContext:
    ctx_defaults = {
        "request_id": "test-001",
        "cidade_destino": "Lisboa",
        "data_saida": date(2026, 7, 10),
        "data_retorno": date(2026, 7, 17),
        "cidade_origem": "Teresina",
        "quantidade_dias": 8,
        "quantidade_noites": 7,
        "preferencias": TravelPreferences(),
        "execucao": ExecutionMetadata(),
    }
    ctx_defaults.update(kwargs)
    return TravelContext(**ctx_defaults)


# ── Testes de Validação do Maestro ────────────────────────────────


class TestMaestroValidacao:
    def test_rejeita_cidade_destino_ausente(self):
        req = make_request(cidade_destino="")
        plano = maestro.run(req)
        assert plano.status == "erro"
        assert any("cidade_destino" in e for e in plano.alertas)

    def test_rejeita_data_retorno_anterior_a_saida(self):
        req = make_request(
            data_saida=date(2026, 7, 17),
            data_retorno=date(2026, 7, 10),
        )
        plano = maestro.run(req)
        assert plano.status == "erro"
        assert any("data_retorno" in e for e in plano.alertas)

    def test_rejeita_datas_iguais(self):
        req = make_request(
            data_saida=date(2026, 7, 10),
            data_retorno=date(2026, 7, 10),
        )
        plano = maestro.run(req)
        assert plano.status == "erro"

    def test_aceita_entrada_valida(self):
        req = make_request()
        plano = maestro.run(req)
        assert plano.status in ("sucesso", "parcial")

    def test_calcula_dias_e_noites(self):
        req = make_request(
            data_saida=date(2026, 7, 10),
            data_retorno=date(2026, 7, 17),
        )
        plano = maestro.run(req)
        assert plano.resumo["duracao_dias"] == 8
        assert plano.resumo["quantidade_noites"] == 7

    def test_normaliza_cidade_destino(self):
        req = make_request(cidade_destino="  lISBOA  ")
        plano = maestro.run(req)
        assert "Lisboa" in plano.resumo["cidade_destino"]


# ── Testes do Agente Aéreo ────────────────────────────────────────


class TestAgenteAereo:
    def test_retorna_opcoes(self):
        ctx = make_context()
        resultado = aereo.run(ctx)
        assert resultado.status in ("sucesso", "parcial")
        assert isinstance(resultado.data.get("opcoes"), list)
        assert len(resultado.data["opcoes"]) > 0

    def test_opcoes_tem_companhia(self):
        ctx = make_context()
        resultado = aereo.run(ctx)
        for op in resultado.data["opcoes"]:
            assert op["companhia"] is not None
            assert len(op["companhia"]) > 0

    def test_opcoes_tem_preco_estimado(self):
        ctx = make_context()
        resultado = aereo.run(ctx)
        for op in resultado.data["opcoes"]:
            assert op["preco_estimado"] is not None
            assert op["preco_estimado"] > 0

    def test_limitacoes_presentes(self):
        ctx = make_context()
        resultado = aereo.run(ctx)
        assert len(resultado.data.get("limitacoes", [])) > 0

    def test_melhor_opcao_sugerida_presente(self):
        ctx = make_context()
        resultado = aereo.run(ctx)
        assert resultado.data.get("melhor_opcao_sugerida") is not None

    def test_sem_cidade_origem_informa_limitacao(self):
        ctx = make_context(cidade_origem=None)
        resultado = aereo.run(ctx)
        limitacoes = resultado.data.get("limitacoes", [])
        assert any("origem" in l.lower() for l in limitacoes)


# ── Testes do Agente Hotel ────────────────────────────────────────


class TestAgenteHotel:
    def test_retorna_opcoes(self):
        ctx = make_context()
        resultado = hotel.run(ctx)
        assert resultado.status in ("sucesso", "parcial")
        assert len(resultado.data.get("opcoes", [])) > 0

    def test_calcula_noites(self):
        ctx = make_context()
        resultado = hotel.run(ctx)
        assert resultado.data.get("quantidade_noites") == 7

    def test_preco_total_coerente(self):
        ctx = make_context()
        resultado = hotel.run(ctx)
        for op in resultado.data["opcoes"]:
            if op.get("preco_estimado_diaria") and op.get("preco_estimado_total"):
                assert op["preco_estimado_total"] > op["preco_estimado_diaria"]

    def test_regioes_recomendadas(self):
        ctx = make_context()
        resultado = hotel.run(ctx)
        assert len(resultado.data.get("regioes_recomendadas", [])) > 0


# ── Testes do Agente Turismo ──────────────────────────────────────


class TestAgenteTurismo:
    def test_retorna_roteiro(self):
        ctx = make_context()
        resultado = turismo.run(ctx)
        assert resultado.status in ("sucesso", "parcial")
        assert len(resultado.data.get("roteiro_por_dia", [])) > 0

    def test_numero_correto_de_dias(self):
        ctx = make_context()
        resultado = turismo.run(ctx)
        roteiro = resultado.data["roteiro_por_dia"]
        assert len(roteiro) == 8  # 8 dias (saída 10/7, retorno 17/7)

    def test_primeiro_dia_chegada(self):
        ctx = make_context()
        resultado = turismo.run(ctx)
        primeiro = resultado.data["roteiro_por_dia"][0]
        assert (
            "chegada" in primeiro["tema"].lower()
            or "adaptação" in primeiro["tema"].lower()
        )

    def test_ultimo_dia_retorno(self):
        ctx = make_context()
        resultado = turismo.run(ctx)
        ultimo = resultado.data["roteiro_por_dia"][-1]
        assert "despedida" in ultimo["tema"].lower()

    def test_pontos_turisticos_presentes(self):
        ctx = make_context()
        resultado = turismo.run(ctx)
        assert len(resultado.data.get("pontos_turisticos_prioritarios", [])) > 0

    def test_dicas_presentes(self):
        ctx = make_context()
        resultado = turismo.run(ctx)
        assert len(resultado.data.get("dicas", [])) > 0


# ── Teste de Resiliência (Falha Parcial) ──────────────────────────


class TestResilienciaFluxo:
    def test_plano_parcial_com_destino_generico(self):
        """Destino desconhecido usa heurística default e retorna resultado."""
        req = make_request(cidade_destino="Ziguinchor")
        plano = maestro.run(req)
        # Status deve ser sucesso ou parcial, nunca erro por destino desconhecido
        assert plano.status in ("sucesso", "parcial")
        assert "passagens_aereas" in plano.resultado
        assert "hoteis" in plano.resultado
        assert "roteiro_turistico" in plano.resultado

    def test_request_id_unico(self):
        """Cada execução deve gerar um request_id único."""
        req = make_request()
        plano1 = maestro.run(req)
        plano2 = maestro.run(req)
        assert plano1.request_id != plano2.request_id

    def test_alertas_sempre_presentes(self):
        """Resposta final deve sempre conter alertas."""
        req = make_request()
        plano = maestro.run(req)
        assert len(plano.alertas) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
