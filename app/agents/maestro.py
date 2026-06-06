"""
maestro.py — Agente orquestrador principal do sistema de planejamento de viagens.

Responsável por: validar entradas, normalizar dados, acionar os agentes especialistas
em paralelo, tratar falhas parciais e consolidar a resposta final conforme definido
em skill.md e plano.md.
"""

import concurrent.futures
import uuid
from typing import Optional

from app.agents import aereo, hotel, turismo
from app.agents.logger import (
    event_logger,
    log_error,
    log_info,
    log_success,
    log_warning,
)
from app.models import (
    AgentResult,
    CostEstimation,
    ExecutionMetadata,
    IntegratedPlan,
    TravelContext,
    TravelPlan,
    TravelPreferences,
    TravelRequest,
)

# ──────────────────────────────────────────────────────────────
# Validação e normalização
# ──────────────────────────────────────────────────────────────


def _validar_request(req: TravelRequest) -> list[str]:
    """Retorna lista de erros de validação."""
    erros = []

    if not req.cidade_destino or not req.cidade_destino.strip():
        erros.append("Campo obrigatório ausente: 'cidade_destino'.")

    if not req.data_saida:
        erros.append("Campo obrigatório ausente: 'data_saida'.")

    if not req.data_retorno:
        erros.append("Campo obrigatório ausente: 'data_retorno'.")

    if req.data_saida and req.data_retorno:
        if req.data_retorno <= req.data_saida:
            erros.append("'data_retorno' deve ser posterior à 'data_saida'.")

        delta = (req.data_retorno - req.data_saida).days
        if delta < 1:
            erros.append("A viagem deve ter pelo menos 1 noite de hospedagem.")

    return erros


def _construir_contexto(req: TravelRequest, request_id: str) -> TravelContext:
    """Transforma TravelRequest em TravelContext enriquecido."""
    quantidade_dias = (req.data_retorno - req.data_saida).days + 1
    quantidade_noites = (req.data_retorno - req.data_saida).days

    return TravelContext(
        request_id=request_id,
        cidade_destino=req.cidade_destino.strip().title(),
        data_saida=req.data_saida,
        data_retorno=req.data_retorno,
        cidade_origem=req.cidade_origem.strip().title() if req.cidade_origem else None,
        quantidade_dias=quantidade_dias,
        quantidade_noites=quantidade_noites,
        preferencias=req.preferencias,
        execucao=ExecutionMetadata(),
    )


# ──────────────────────────────────────────────────────────────
# Consolidação da resposta
# ──────────────────────────────────────────────────────────────


def _calcular_estimativa_custos(
    resultado_aereo: AgentResult,
    resultado_hotel: AgentResult,
) -> CostEstimation:
    """Estima custos totais a partir dos resultados dos agentes."""
    passagens = None
    hospedagem = None

    try:
        if resultado_aereo.status in ("sucesso", "parcial"):
            opcoes = resultado_aereo.data.get("opcoes", [])
            if opcoes:
                melhor = max(opcoes, key=lambda x: x.get("score", 0))
                passagens = melhor.get("preco_estimado")
    except Exception:
        pass

    try:
        if resultado_hotel.status in ("sucesso", "parcial"):
            opcoes = resultado_hotel.data.get("opcoes", [])
            if opcoes:
                melhor = max(opcoes, key=lambda x: x.get("score", 0))
                hospedagem = melhor.get("preco_estimado_total")
    except Exception:
        pass

    total = None
    if passagens is not None and hospedagem is not None:
        # Adiciona 20% estimado para passeios, alimentação e transporte local
        passeios = round((passagens + hospedagem) * 0.20, 2)
        total = round(passagens + hospedagem + passeios, 2)
    else:
        passeios = None

    return CostEstimation(
        passagens=passagens,
        hospedagem=hospedagem,
        passeios=passeios,
        total_estimado=total,
        moeda="BRL",
    )


def _gerar_recomendacao_geral(ctx: TravelContext, resultados: dict) -> str:
    """Gera um texto de recomendação consolidado."""
    status_geral = all(r.status == "sucesso" for r in resultados.values())
    status_txt = "com sucesso" if status_geral else "parcialmente"

    passagens = resultados["aereo"].data.get("melhor_opcao_sugerida", {}) or {}
    hotel_rec = resultados["hotel"].data.get("melhor_opcao_sugerida", {}) or {}

    linhas = [
        f"✈️ Sua viagem de {ctx.cidade_origem or 'sua cidade'} para "
        f"**{ctx.cidade_destino}** foi planejada {status_txt}!",
        f"📅 Período: {ctx.data_saida.strftime('%d/%m/%Y')} a {ctx.data_retorno.strftime('%d/%m/%Y')} "
        f"({ctx.quantidade_dias} dias, {ctx.quantidade_noites} noites).",
    ]

    if passagens:
        linhas.append(
            f"🛫 Melhor opção de voo: **{passagens.get('companhia', 'N/A')}** "
            f"— R$ {passagens.get('preco_estimado', 0):,.2f} "
            f"({passagens.get('duracao_estimada', 'N/A')}, {passagens.get('escalas', 0)} escala(s))."
        )

    if hotel_rec:
        linhas.append(
            f"🏨 Hospedagem recomendada: **{hotel_rec.get('nome', 'N/A')}** "
            f"em {hotel_rec.get('bairro', 'N/A')} "
            f"— R$ {hotel_rec.get('preco_diaria', 0):,.2f}/noite "
            f"(avaliação: {hotel_rec.get('avaliacao', 'N/A')})."
        )

    linhas.append(
        "⚠️ Todos os valores são estimativas. Confirme preços e disponibilidade "
        "diretamente nos sites oficiais antes de realizar qualquer reserva ou compra."
    )
    return "\n\n".join(linhas)


# ──────────────────────────────────────────────────────────────
# Execução principal
# ──────────────────────────────────────────────────────────────


def run(req: TravelRequest, request_id: str = None) -> TravelPlan:
    """
    Ponto de entrada do maestro.
    Valida, constrói contexto, executa agentes em paralelo e consolida.
    """
    if request_id is None:
        request_id = str(uuid.uuid4())

    log_info(
        request_id, "maestro", f"Iniciando processamento para {req.cidade_destino}"
    )

    # 1. Validação
    erros_validacao = _validar_request(req)
    if erros_validacao:
        log_error(request_id, "maestro", f"Validação falhou: {erros_validacao}")
        return TravelPlan(
            request_id=request_id,
            status="erro",
            resumo={
                "cidade_destino": req.cidade_destino,
                "data_saida": str(req.data_saida) if req.data_saida else None,
                "data_retorno": str(req.data_retorno) if req.data_retorno else None,
            },
            resultado={},
            plano_integrado=IntegratedPlan(
                estimativa_custos=CostEstimation(),
                recomendacao_geral="Não foi possível processar a solicitação.",
            ),
            alertas=erros_validacao,
        )

    # 2. Construção do contexto
    ctx = _construir_contexto(req, request_id)
    log_info(
        request_id,
        "maestro",
        f"Contexto construído. Viagem: {ctx.cidade_origem or 'N/A'} -> {ctx.cidade_destino}, {ctx.quantidade_dias} dias",
    )

    # 3. Execução paralela dos agentes especialistas
    resultados: dict[str, AgentResult] = {}
    log_info(
        request_id,
        "maestro",
        "Iniciando execução paralela dos agentes especialistas...",
    )

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            "aereo": executor.submit(aereo.run, ctx, request_id),
            "hotel": executor.submit(hotel.run, ctx, request_id),
            "turismo": executor.submit(turismo.run, ctx, request_id),
        }
        for nome, future in futures.items():
            try:
                resultados[nome] = future.result(timeout=60)
                log_success(
                    request_id,
                    "maestro",
                    f"Agente {nome} concluído com status: {resultados[nome].status}",
                )
            except Exception as e:
                log_error(request_id, "maestro", f"Agente {nome} falhou: {str(e)}")
                resultados[nome] = AgentResult(
                    agent_name=f"agente_{nome}",
                    status="erro",
                    data={},
                    erros=[f"Agente {nome} falhou: {str(e)}"],
                    alertas=[f"Resultado do agente_{nome} não disponível."],
                )

    # 4. Determinação do status geral
    statuses = [r.status for r in resultados.values()]
    if all(s == "sucesso" for s in statuses):
        status_geral = "sucesso"
    elif all(s == "erro" for s in statuses):
        status_geral = "erro"
    else:
        status_geral = "parcial"

    log_info(request_id, "maestro", f"Status geral determinado: {status_geral}")

    # 5. Estimativa de custos e recomendação
    estimativa = _calcular_estimativa_custos(resultados["aereo"], resultados["hotel"])
    recomendacao = _gerar_recomendacao_geral(ctx, resultados)

    # 6. Consolidação dos alertas
    alertas_globais = [
        "⚠️ Preços de passagens variam rapidamente. Confirme antes de comprar.",
        "⚠️ Tarifas de hotel dependem de disponibilidade. Reserve com antecedência.",
        "⚠️ Horários de atrações turísticas podem variar. Consulte fontes oficiais.",
    ]
    for resultado in resultados.values():
        alertas_globais.extend(resultado.alertas)

    # 7. Resposta final
    log_success(
        request_id, "maestro", f"Processamento concluído. Status final: {status_geral}"
    )
    return TravelPlan(
        request_id=request_id,
        status=status_geral,
        resumo={
            "cidade_destino": ctx.cidade_destino,
            "cidade_origem": ctx.cidade_origem,
            "data_saida": str(ctx.data_saida),
            "data_retorno": str(ctx.data_retorno),
            "duracao_dias": ctx.quantidade_dias,
            "quantidade_noites": ctx.quantidade_noites,
        },
        resultado={
            "passagens_aereas": resultados["aereo"],
            "hoteis": resultados["hotel"],
            "roteiro_turistico": resultados["turismo"],
        },
        plano_integrado=IntegratedPlan(
            estimativa_custos=estimativa,
            recomendacao_geral=recomendacao,
        ),
        alertas=list(dict.fromkeys(alertas_globais)),  # deduplica mantendo ordem
    )
