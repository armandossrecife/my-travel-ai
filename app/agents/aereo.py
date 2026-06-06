"""
agente_aereo.py — Agente especializado em busca e análise de passagens aéreas.

Implementa a lógica de geração e ranking de opções de voos seguindo os contratos
definidos em skill.md e plano.md. Suporta engine LLM (Google Gemini) e engine
de heurística local como fallback.
"""

import json
import os
from typing import List

from app.agents.logger import log_info
from app.models import AgentResult, FlightOption, TravelContext

from app.agents.base_local import _CONHECIMENTO_AEREO, _HUBS_POR_ORIGEM
from app.agents.config import MODELO_LMM

def _calcular_score_voo(voo: dict) -> float:
    """Calcula score ponderado de um voo conforme regras do skill.md."""
    # Normaliza escalas (0 = melhor, max 3)
    max_escalas = 3
    nota_escalas = 1 - (voo["escalas"] / max_escalas)

    # Normaliza preço (invertido: menor = melhor)
    preco_min = voo.get("preco_ref_min", voo["preco_base"] * 0.85)
    preco_max = voo.get("preco_ref_max", voo["preco_base"] * 1.15)
    span = max(preco_max - preco_min, 1)
    nota_preco = max(0, 1 - ((voo["preco_base"] - preco_min) / span))

    # Normaliza duração (horas)
    try:
        h, m = map(int, voo["duracao"].replace("h", ":").replace("min", "").split(":"))
    except Exception:
        h, m = 12, 0
    duracao_horas = h + m / 60
    nota_duracao = max(0, 1 - (duracao_horas / 24))

    nota_confianca = 0.8  # fonte heurística = 80% confiança

    score = (
        0.40 * nota_preco
        + 0.25 * nota_duracao
        + 0.20 * nota_escalas
        + 0.15 * nota_confianca
    )
    return round(score, 4)


def _gerar_opcoes_heuristica(ctx: TravelContext) -> List[FlightOption]:
    """Gera opções de passagens aéreas usando heurística local."""
    destino_key = ctx.cidade_destino.lower().strip()
    dados_rotas = _CONHECIMENTO_AEREO.get(destino_key, _CONHECIMENTO_AEREO["default"])

    origem = ctx.cidade_origem or "São Paulo (hub GRU)"
    sigla_hub = _HUBS_POR_ORIGEM.get(
        ctx.cidade_origem.lower().strip() if ctx.cidade_origem else "", "GRU"
    )

    # Fator de demanda por temporada
    mes_saida = ctx.data_saida.month
    fator_sazonalidade = (
        1.25 if mes_saida in [1, 7, 12] else (1.10 if mes_saida in [6, 8, 11] else 1.0)
    )

    opcoes: List[FlightOption] = []
    precos = [d["preco_base"] * fator_sazonalidade for d in dados_rotas]
    preco_min = min(precos)
    preco_max = max(precos)

    for i, dado in enumerate(dados_rotas):
        preco_final = round(dado["preco_base"] * fator_sazonalidade, 2)
        dado["preco_ref_min"] = preco_min
        dado["preco_ref_max"] = preco_max
        score = _calcular_score_voo(dado)

        opcoes.append(
            FlightOption(
                companhia=dado["companhia"],
                origem=f"{origem} ({sigla_hub})",
                destino=ctx.cidade_destino,
                data_ida=ctx.data_saida,
                data_volta=ctx.data_retorno,
                preco_estimado=preco_final,
                moeda="BRL",
                duracao_estimada=dado["duracao"],
                escalas=dado["escalas"],
                link_consulta=None,
                observacoes="Estimativa baseada em heurística. Confirme valores em sites oficiais.",
                score=score,
            )
        )

    # Ordena por score descrescente
    opcoes.sort(key=lambda x: x.score, reverse=True)
    return opcoes


def _gerar_opcoes_llm(ctx: TravelContext) -> List[FlightOption]:
    """Gera opções de passagens aéreas usando LLM (Google Gemini)."""
    try:
        from google import genai

        api_key = os.environ.get("GEMINI_API_KEY", "")
        if not api_key:
            raise ValueError("GEMINI_API_KEY não configurada.")

        client = genai.Client(api_key=api_key)

        prompt = f"""Você é o agente_aereo, especialista em passagens aéreas.

Dados da viagem:
- Cidade origem: {ctx.cidade_origem or "Não informada (assumir São Paulo/GRU)"}
- Cidade destino: {ctx.cidade_destino}
- Data de saída: {ctx.data_saida}
- Data de retorno: {ctx.data_retorno}
- Quantidade de viajantes: {ctx.preferencias.quantidade_viajantes}
- Preferência: {ctx.preferencias.preferencia_voo}

Gere uma lista JSON de exatamente 3 opções de passagens aéreas realistas.
Responda SOMENTE com um JSON array, sem markdown, no formato:
[
  {{
    "companhia": "Nome da companhia",
    "origem": "Cidade - Sigla aeroporto",
    "destino": "Cidade destino",
    "data_ida": "YYYY-MM-DD",
    "data_volta": "YYYY-MM-DD",
    "preco_estimado": 0000.00,
    "moeda": "BRL",
    "duracao_estimada": "XhYY",
    "escalas": 0,
    "link_consulta": null,
    "observacoes": "Estimativa. Confirme em sites oficiais.",
    "score": 0.0
  }}
]

REGRAS OBRIGATÓRIAS:
- Use companhias aéreas reais que operem essa rota.
- Preços em BRL realistas para a temporada.
- NÃO invente links.
- NÃO afirme disponibilidade garantida.
"""
        response = client.models.generate_content(
            model=MODELO_LMM,
            contents=prompt,
        )
        raw = response.text.strip()
        # Remove possíveis blocos markdown
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        data = json.loads(raw)
        opcoes = []
        for item in data:
            item.setdefault("score", 0.0)
            opcoes.append(FlightOption(**item))
        return opcoes

    except Exception as e:
        print(f"[agente_aereo] LLM falhou: {e}. Usando heurística local.")
        return _gerar_opcoes_heuristica(ctx)


def run(ctx: TravelContext, request_id: str = None) -> AgentResult:
    """Ponto de entrada do agente_aereo."""
    try:
        log_info(
            request_id, "aereo", f"Iniciando busca de voos para {ctx.cidade_destino}"
        )
        use_llm = bool(os.environ.get("GEMINI_API_KEY", ""))
        if use_llm:
            log_info(
                request_id, "aereo", "Usando engine LLM (Gemini) para busca de voos"
            )
        else:
            log_info(
                request_id, "aereo", "Usando engine heurística local para busca de voos"
            )

        opcoes = _gerar_opcoes_llm(ctx) if use_llm else _gerar_opcoes_heuristica(ctx)

        melhor = opcoes[0] if opcoes else None
        melhor_info = None
        if melhor:
            melhor_info = {
                "companhia": melhor.companhia,
                "preco_estimado": melhor.preco_estimado,
                "duracao_estimada": melhor.duracao_estimada,
                "escalas": melhor.escalas,
                "criterio": ctx.preferencias.preferencia_voo,
                "justificativa": f"Melhor equilíbrio entre preço (R$ {melhor.preco_estimado:,.2f}), "
                f"duração ({melhor.duracao_estimada}) e {melhor.escalas} escala(s).",
            }

        return AgentResult(
            agent_name="agente_aereo",
            status="sucesso",
            data={
                "opcoes": [o.model_dump() for o in opcoes],
                "melhor_opcao_sugerida": melhor_info,
                "limitacoes": [
                    "Preços são estimativas e variam rapidamente.",
                    "Confirme disponibilidade e valores em sites oficiais ou agências.",
                    "Tarifas de bagagem e taxas não estão incluídas.",
                ]
                + (
                    [
                        "Cidade de origem não informada. Assumindo partida de São Paulo (GRU)."
                    ]
                    if not ctx.cidade_origem
                    else []
                ),
            },
            alertas=[
                "⚠️ Valores são estimativas geradas por IA. Confirme antes de comprar.",
            ],
            fontes=["Heurística local baseada em dados históricos de rotas"]
            if not os.environ.get("GEMINI_API_KEY")
            else ["Google Gemini LLM"],
        )

    except Exception as e:
        return AgentResult(
            agent_name="agente_aereo",
            status="erro",
            data={},
            erros=[str(e)],
            alertas=["Não foi possível gerar sugestões de passagens aéreas."],
        )
