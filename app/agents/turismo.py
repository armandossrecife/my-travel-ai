"""
agente_turismo.py — Agente especializado em criação de roteiros turísticos.

Implementa a lógica de geração de itinerários diários baseados na cidade destino,
período de viagem e interesses do usuário. Suporta engine LLM (Google Gemini) e
engine de heurística local como fallback.
"""

import json
import os
from datetime import date, timedelta
from typing import List

from app.agents.logger import log_info
from app.models import AgentResult, DailyItinerary, TouristAttraction, TravelContext

from app.agents.base_local import _PONTOS_TURISTICOS, _DICAS_GERAIS

from app.agents.config import MODELO_LMM

def _gerar_roteiro_heuristica(ctx: TravelContext) -> dict:
    """Gera roteiro turístico usando heurística local."""
    destino_key = ctx.cidade_destino.lower().strip()
    pontos = _PONTOS_TURISTICOS.get(destino_key, _PONTOS_TURISTICOS["default"])
    dicas = _DICAS_GERAIS.get(destino_key, _DICAS_GERAIS["default"])

    # Cria os objetos de atração
    atracoes = []
    for p in pontos:
        atracoes.append(
            TouristAttraction(
                nome=p["nome"],
                categoria=p["categoria"],
                bairro=p["bairro"],
                tempo_estimado_visita=p["tempo"],
                prioridade=p["prioridade"],
                observacoes=[
                    "Confirme horários e valores de ingressos no site oficial."
                ],
            )
        )

    # Constrói roteiro diário
    roteiro: List[DailyItinerary] = []
    data_atual = ctx.data_saida
    idx_atracao = 0
    total_dias = ctx.quantidade_dias

    for dia_num in range(1, total_dias + 1):
        is_chegada = dia_num == 1
        is_retorno = dia_num == total_dias

        if is_chegada:
            manha = [
                "Chegada ao aeroporto",
                "Deslocamento e check-in no hotel",
                "Descanso após a viagem",
            ]
            tarde = ["Passeio leve pelo bairro do hotel", "Conhecer os arredores"]
            noite = [
                "Jantar em restaurante próximo ao hotel",
                "Adaptação ao fuso horário (se houver)",
            ]
            tema = "Chegada e adaptação"
            obs = [
                "Evite agenda intensa no dia de chegada.",
                "Hidrate-se bem após o voo.",
            ]

        elif is_retorno:
            manha = ["Café da manhã no hotel", "Últimas compras e souvenirs"]
            tarde = ["Check-out do hotel", "Deslocamento ao aeroporto"]
            noite = ["Embarque de retorno"]
            tema = "Retorno para casa"
            obs = [
                "Chegue ao aeroporto com pelo menos 3h de antecedência para voos internacionais."
            ]

        else:
            # Distribui 2-3 atrações por dia dependendo do ritmo
            ritmo = ctx.preferencias.ritmo_roteiro
            atracoes_por_dia = (
                3 if ritmo == "intenso" else (2 if ritmo == "moderado" else 1)
            )

            atr_dia = []
            for _ in range(atracoes_por_dia):
                if idx_atracao < len(atracoes):
                    atr_dia.append(atracoes[idx_atracao])
                    idx_atracao += 1

            if len(atr_dia) >= 3:
                manha = [
                    f"Visita: {atr_dia[0].nome} ({atr_dia[0].bairro}) — ~{atr_dia[0].tempo_estimado_visita}"
                ]
                tarde = [
                    f"Visita: {atr_dia[1].nome} ({atr_dia[1].bairro}) — ~{atr_dia[1].tempo_estimado_visita}",
                    f"Explorar: {atr_dia[2].nome}"
                    if len(atr_dia) > 2
                    else "Tempo livre",
                ]
                noite = ["Jantar local", "Explorar a vida noturna do bairro"]
                tema = f"Dia {dia_num - 1}: {' e '.join(a.nome for a in atr_dia[:2])}"
            elif len(atr_dia) == 2:
                manha = [
                    f"Visita: {atr_dia[0].nome} ({atr_dia[0].bairro}) — ~{atr_dia[0].tempo_estimado_visita}"
                ]
                tarde = [
                    f"Visita: {atr_dia[1].nome} ({atr_dia[1].bairro}) — ~{atr_dia[1].tempo_estimado_visita}",
                    "Café/lanche local",
                ]
                noite = ["Jantar no bairro", "Passeio noturno"]
                tema = f"Dia {dia_num - 1}: {atr_dia[0].nome}"
            elif len(atr_dia) == 1:
                manha = [
                    f"Visita: {atr_dia[0].nome} ({atr_dia[0].bairro}) — ~{atr_dia[0].tempo_estimado_visita}"
                ]
                tarde = ["Tempo livre para explorar", "Compras e gastronomia local"]
                noite = ["Jantar em restaurante escolhido", "Tempo livre"]
                tema = f"Dia {dia_num - 1}: {atr_dia[0].nome}"
            else:
                manha = ["Dia livre", "Explore o bairro ao seu ritmo"]
                tarde = ["Gastronomia local", "Descanso ou compras"]
                noite = ["Jantar especial", "Passeio noturno"]
                tema = f"Dia {dia_num - 1}: Exploração livre"

            obs = [
                "Confirme horários de funcionamento antes de visitar.",
                "Atrações próximas foram agrupadas para economizar deslocamento.",
            ]

        roteiro.append(
            DailyItinerary(
                dia=dia_num,
                data=data_atual,
                tema=tema,
                manha=manha,
                tarde=tarde,
                noite=noite,
                observacoes=obs,
            )
        )
        data_atual = data_atual + timedelta(days=1)

    return {
        "pontos_turisticos_prioritarios": atracoes,
        "roteiro_por_dia": roteiro,
        "dicas": dicas,
        "alertas": [
            "⚠️ Confirme horários de funcionamento e preços de ingressos nos sites oficiais.",
            "⚠️ Para atrações muito populares, reserve ingressos com antecedência.",
        ],
    }


def _gerar_roteiro_llm(ctx: TravelContext) -> dict:
    """Gera roteiro turístico usando LLM (Google Gemini)."""
    try:
        from google import genai

        api_key = os.environ.get("GEMINI_API_KEY", "")
        if not api_key:
            raise ValueError("GEMINI_API_KEY não configurada.")

        client = genai.Client(api_key=api_key)

        prompt = f"""Você é o agente_turismo, especialista em roteiros turísticos.

Dados da viagem:
- Cidade destino: {ctx.cidade_destino}
- Data de saída: {ctx.data_saida}
- Data de retorno: {ctx.data_retorno}
- Quantidade de dias: {ctx.quantidade_dias}
- Interesses: {", ".join(ctx.preferencias.interesses) if ctx.preferencias.interesses else "geral"}
- Ritmo: {ctx.preferencias.ritmo_roteiro}

Gere um JSON com as chaves:
- "pontos_turisticos_prioritarios": lista de atrações
- "roteiro_por_dia": itinerário por dia
- "dicas": lista de dicas práticas
- "alertas": lista de avisos

Responda SOMENTE com JSON puro, sem markdown, no formato:
{{
  "pontos_turisticos_prioritarios": [
    {{
      "nome": "...", "categoria": "...", "bairro": "...",
      "tempo_estimado_visita": "Xh", "prioridade": 1,
      "observacoes": ["Confirme horários."], "score": 0.0
    }}
  ],
  "roteiro_por_dia": [
    {{
      "dia": 1, "data": "YYYY-MM-DD", "tema": "...",
      "manha": ["..."], "tarde": ["..."], "noite": ["..."],
      "observacoes": ["..."]
    }}
  ],
  "dicas": ["dica 1", "dica 2"],
  "alertas": ["alerta 1"]
}}

REGRAS: Atrações reais, roteiro realista, {ctx.quantidade_dias} dias exatos.
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

        atracoes = []
        for item in data.get("pontos_turisticos_prioritarios", []):
            item.setdefault("score", 0.0)
            atracoes.append(TouristAttraction(**item))

        roteiro = []
        for item in data.get("roteiro_por_dia", []):
            item["data"] = date.fromisoformat(str(item["data"]))
            roteiro.append(DailyItinerary(**item))

        return {
            "pontos_turisticos_prioritarios": atracoes,
            "roteiro_por_dia": roteiro,
            "dicas": data.get("dicas", []),
            "alertas": data.get("alertas", []),
        }

    except Exception as e:
        print(f"[agente_turismo] LLM falhou: {e}. Usando heurística local.")
        return _gerar_roteiro_heuristica(ctx)


def run(ctx: TravelContext, request_id: str = None) -> AgentResult:
    """Ponto de entrada do agente_turismo."""
    try:
        log_info(
            request_id,
            "turismo",
            f"Iniciando criação do roteiro turístico para {ctx.cidade_destino}",
        )
        use_llm = bool(os.environ.get("GEMINI_API_KEY", ""))
        if use_llm:
            log_info(
                request_id,
                "turismo",
                "Usando engine LLM (Gemini) para roteiro turístico",
            )
        else:
            log_info(
                request_id,
                "turismo",
                "Usando engine heurística local para roteiro turístico",
            )

        resultado = (
            _gerar_roteiro_llm(ctx) if use_llm else _gerar_roteiro_heuristica(ctx)
        )

        # Serializa os objetos Pydantic
        pontos = resultado["pontos_turisticos_prioritarios"]
        roteiro = resultado["roteiro_por_dia"]

        pontos_serial = [p.model_dump() for p in pontos]
        roteiro_serial = []
        for dia in roteiro:
            d = dia.model_dump()
            d["data"] = str(d["data"])
            roteiro_serial.append(d)

        return AgentResult(
            agent_name="agente_turismo",
            status="sucesso",
            data={
                "periodo": {
                    "data_saida": str(ctx.data_saida),
                    "data_retorno": str(ctx.data_retorno),
                    "quantidade_dias": ctx.quantidade_dias,
                },
                "pontos_turisticos_prioritarios": pontos_serial,
                "roteiro_por_dia": roteiro_serial,
                "dicas": resultado.get("dicas", []),
                "alertas": resultado.get("alertas", []),
            },
            alertas=[
                "⚠️ Confirme horários de funcionamento antes de visitar.",
                "⚠️ Compre ingressos antecipados para as atrações mais populares.",
            ],
            fontes=["Heurística local"]
            if not os.environ.get("GEMINI_API_KEY")
            else ["Google Gemini LLM"],
        )

    except Exception as e:
        return AgentResult(
            agent_name="agente_turismo",
            status="erro",
            data={},
            erros=[str(e)],
            alertas=["Não foi possível gerar o roteiro turístico."],
        )
