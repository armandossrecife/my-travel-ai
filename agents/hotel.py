"""
agente_hotel.py — Agente especializado em busca e análise de hospedagens.

Implementa a lógica de geração e ranking de opções de hotéis seguindo os contratos
definidos em skill.md e plano.md. Suporta engine LLM (Google Gemini) e engine
de heurística local como fallback.
"""
from datetime import date, datetime
from typing import List, Optional
import os
import json

from models import TravelContext, AgentResult, HotelOption


# ──────────────────────────────────────────────────────────────
# Base de conhecimento para heurística local
# ──────────────────────────────────────────────────────────────

_CONHECIMENTO_HOTEL = {
    "lisboa": {
        "regioes_recomendadas": ["Baixa-Chiado", "Belém", "Alfama", "Príncipe Real", "Parque das Nações"],
        "hoteis": [
            {"nome": "Hotel Altis Belém", "bairro": "Belém", "categoria": "5 estrelas", "preco_diaria": 650, "avaliacao": "9.2/10", "destaques": ["Piscina", "Vista para o Tejo", "Spa", "Restaurante gourmet"]},
            {"nome": "Lisboa Carmo Hotel", "bairro": "Chiado", "categoria": "4 estrelas", "preco_diaria": 280, "avaliacao": "8.9/10", "destaques": ["Centro histórico", "Café da manhã", "Localização excelente"]},
            {"nome": "Hotel ZENIT Lisboa", "bairro": "Baixa", "categoria": "3 estrelas", "preco_diaria": 160, "avaliacao": "8.2/10", "destaques": ["Boa localização", "Custo-benefício", "Próximo ao metrô"]},
            {"nome": "Bairro Alto Hotel", "bairro": "Bairro Alto", "categoria": "5 estrelas", "preco_diaria": 580, "avaliacao": "9.4/10", "destaques": ["Boutique", "Vista panorâmica", "Restaurante com estrela Michelin"]},
        ],
    },
    "paris": {
        "regioes_recomendadas": ["Le Marais", "Saint-Germain-des-Prés", "Montmartre", "Châtelet", "Opera"],
        "hoteis": [
            {"nome": "Hotel des Arts Montmartre", "bairro": "Montmartre", "categoria": "3 estrelas", "preco_diaria": 220, "avaliacao": "8.5/10", "destaques": ["Vista para Sacré-Cœur", "Café da manhã", "Ambiente artístico"]},
            {"nome": "Hotel Le Marais Bastille", "bairro": "Le Marais", "categoria": "4 estrelas", "preco_diaria": 320, "avaliacao": "8.8/10", "destaques": ["Centro histórico", "Próximo ao metrô", "Wi-Fi gratuito"]},
            {"nome": "Ibis Paris Gare de Lyon", "bairro": "Lyon", "categoria": "2 estrelas", "preco_diaria": 140, "avaliacao": "7.8/10", "destaques": ["Econômico", "Bem localizado", "Fácil acesso ao transporte"]},
        ],
    },
    "nova york": {
        "regioes_recomendadas": ["Midtown Manhattan", "Times Square", "Upper East Side", "Brooklyn", "Chelsea"],
        "hoteis": [
            {"nome": "The Westin New York at Times Square", "bairro": "Times Square", "categoria": "4 estrelas", "preco_diaria": 480, "avaliacao": "8.6/10", "destaques": ["Centro de tudo", "Academia", "Vista para Times Square"]},
            {"nome": "Pod 51 Hotel", "bairro": "Midtown East", "categoria": "3 estrelas", "preco_diaria": 220, "avaliacao": "8.1/10", "destaques": ["Design moderno", "Custo-benefício", "Próximo ao metrô"]},
            {"nome": "The Standard, High Line", "bairro": "Chelsea", "categoria": "4 estrelas", "preco_diaria": 380, "avaliacao": "8.9/10", "destaques": ["Design icônico", "Vista do Rio Hudson", "Restaurante rooftop"]},
        ],
    },
    "miami": {
        "regioes_recomendadas": ["South Beach", "Brickell", "Downtown Miami", "Wynwood", "Coral Gables"],
        "hoteis": [
            {"nome": "Faena Hotel Miami Beach", "bairro": "South Beach", "categoria": "5 estrelas", "preco_diaria": 780, "avaliacao": "9.3/10", "destaques": ["Praia privativa", "Spa luxuoso", "Arte de vanguarda"]},
            {"nome": "Kimpton Angler's Hotel", "bairro": "South Beach", "categoria": "4 estrelas", "preco_diaria": 340, "avaliacao": "8.7/10", "destaques": ["Piscina", "Bar na cobertura", "A 100m da praia"]},
            {"nome": "Hotel Urbano", "bairro": "Brickell", "categoria": "3 estrelas", "preco_diaria": 180, "avaliacao": "8.0/10", "destaques": ["Piscina", "Café da manhã", "Custo-benefício"]},
        ],
    },
    "buenos aires": {
        "regioes_recomendadas": ["Palermo", "San Telmo", "Recoleta", "Puerto Madero", "Belgrano"],
        "hoteis": [
            {"nome": "Hotel Faena Buenos Aires", "bairro": "Puerto Madero", "categoria": "5 estrelas", "preco_diaria": 420, "avaliacao": "9.1/10", "destaques": ["Piscina aquecida", "Spa", "Vista para o Rio da Prata"]},
            {"nome": "Palermo Soho Suites", "bairro": "Palermo", "categoria": "4 estrelas", "preco_diaria": 180, "avaliacao": "8.8/10", "destaques": ["Terraço", "Café da manhã incluso", "Bairro badalado"]},
            {"nome": "Hostel Suites San Telmo", "bairro": "San Telmo", "categoria": "2 estrelas", "preco_diaria": 70, "avaliacao": "8.2/10", "destaques": ["Econômico", "Bairro histórico", "Ótima localização"]},
        ],
    },
    "roma": {
        "regioes_recomendadas": ["Centro Storico", "Trastevere", "Prati", "Termini", "Testaccio"],
        "hoteis": [
            {"nome": "Hotel de la Minerve", "bairro": "Centro Storico", "categoria": "5 estrelas", "preco_diaria": 620, "avaliacao": "9.0/10", "destaques": ["Terraço panorâmico", "A 200m do Panthéon", "Restaurante excelente"]},
            {"nome": "Hotel Artemide", "bairro": "Termini", "categoria": "4 estrelas", "preco_diaria": 220, "avaliacao": "8.7/10", "destaques": ["Café da manhã farto", "Spa e piscina", "Próximo à estação central"]},
            {"nome": "Trastevere Charming House", "bairro": "Trastevere", "categoria": "3 estrelas", "preco_diaria": 150, "avaliacao": "8.4/10", "destaques": ["Bairro romântico", "Custo-benefício", "Restaurantes na porta"]},
        ],
    },
    "default": {
        "regioes_recomendadas": ["Centro histórico", "Área turística principal", "Próximo ao transporte público"],
        "hoteis": [
            {"nome": "Grand Hotel Centro", "bairro": "Centro", "categoria": "4 estrelas", "preco_diaria": 350, "avaliacao": "8.5/10", "destaques": ["Centralizado", "Café da manhã", "Próximo às atrações"]},
            {"nome": "City Comfort Hotel", "bairro": "Área Central", "categoria": "3 estrelas", "preco_diaria": 200, "avaliacao": "8.0/10", "destaques": ["Custo-benefício", "Boa localização", "Wi-Fi"]},
            {"nome": "Budget Inn Express", "bairro": "Zona Turística", "categoria": "2 estrelas", "preco_diaria": 120, "avaliacao": "7.5/10", "destaques": ["Econômico", "Café da manhã simples"]},
        ],
    },
}


def _calcular_score_hotel(hotel: dict, preco_min: float, preco_max: float) -> float:
    """Calcula score ponderado de um hotel conforme skill.md."""
    # Nota localização: mapeada pela categoria do hotel
    categorias = {"5 estrelas": 1.0, "4 estrelas": 0.8, "3 estrelas": 0.6, "2 estrelas": 0.4, "1 estrela": 0.2}
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
        0.35 * nota_localizacao +
        0.25 * nota_avaliacao +
        0.25 * nota_preco +
        0.15 * nota_comodidades
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

        opcoes.append(HotelOption(
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
        ))

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
        response = client.models.generate_content(model="gemini-3.5-flash", contents=prompt)
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


def run(ctx: TravelContext) -> AgentResult:
    """Ponto de entrada do agente_hotel."""
    try:
        use_llm = bool(os.environ.get("GEMINI_API_KEY", ""))
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
            alertas=["⚠️ Valores são estimativas. Confirme tarifas em plataformas de reserva antes de pagar."],
            fontes=["Heurística local"] if not os.environ.get("GEMINI_API_KEY") else ["Google Gemini LLM"],
        )

    except Exception as e:
        return AgentResult(
            agent_name="agente_hotel",
            status="erro",
            data={},
            erros=[str(e)],
            alertas=["Não foi possível gerar sugestões de hotéis."],
        )
