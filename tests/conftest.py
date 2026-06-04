"""
conftest.py - Configurações compartilhadas para testes pytest
"""

import os
import sys
from datetime import date, timedelta

import pytest

# Adiciona o diretório raiz ao path para importar módulos do projeto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models import ExecutionMetadata, TravelContext, TravelPreferences, TravelRequest

# ── Fixtures para Backend ─────────────────────────────────────────


@pytest.fixture
def sample_travel_request():
    """Fixture com uma requisição de viagem válida."""
    return TravelRequest(
        cidade_destino="Lisboa",
        data_saida=date(2026, 7, 10),
        data_retorno=date(2026, 7, 17),
        cidade_origem="Teresina",
        preferencias=TravelPreferences(
            quantidade_viajantes=2,
            quantidade_hospedes=2,
            quantidade_quartos=1,
            preferencia_voo="melhor_custo_beneficio",
            preferencia_hotel="melhor_custo_beneficio",
            ritmo_roteiro="moderado",
            interesses=["historia", "gastronomia"],
        ),
    )


@pytest.fixture
def sample_travel_context():
    """Fixture com um contexto de viagem válido para os agentes."""
    return TravelContext(
        request_id="test-001",
        cidade_destino="Lisboa",
        data_saida=date(2026, 7, 10),
        data_retorno=date(2026, 7, 17),
        cidade_origem="Teresina",
        quantidade_dias=8,
        quantidade_noites=7,
        preferencias=TravelPreferences(),
        execucao=ExecutionMetadata(),
    )


@pytest.fixture
def sample_plan_request_data():
    """Fixture com dados para PlanRequest (API)."""
    return {
        "cidade_destino": "Paris",
        "data_saida": "2026-08-01",
        "data_retorno": "2026-08-10",
        "cidade_origem": "São Paulo",
        "quantidade_viajantes": 2,
        "preferencia_voo": "menor_preco",
        "preferencia_hotel": "melhor_custo_beneficio",
        "ritmo_roteiro": "moderado",
        "interesses": ["museus", "gastronomia"],
    }


@pytest.fixture
def invalid_plan_request_data():
    """Fixture com dados inválidos para testar validações."""
    return {
        "cidade_destino": "",  # Inválido: vazio
        "data_saida": "2026-08-10",
        "data_retorno": "2026-08-01",  # Inválido: retorno anterior à saída
        "quantidade_viajantes": 0,  # Inválido: menor que 1
    }


# ── Fixtures para Frontend ────────────────────────────────────────


@pytest.fixture
def sample_form_data():
    """Fixture com dados simulados do formulário HTML."""
    return {
        "cidade_destino": "Rio de Janeiro",
        "data_saida": "2026-12-15",
        "data_retorno": "2026-12-22",
        "cidade_origem": "São Paulo",
        "quantidade_viajantes": 4,
        "ritmo_roteiro": "intenso",
        "interesses": ["praia", "trilhas"],
        "preferencia_voo": "menor_duracao",
        "preferencia_hotel": "luxo",
    }


@pytest.fixture
def sample_api_response():
    """Fixture com resposta simulada da API."""
    return {
        "request_id": "550e8400-e29b-41d4-a716-446655440000",
        "status": "processing",
        "message": "Processamento iniciado. Use GET /api/stream/... para acompanhar.",
    }


# ── Helpers ───────────────────────────────────────────────────────


@pytest.fixture
def make_request():
    """Factory para criar TravelRequest com parâmetros customizados."""

    def _make_request(**kwargs):
        defaults = {
            "cidade_destino": "Lisboa",
            "data_saida": date(2026, 7, 10),
            "data_retorno": date(2026, 7, 17),
            "cidade_origem": "Teresina",
        }
        defaults.update(kwargs)
        return TravelRequest(**defaults)

    return _make_request


@pytest.fixture
def make_context():
    """Factory para criar TravelContext com parâmetros customizados."""

    def _make_context(**kwargs):
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

    return _make_context
