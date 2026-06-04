"""
agente_turismo.py — Agente especializado em criação de roteiros turísticos.

Implementa a lógica de geração de itinerários diários baseados na cidade destino,
período de viagem e interesses do usuário. Suporta engine LLM (Google Gemini) e
engine de heurística local como fallback.
"""

import json
import os
from datetime import date, datetime, timedelta
from typing import Dict, List

from agents.logger import log_error, log_info, log_success, log_warning
from models import AgentResult, DailyItinerary, TouristAttraction, TravelContext

# ──────────────────────────────────────────────────────────────
# Base de conhecimento turístico
# ──────────────────────────────────────────────────────────────

_PONTOS_TURISTICOS = {
    "lisboa": [
        {
            "nome": "Torre de Belém",
            "categoria": "histórico",
            "bairro": "Belém",
            "tempo": "1h30",
            "prioridade": 1,
        },
        {
            "nome": "Mosteiro dos Jerónimos",
            "categoria": "histórico",
            "bairro": "Belém",
            "tempo": "2h00",
            "prioridade": 2,
        },
        {
            "nome": "Museu Nacional do Azulejo",
            "categoria": "cultural",
            "bairro": "Santa Apolónia",
            "tempo": "2h00",
            "prioridade": 3,
        },
        {
            "nome": "Alfama e Castelo de São Jorge",
            "categoria": "histórico",
            "bairro": "Alfama",
            "tempo": "3h00",
            "prioridade": 4,
        },
        {
            "nome": "Praça do Comércio",
            "categoria": "cultural",
            "bairro": "Baixa",
            "tempo": "1h00",
            "prioridade": 5,
        },
        {
            "nome": "Parque das Nações",
            "categoria": "entretenimento",
            "bairro": "Parque das Nações",
            "tempo": "3h00",
            "prioridade": 6,
        },
        {
            "nome": "Bairro Alto & Chiado",
            "categoria": "gastronômico",
            "bairro": "Chiado",
            "tempo": "2h00",
            "prioridade": 7,
        },
        {
            "nome": "LX Factory",
            "categoria": "cultural",
            "bairro": "Alcântara",
            "tempo": "2h00",
            "prioridade": 8,
        },
        {
            "nome": "Palácio Nacional de Sintra",
            "categoria": "histórico",
            "bairro": "Sintra (excursão)",
            "tempo": "4h00",
            "prioridade": 9,
        },
        {
            "nome": "Cabo da Roca",
            "categoria": "natureza",
            "bairro": "Sintra (excursão)",
            "tempo": "1h30",
            "prioridade": 10,
        },
    ],
    "paris": [
        {
            "nome": "Torre Eiffel",
            "categoria": "histórico",
            "bairro": "Champ-de-Mars",
            "tempo": "2h00",
            "prioridade": 1,
        },
        {
            "nome": "Museu do Louvre",
            "categoria": "cultural",
            "bairro": "1er arrondissement",
            "tempo": "4h00",
            "prioridade": 2,
        },
        {
            "nome": "Notre-Dame de Paris",
            "categoria": "religioso",
            "bairro": "Île de la Cité",
            "tempo": "1h30",
            "prioridade": 3,
        },
        {
            "nome": "Musée d'Orsay",
            "categoria": "cultural",
            "bairro": "7e arrondissement",
            "tempo": "3h00",
            "prioridade": 4,
        },
        {
            "nome": "Arc de Triomphe & Champs-Élysées",
            "categoria": "histórico",
            "bairro": "8e arrondissement",
            "tempo": "2h00",
            "prioridade": 5,
        },
        {
            "nome": "Montmartre & Sacré-Cœur",
            "categoria": "cultural",
            "bairro": "Montmartre",
            "tempo": "2h30",
            "prioridade": 6,
        },
        {
            "nome": "Palácio de Versalhes",
            "categoria": "histórico",
            "bairro": "Versalhes (excursão)",
            "tempo": "5h00",
            "prioridade": 7,
        },
        {
            "nome": "Le Marais",
            "categoria": "gastronômico",
            "bairro": "Le Marais",
            "tempo": "2h00",
            "prioridade": 8,
        },
    ],
    "nova york": [
        {
            "nome": "Estátua da Liberdade & Ellis Island",
            "categoria": "histórico",
            "bairro": "Liberty Island",
            "tempo": "4h00",
            "prioridade": 1,
        },
        {
            "nome": "Central Park",
            "categoria": "natureza",
            "bairro": "Midtown",
            "tempo": "2h00",
            "prioridade": 2,
        },
        {
            "nome": "Times Square",
            "categoria": "entretenimento",
            "bairro": "Midtown",
            "tempo": "1h00",
            "prioridade": 3,
        },
        {
            "nome": "Metropolitan Museum of Art",
            "categoria": "cultural",
            "bairro": "Upper East Side",
            "tempo": "3h00",
            "prioridade": 4,
        },
        {
            "nome": "Empire State Building",
            "categoria": "histórico",
            "bairro": "Midtown",
            "tempo": "2h00",
            "prioridade": 5,
        },
        {
            "nome": "Brooklyn Bridge & DUMBO",
            "categoria": "histórico",
            "bairro": "Brooklyn",
            "tempo": "2h00",
            "prioridade": 6,
        },
        {
            "nome": "High Line",
            "categoria": "cultural",
            "bairro": "Chelsea",
            "tempo": "1h30",
            "prioridade": 7,
        },
        {
            "nome": "9/11 Memorial & Museum",
            "categoria": "histórico",
            "bairro": "Financial District",
            "tempo": "2h30",
            "prioridade": 8,
        },
    ],
    "miami": [
        {
            "nome": "South Beach & Ocean Drive",
            "categoria": "natureza",
            "bairro": "South Beach",
            "tempo": "3h00",
            "prioridade": 1,
        },
        {
            "nome": "Art Deco Historic District",
            "categoria": "histórico",
            "bairro": "South Beach",
            "tempo": "2h00",
            "prioridade": 2,
        },
        {
            "nome": "Wynwood Walls",
            "categoria": "cultural",
            "bairro": "Wynwood",
            "tempo": "2h00",
            "prioridade": 3,
        },
        {
            "nome": "Vizcaya Museum & Gardens",
            "categoria": "histórico",
            "bairro": "Coconut Grove",
            "tempo": "2h30",
            "prioridade": 4,
        },
        {
            "nome": "Little Havana",
            "categoria": "gastronômico",
            "bairro": "Little Havana",
            "tempo": "2h00",
            "prioridade": 5,
        },
        {
            "nome": "Everglades National Park",
            "categoria": "natureza",
            "bairro": "Everglades (excursão)",
            "tempo": "6h00",
            "prioridade": 6,
        },
    ],
    "buenos aires": [
        {
            "nome": "La Boca & Caminito",
            "categoria": "cultural",
            "bairro": "La Boca",
            "tempo": "2h00",
            "prioridade": 1,
        },
        {
            "nome": "San Telmo & Feira Antigos",
            "categoria": "cultural",
            "bairro": "San Telmo",
            "tempo": "2h30",
            "prioridade": 2,
        },
        {
            "nome": "Palácio do Congresso",
            "categoria": "histórico",
            "bairro": "Balvanera",
            "tempo": "1h30",
            "prioridade": 3,
        },
        {
            "nome": "Recoleta Cemetery",
            "categoria": "histórico",
            "bairro": "Recoleta",
            "tempo": "1h30",
            "prioridade": 4,
        },
        {
            "nome": "MALBA - Museu de Arte Latino-Americana",
            "categoria": "cultural",
            "bairro": "Palermo",
            "tempo": "2h00",
            "prioridade": 5,
        },
        {
            "nome": "Puerto Madero",
            "categoria": "gastronômico",
            "bairro": "Puerto Madero",
            "tempo": "2h00",
            "prioridade": 6,
        },
        {
            "nome": "Tango Show em San Telmo",
            "categoria": "entretenimento",
            "bairro": "San Telmo",
            "tempo": "2h30",
            "prioridade": 7,
        },
    ],
    "roma": [
        {
            "nome": "Coliseu e Fórum Romano",
            "categoria": "histórico",
            "bairro": "Centro Storico",
            "tempo": "3h00",
            "prioridade": 1,
        },
        {
            "nome": "Vaticano e Capela Sistina",
            "categoria": "religioso",
            "bairro": "Prati",
            "tempo": "4h00",
            "prioridade": 2,
        },
        {
            "nome": "Fontana di Trevi",
            "categoria": "histórico",
            "bairro": "Trevi",
            "tempo": "1h00",
            "prioridade": 3,
        },
        {
            "nome": "Panthéon",
            "categoria": "histórico",
            "bairro": "Pigna",
            "tempo": "1h30",
            "prioridade": 4,
        },
        {
            "nome": "Piazza Navona",
            "categoria": "cultural",
            "bairro": "Parione",
            "tempo": "1h00",
            "prioridade": 5,
        },
        {
            "nome": "Trastevere",
            "categoria": "gastronômico",
            "bairro": "Trastevere",
            "tempo": "2h30",
            "prioridade": 6,
        },
        {
            "nome": "Galeria Borghese",
            "categoria": "cultural",
            "bairro": "Villa Borghese",
            "tempo": "2h00",
            "prioridade": 7,
        },
        {
            "nome": "Castelo Sant'Angelo",
            "categoria": "histórico",
            "bairro": "Borgo",
            "tempo": "2h00",
            "prioridade": 8,
        },
    ],
    "default": [
        {
            "nome": "Centro Histórico da Cidade",
            "categoria": "histórico",
            "bairro": "Centro",
            "tempo": "2h00",
            "prioridade": 1,
        },
        {
            "nome": "Museu Municipal Principal",
            "categoria": "cultural",
            "bairro": "Centro",
            "tempo": "2h00",
            "prioridade": 2,
        },
        {
            "nome": "Mercado e Gastronomia Local",
            "categoria": "gastronômico",
            "bairro": "Centro",
            "tempo": "1h30",
            "prioridade": 3,
        },
        {
            "nome": "Parque ou Área Verde Principal",
            "categoria": "natureza",
            "bairro": "Área central",
            "tempo": "1h30",
            "prioridade": 4,
        },
        {
            "nome": "Mirante ou Vista Panorâmica",
            "categoria": "cultural",
            "bairro": "Ponto alto",
            "tempo": "1h00",
            "prioridade": 5,
        },
        {
            "nome": "Bairro Artístico e Cultural",
            "categoria": "cultural",
            "bairro": "Bairro Artístico",
            "tempo": "2h00",
            "prioridade": 6,
        },
    ],
}

_DICAS_GERAIS = {
    "lisboa": [
        "🚊 Use o Passe Lisboa para metrô, eléctrico e ônibus. Vale muito a pena.",
        "🍽️ Almoce entre 12h-14h nos restaurantes locais para evitar filas e pagar menos.",
        "🎭 Reserve ingressos do Mosteiro dos Jerónimos com antecedência — forma filas enormes.",
        "☀️ Julho é muito quente: leve protetor solar e hidrate-se bem.",
        "🏄 Reserve um dia para Sintra — a excursão vale cada minuto!",
    ],
    "paris": [
        "🎫 Compre o Paris Museum Pass para acesso a mais de 50 museus sem filas.",
        "🚇 O metrô parisiense é eficiente e econômico para se locomover.",
        "🥐 Pequenos bistrôs cobram menos que restaurantes turísticos. Explore!",
        "📸 A Torre Eiffel é mais bonita ao pôr do sol e iluminada à noite.",
        "🏰 Versalhes recebe milhões de turistas. Reserve com meses de antecedência.",
    ],
    "nova york": [
        "🗽 Compre ingressos para a Estátua da Liberdade com semanas de antecedência.",
        "🚇 O subway é o melhor transporte. Compre um MetroCard ilimitado.",
        "🎭 Busque bilhetes TKTS em Times Square para shows na Broadway com desconto.",
        "🌆 O Top of the Rock (30 Rock) tem vista melhor que o Empire State e menos filas.",
        "🍕 A pizza nova-iorquina de fatia é uma experiência cultural obrigatória.",
    ],
    "default": [
        "📅 Pesquise eventos locais que possam ocorrer no período da sua viagem.",
        "💊 Verifique se há necessidade de vacinas ou documentos especiais para o destino.",
        "💱 Consulte as melhores opções de câmbio antes de viajar.",
        "📱 Baixe mapas offline do destino para usar sem internet.",
        "🌤️ Verifique a previsão do tempo para os dias da viagem.",
    ],
}


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
            # model="gemini-3.5-flash",
            model="gemini-3.1-flash-lite",
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
