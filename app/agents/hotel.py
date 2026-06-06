"""
agente_hotel.py — Agente especializado em busca e análise de hospedagens.

Implementa a lógica de geração e ranking de opções de hotéis seguindo os contratos
definidos em skill.md e plano.md. Suporta engine LLM (Google Gemini) e engine
de heurística local como fallback.
"""

import json
import os
from typing import List

from app.agents.logger import log_info
from app.models import AgentResult, HotelOption, TravelContext

from app.agents.base_local import _CONHECIMENTO_HOTEL
from app.agents.config import MODELO_LMM

def _calcular_score_hotel(hotel: dict, preco_min: float, preco_max: float) -> float:
    """Calcula score ponderado de um hotel conforme skill.md."""
    # Nota localização: mapeada pela categoria do hotel
    categorias = {
        "5 estrelas": 1.0,
        "4 estrelas": 0.8,
        "3 estrelas": 0.6,
        "2 estrelas": 0.4,
        "1 estrela": 0.2,
    }
    nota_localizacao = categorias.get(hotel.get("categoria", "3 estrelas"), 0.6)

    # Nota avaliação: parse de "X.X/10"
    try:
        nota_avaliacao = float(hotel["avaliacao"].split("/")[0]) / 10
    except Exception:
        nota_avaliacao = 0.8

    # Nota preço: invertido, menor = melhor
    span = max(preco_max - preco_min, 1)
    nota_preco = max(0, 1 - (hotel["preco_diaria"] - preco_min) / span)

    nota_comodidades = min(1.0, len(hotel.get("destaques", [])) / 5)

    score = (
        0.35 * nota_localizacao
        + 0.25 * nota_avaliacao
        + 0.25 * nota_preco
        + 0.15 * nota_comodidades
    )
    return round(score, 4)


def _gerar_opcoes_heuristica(ctx: TravelContext) -> dict:
    """Gera opções de hotéis usando heurística local."""
    destino_key = ctx.cidade_destino.lower().strip()
    conhecimento = _CONHECIMENTO_HOTEL.get(destino_key, _CONHECIMENTO_HOTEL["default"])
    quantidade_noites = ctx.quantidade_noites

    hoteis_raw = conhecimento["hoteis"]
    precos = [h["preco_diaria"] for h in hoteis_raw]
    preco_min = min(precos)
    preco_max = max(precos)

    # Fator sazonalidade
    mes = ctx.data_saida.month
    fator = 1.30 if mes in [1, 7, 12] else (1.15 if mes in [6, 8, 11] else 1.0)

    opcoes: List[HotelOption] = []
    for hotel in hoteis_raw:
        diaria = round(hotel["preco_diaria"] * fator, 2)
        total = round(diaria * quantidade_noites, 2)
        score = _calcular_score_hotel(hotel, preco_min * fator, preco_max * fator)

        opcoes.append(
            HotelOption(
                nome=hotel["nome"],
                bairro=hotel["bairro"],
                categoria=hotel["categoria"],
                preco_estimado_total=total,
                preco_estimado_diaria=diaria,
                moeda="BRL",
                avaliacao=hotel["avaliacao"],
                destaques=hotel["destaques"],
                link_consulta=None,
                observacoes="Tarifa estimada. Confirme disponibilidade em sites de reserva.",
                score=score,
            )
        )

    opcoes.sort(key=lambda x: x.score, reverse=True)
    return {
        "opcoes": opcoes,
        "regioes_recomendadas": conhecimento["regioes_recomendadas"],
    }


def _gerar_opcoes_llm(ctx: TravelContext) -> dict:
    """Gera opções de hotéis usando LLM (Google Gemini)."""
    try:
        from google import genai

        api_key = os.environ.get("GEMINI_API_KEY", "")
        if not api_key:
            raise ValueError("GEMINI_API_KEY não configurada.")

        client = genai.Client(api_key=api_key)
        quantidade_noites = ctx.quantidade_noites

        prompt = f"""Você é o agente_hotel, especialista em hospedagens.

Dados da viagem:
- Cidade destino: {ctx.cidade_destino}
- Check-in: {ctx.data_saida}
- Check-out: {ctx.data_retorno}
- Quantidade de noites: {quantidade_noites}
- Hóspedes: {ctx.preferencias.quantidade_hospedes}
- Preferência: {ctx.preferencias.preferencia_hotel}
- Categoria desejada: {ctx.preferencias.categoria_hotel or "sem preferência específica"}

Gere um JSON com as chaves "opcoes" (lista de 3 hotéis) e "regioes_recomendadas" (lista de bairros).
Responda SOMENTE com JSON puro, sem markdown, no formato:
{{
  "opcoes": [
    {{
      "nome": "Nome do hotel",
      "bairro": "Bairro",
      "categoria": "X estrelas",
      "preco_estimado_diaria": 000.00,
      "preco_estimado_total": 000.00,
      "moeda": "BRL",
      "avaliacao": "X.X/10",
      "destaques": ["característica 1", "característica 2"],
      "link_consulta": null,
      "observacoes": "Tarifa estimada. Confirme em sites de reserva.",
      "score": 0.0
    }}
  ],
  "regioes_recomendadas": ["Bairro 1", "Bairro 2"]
}}

REGRAS: Hotéis reais da cidade, preços em BRL, sem links inventados.
"""
        response = client.models.generate_content(
            model=MODELO_LMM,
            contents=prompt,
        )
        raw = response.text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        data = json.loads(raw)

        opcoes = []
        for item in data.get("opcoes", []):
            item.setdefault("score", 0.0)
            opcoes.append(HotelOption(**item))

        return {
            "opcoes": opcoes,
            "regioes_recomendadas": data.get("regioes_recomendadas", []),
        }

    except Exception as e:
        print(f"[agente_hotel] LLM falhou: {e}. Usando heurística local.")
        return _gerar_opcoes_heuristica(ctx)


def run(ctx: TravelContext, request_id: str = None) -> AgentResult:
    """Ponto de entrada do agente_hotel."""
    try:
        log_info(
            request_id, "hotel", f"Iniciando busca de hotéis em {ctx.cidade_destino}"
        )
        use_llm = bool(os.environ.get("GEMINI_API_KEY", ""))
        if use_llm:
            log_info(
                request_id, "hotel", "Usando engine LLM (Gemini) para busca de hotéis"
            )
        else:
            log_info(
                request_id,
                "hotel",
                "Usando engine heurística local para busca de hotéis",
            )

        resultado = _gerar_opcoes_llm(ctx) if use_llm else _gerar_opcoes_heuristica(ctx)

        opcoes = resultado["opcoes"]
        regioes = resultado["regioes_recomendadas"]
        melhor = opcoes[0] if opcoes else None

        melhor_info = None
        if melhor:
            melhor_info = {
                "nome": melhor.nome,
                "bairro": melhor.bairro,
                "preco_diaria": melhor.preco_estimado_diaria,
                "preco_total": melhor.preco_estimado_total,
                "avaliacao": melhor.avaliacao,
                "criterio": ctx.preferencias.preferencia_hotel,
                "justificativa": f"Melhor equilíbrio entre localização ({melhor.bairro}), "
                f"avaliação ({melhor.avaliacao}) e diária de R$ {melhor.preco_estimado_diaria:,.2f}.",
            }

        return AgentResult(
            agent_name="agente_hotel",
            status="sucesso",
            data={
                "checkin": str(ctx.data_saida),
                "checkout": str(ctx.data_retorno),
                "quantidade_noites": ctx.quantidade_noites,
                "opcoes": [o.model_dump() for o in opcoes],
                "regioes_recomendadas": regioes,
                "melhor_opcao_sugerida": melhor_info,
                "limitacoes": [
                    "Tarifas variam com disponibilidade e antecedência da reserva.",
                    "Taxas locais (city tax) não incluídas nos valores estimados.",
                    "Políticas de cancelamento variam por hotel. Verifique antes de reservar.",
                ],
            },
            alertas=[
                "⚠️ Valores são estimativas. Confirme tarifas em plataformas de reserva antes de pagar."
            ],
            fontes=["Heurística local"]
            if not os.environ.get("GEMINI_API_KEY")
            else ["Google Gemini LLM"],
        )

    except Exception as e:
        return AgentResult(
            agent_name="agente_hotel",
            status="erro",
            data={},
            erros=[str(e)],
            alertas=["Não foi possível gerar sugestões de hotéis."],
        )
