"""
test_models.py — Testes para os modelos Pydantic (models.py)
"""

import os
import sys
from datetime import date, datetime

from pydantic import ValidationError

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from app.models import (
    AgentResult,
    CostEstimation,
    DailyItinerary,
    ExecutionMetadata,
    FlightOption,
    HotelOption,
    IntegratedPlan,
    TouristAttraction,
    TravelContext,
    TravelPreferences,
    TravelRequest,
)


class TestTravelPreferences:
    """Testes para o modelo TravelPreferences"""

    def test_default_values(self):
        """Testa se os valores padrão estão corretos."""
        prefs = TravelPreferences()
        assert prefs.quantidade_viajantes == 1
        assert prefs.quantidade_hospedes == 1
        assert prefs.quantidade_quartos == 1
        assert prefs.preferencia_voo == "melhor_custo_beneficio"
        assert prefs.preferencia_hotel == "melhor_custo_beneficio"
        assert prefs.categoria_hotel is None
        assert prefs.ritmo_roteiro == "moderado"
        assert prefs.interesses == []

    def test_custom_values(self):
        """Testa atribuição de valores customizados."""
        prefs = TravelPreferences(
            quantidade_viajantes=4,
            preferencia_voo="menor_preco",
            interesses=["praia", "trilhas"],
        )
        assert prefs.quantidade_viajantes == 4
        assert prefs.preferencia_voo == "menor_preco"
        assert "praia" in prefs.interesses

    def test_quantidade_viajantes_minimum(self):
        """Testa se quantidade_viajantes aceita valor 1 (mínimo)."""
        prefs = TravelPreferences(quantidade_viajantes=1)
        assert prefs.quantidade_viajantes == 1

    def test_interesses_list(self):
        """Testa se interesses é uma lista."""
        prefs = TravelPreferences(interesses=["museus", "gastronomia"])
        assert isinstance(prefs.interesses, list)
        assert len(prefs.interesses) == 2


class TestTravelRequest:
    """Testes para o modelo TravelRequest"""

    def test_valid_request(self):
        """Testa criação de requisição válida."""
        req = TravelRequest(
            cidade_destino="Lisboa",
            data_saida=date(2026, 7, 10),
            data_retorno=date(2026, 7, 17),
        )
        assert req.cidade_destino == "Lisboa"
        assert req.data_saida == date(2026, 7, 10)
        assert req.data_retorno == date(2026, 7, 17)

    def test_missing_required_fields(self):
        """Testa se campos obrigatórios são validados."""
        import pytest

        with pytest.raises(ValidationError):
            TravelRequest(
                data_saida=date(2026, 7, 10),
                data_retorno=date(2026, 7, 17),
                # Falta cidade_destino
            )

    def test_optional_cidade_origem(self):
        """Testa se cidade_origem é opcional."""
        req = TravelRequest(
            cidade_destino="Paris",
            data_saida=date(2026, 8, 1),
            data_retorno=date(2026, 8, 10),
            # Sem cidade_origem
        )
        assert req.cidade_origem is None

    def test_with_cidade_origem(self):
        """Testa com cidade_origem preenchida."""
        req = TravelRequest(
            cidade_destino="Tóquio",
            data_saida=date(2026, 9, 1),
            data_retorno=date(2026, 9, 15),
            cidade_origem="São Paulo",
        )
        assert req.cidade_origem == "São Paulo"

    def test_default_preferences(self):
        """Testa se preferencias tem valor padrão."""
        req = TravelRequest(
            cidade_destino="Lisboa",
            data_saida=date(2026, 7, 10),
            data_retorno=date(2026, 7, 17),
        )
        assert isinstance(req.preferencias, TravelPreferences)


class TestTravelContext:
    """Testes para o modelo TravelContext"""

    def test_valid_context(self, sample_travel_context):
        """Testa criação de contexto válido."""
        ctx = sample_travel_context
        assert ctx.request_id == "test-001"
        assert ctx.cidade_destino == "Lisboa"
        assert ctx.quantidade_dias == 8
        assert ctx.quantidade_noites == 7

    def test_calculate_days(self):
        """Testa se quantidade_dias é calculada corretamente."""
        ctx = TravelContext(
            request_id="test-002",
            cidade_destino="Rio",
            data_saida=date(2026, 12, 1),
            data_retorno=date(2026, 12, 10),
            cidade_origem="SP",
            quantidade_dias=10,
            quantidade_noites=9,
            preferencias=TravelPreferences(),
            execucao=ExecutionMetadata(),
        )
        assert ctx.quantidade_dias == 10
        assert ctx.quantidade_noites == 9


class TestFlightOption:
    """Testes para o modelo FlightOption"""

    def test_valid_flight(self):
        """Testa criação de opção de voo válida."""
        flight = FlightOption(
            companhia="LATAM",
            origem="GRU",
            destino="LIS",
            data_ida=date(2026, 7, 10),
            data_volta=date(2026, 7, 17),
        )
        assert flight.companhia == "LATAM"
        assert flight.preco_estimado is None  # Opcional
        assert flight.escalas == 0  # Padrão

    def test_flight_with_price(self):
        """Testa opção de voo com preço."""
        flight = FlightOption(
            companhia="TAP",
            origem="GRU",
            destino="LIS",
            data_ida=date(2026, 7, 10),
            data_volta=date(2026, 7, 17),
            preco_estimado=3500.50,
            moeda="BRL",
        )
        assert flight.preco_estimado == 3500.50
        assert flight.moeda == "BRL"


class TestHotelOption:
    """Testes para o modelo HotelOption"""

    def test_valid_hotel(self):
        """Testa criação de opção de hotel válida."""
        hotel = HotelOption(
            nome="Hotel Lisboa Palace", bairro="Baixa", preco_estimado_diaria=150.00
        )
        assert hotel.nome == "Hotel Lisboa Palace"
        assert hotel.avaliacao is None  # Opcional
        assert hotel.destaques == []  # Lista vazia padrão

    def test_hotel_with_rating(self):
        """Testa hotel com avaliação."""
        hotel = HotelOption(
            nome="Luxury Hotel",
            categoria="5 estrelas",
            preco_estimado_diaria=500.00,
            avaliacao="4.8/5",
            destaques=["piscina", "spa", "vista mar"],
        )
        assert hotel.avaliacao == "4.8/5"
        assert len(hotel.destaques) == 3


class TestAgentResult:
    """Testes para o modelo AgentResult"""

    def test_valid_agent_result(self):
        """Testa criação de resultado de agente válido."""
        result = AgentResult(
            agent_name="agente_aereo", status="sucesso", data={"opcoes": []}
        )
        assert result.agent_name == "agente_aereo"
        assert result.status == "sucesso"
        assert result.data == {"opcoes": []}
        assert result.alertas == []  # Lista vazia padrão

    def test_agent_result_status_values(self):
        """Testa valores válidos para status."""
        for status in ["sucesso", "parcial", "erro"]:
            result = AgentResult(agent_name="test", status=status, data={})
            assert result.status == status

    def test_agent_result_with_errors(self):
        """Testa resultado com erros."""
        result = AgentResult(
            agent_name="agente_test",
            status="erro",
            data={},
            erros=["Erro de conexão", "Timeout"],
        )
        assert len(result.erros) == 2
        assert result.status == "erro"


class TestCostEstimation:
    """Testes para o modelo CostEstimation"""

    def test_default_cost(self):
        """Testa valores padrão de custo."""
        cost = CostEstimation()
        assert cost.passagens is None
        assert cost.hospedagem is None
        assert cost.passeios is None
        assert cost.total_estimado is None
        assert cost.moeda == "BRL"

    def test_with_values(self):
        """Testa com valores preenchidos."""
        cost = CostEstimation(
            passagens=1500.00,
            hospedagem=3000.00,
            passeios=800.00,
            total_estimado=5300.00,
        )
        assert cost.total_estimado == 5300.00
