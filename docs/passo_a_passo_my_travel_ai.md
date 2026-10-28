# Passo a Passo: Como o `my-travel-ai` Funciona

## 🔹 Passo 1 — O Usuário Preenche o Formulário

O ponto de partida é a interface web em [`static/index.html`](file:///home/armando_sousa/my-travel-ai/static/index.html). O usuário preenche:

- Cidade de destino (ex: "Lisboa")
- Cidade de origem (ex: "São Paulo")
- Data de ida e volta
- Número de viajantes
- Preferências de voo, hotel e ritmo do roteiro

O JavaScript em [`static/index.js`](file:///home/armando_sousa/my-travel-ai/static/index.js) coleta esses dados e monta um JSON:

```json
{
  "cidade_destino": "Lisboa",
  "cidade_origem": "São Paulo",
  "data_saida": "2026-12-01",
  "data_retorno": "2026-12-08",
  "quantidade_viajantes": 2,
  "preferencia_voo": "melhor_custo_beneficio",
  "preferencia_hotel": "melhor_custo_beneficio",
  "ritmo_roteiro": "moderado"
}
```

---

## 🔹 Passo 2 — O Frontend Envia o Pedido para a API

O JS faz um `POST /api/plan` com o JSON acima. Essa rota está definida em [`app/api/routes/plan.py`](file:///home/armando_sousa/my-travel-ai/app/api/routes/plan.py#L15-L54).

O que acontece aqui:
1. Gera um `request_id` único (UUID).
2. Cria uma **fila de eventos** no [`EventLogger`](file:///home/armando_sousa/my-travel-ai/app/agents/logger.py#L36-L56) para esse ID — essa fila vai servir para transmitir os logs em tempo real.
3. Converte o `PlanRequest` da API em um objeto interno [`TravelRequest`](file:///home/armando_sousa/my-travel-ai/app/models/travel.py#L15-L21) com [`TravelPreferences`](file:///home/armando_sousa/my-travel-ai/app/models/travel.py#L5-L14).
4. **Dispara uma thread em background** para processar o plano — assim a API responde instantaneamente sem bloquear.
5. Retorna imediatamente ao frontend:
   ```json
   {"request_id": "abc-123", "status": "processing", "message": "Use GET /api/stream/abc-123 para acompanhar."}
   ```

> **Ponto-chave**: O processamento pesado acontece em uma thread separada. O usuário não fica esperando.

---

## 🔹 Passo 3 — O Frontend Abre a Conexão SSE (Streaming)

Ao receber o `request_id`, o JavaScript abre uma conexão **Server-Sent Events (SSE)** com `GET /api/stream/{request_id}` ([`stream.py`](file:///home/armando_sousa/my-travel-ai/app/api/routes/stream.py#L15-L51)):

```javascript
const eventSource = new EventSource(`/api/stream/${requestId}`);
```

A partir daqui, o navegador recebe mensagens em tempo real. O endpoint SSE fica num loop:
- Se tem evento na fila → envia ao frontend como `data: {...}\n\n`
- Se não tem evento mas o resultado final existe → envia `{"event": "done", "result": {...}}` e encerra
- Se nenhum dos dois → espera 0.5 segundo e verifica de novo

---

## 🔹 Passo 4 — A Thread de Background Inicia o Maestro

Na thread, a função [`run_maestro_background`](file:///home/armando_sousa/my-travel-ai/app/services/planning_jobs.py#L15-L29) chama o orquestrador principal:

```python
plano = maestro.run(travel_req, request_id=request_id)
```

---

## 🔹 Passo 5 — O Maestro Valida a Requisição

Dentro de [`maestro.run()`](file:///home/armando_sousa/my-travel-ai/app/agents/maestro.py#L169-L290), a primeira coisa que acontece é a **validação** ([`_validar_request`](file:///home/armando_sousa/my-travel-ai/app/agents/maestro.py#L37-L58)):

- `cidade_destino` está preenchida?
- `data_saida` e `data_retorno` existem?
- `data_retorno > data_saida`? (No mínimo 1 noite)

Se houver erros, o Maestro retorna um `TravelPlan` com `status="erro"` e a lista de problemas, **sem acionar nenhum agente**.

---

## 🔹 Passo 6 — O Maestro Constrói o Contexto de Viagem

Se a validação passou, o Maestro monta o objeto [`TravelContext`](file:///home/armando_sousa/my-travel-ai/app/agents/maestro.py#L61-L76) que é compartilhado com todos os agentes:

```python
TravelContext(
    request_id="abc-123",
    cidade_destino="Lisboa",          # normalizado com .title()
    cidade_origem="São Paulo",
    quantidade_dias=8,                # calculado: (retorno - saída).days + 1
    quantidade_noites=7,              # calculado: (retorno - saída).days
    preferencias=TravelPreferences(...),
    execucao=ExecutionMetadata(idioma="pt-BR", timestamp="...")
)
```

---

## 🔹 Passo 7 — Execução Paralela dos 3 Agentes Especialistas

Este é o **coração da arquitetura multiagente**. O Maestro abre um [`ThreadPoolExecutor`](file:///home/armando_sousa/my-travel-ai/app/agents/maestro.py#L217-L240) com 3 workers e despacha simultaneamente:

```python
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    futures = {
        "aereo":  executor.submit(aereo.run, ctx, request_id),
        "hotel":  executor.submit(hotel.run, ctx, request_id),
        "turismo": executor.submit(turismo.run, ctx, request_id),
    }
```

Os três agentes executam **em paralelo**, cada um em sua própria thread:

### 🛫 Agente Aéreo ([`aereo.py`](file:///home/armando_sousa/my-travel-ai/app/agents/aereo.py))
1. Verifica se `GEMINI_API_KEY` existe → se sim, usa LLM; se não, usa heurística local.
2. Na heurística: busca na base de conhecimento [`_CONHECIMENTO_AEREO`](file:///home/armando_sousa/my-travel-ai/app/agents/base_local.py#L5-L191) as companhias aéreas, preços base, escalas e duração para o destino.
3. Aplica um **fator de temporada** baseado no mês da viagem (alta/média/baixa demanda).
4. Calcula um score ponderado para cada opção: `40% preço + 25% duração + 20% escalas + 15% confiança`.
5. Ordena do melhor para o pior score.
6. Retorna um [`AgentResult`](file:///home/armando_sousa/my-travel-ai/app/models/travel.py#L82-L90) com a lista de opções e a melhor sugestão.

### 🏨 Agente Hotel ([`hotel.py`](file:///home/armando_sousa/my-travel-ai/app/agents/hotel.py))
1. Mesmo padrão: LLM ou heurística.
2. Na heurística: busca em [`_CONHECIMENTO_HOTEL`](file:///home/armando_sousa/my-travel-ai/app/agents/base_local.py#L210-L499) os hotéis reais por destino (com bairro, categoria, diária e avaliação).
3. Calcula score: `35% localização + 25% avaliação + 25% preço + 15% comodidades`.
4. Multiplica a diária pelo número de noites para obter o custo total.
5. Retorna `AgentResult` com opções ranqueadas.

### 🗺️ Agente Turismo ([`turismo.py`](file:///home/armando_sousa/my-travel-ai/app/agents/turismo.py))
1. Busca pontos turísticos em [`_PONTOS_TURISTICOS`](file:///home/armando_sousa/my-travel-ai/app/agents/base_local.py#L505) e dicas gerais.
2. Distribui atrações entre os dias da viagem, separando por **manhã**, **tarde** e **noite**.
3. Tratamento especial: Dia 1 = check-in e descanso; Último dia = atividades leves e ida ao aeroporto.
4. Retorna `AgentResult` com um `DailyItinerary` completo por dia.

> **Durante toda a execução**, cada agente envia logs ao [`EventLogger`](file:///home/armando_sousa/my-travel-ai/app/agents/logger.py#L58-L70), e esses logs são transmitidos instantaneamente via SSE para o frontend, que atualiza os spinners e cards de progresso.

---

## 🔹 Passo 8 — O Maestro Consolida os Resultados

Quando os 3 agentes terminam (ou falham com timeout de 60s), o Maestro:

1. **Determina o status geral**:
   - Todos `"sucesso"` → `"sucesso"`
   - Todos `"erro"` → `"erro"`
   - Misturado → `"parcial"` (o plano é entregue parcialmente)

2. **Calcula a estimativa de custos** ([`_calcular_estimativa_custos`](file:///home/armando_sousa/my-travel-ai/app/agents/maestro.py#L84-L125)):
   - Passagens: preço da melhor opção aérea
   - Hospedagem: preço total da melhor opção de hotel
   - Passeios: estimado como **20%** do total de passagens + hospedagem
   - **Total = passagens + hospedagem + passeios**

3. **Gera a recomendação textual** ([`_gerar_recomendacao_geral`](file:///home/armando_sousa/my-travel-ai/app/agents/maestro.py#L127-L161)): Um texto consolidado em Markdown com emojis destacando a melhor companhia aérea, hotel recomendado e período da viagem.

4. **Monta o objeto final** [`TravelPlan`](file:///home/armando_sousa/my-travel-ai/app/agents/maestro.py#L269-L290) contendo tudo: resumo, resultados dos 3 agentes, plano integrado com custos e alertas.

---

## 🔹 Passo 9 — O Resultado é Salvo e Entregue via SSE

De volta na thread de background ([`planning_jobs.py`](file:///home/armando_sousa/my-travel-ai/app/services/planning_jobs.py#L17-L21)):

```python
plano = maestro.run(travel_req, request_id=request_id)
results_store[request_id] = plano.model_dump()   # salva como dict
event_logger.log(request_id, "system", "success", "PROCESSAMENTO_CONCLUIDO")
```

O endpoint SSE detecta que `results_store` agora contém o resultado para esse `request_id` e envia o evento final:

```
data: {"event": "done", "result": { ...plano completo... }}
```

---

## 🔹 Passo 10 — O Frontend Renderiza o Resultado Final

O JavaScript em [`index.js`](file:///home/armando_sousa/my-travel-ai/static/index.js#L663-L713) recebe o evento `done`, fecha a conexão SSE e:

1. Finaliza as animações dos cards de agentes (spinners → ✅ ou ⚠️).
2. Renderiza o **resumo da viagem** (destino, datas, duração).
3. Renderiza os **cards de custos** (passagens, hospedagem, passeios, total).
4. Preenche as **abas de resultado**:
   - ✈️ Passagens Aéreas (tabela comparativa de opções ranqueadas)
   - 🏨 Hospedagem (cards por hotel com estrelas, avaliação e preço)
   - 🗺️ Roteiro Turístico (itinerário dia a dia)
   - ⚠️ Alertas e Dicas gerais
5. Faz scroll suave até a seção de resultados.

---

## Resumo Visual do Fluxo Completo

```
Usuário preenche formulário
    ↓
POST /api/plan → gera request_id, dispara thread
    ↓                          ↓
Frontend abre SSE ←────── Thread executa Maestro
    ↓                          ↓
Recebe logs em              Maestro valida → constrói contexto
tempo real                     ↓
    ↓                     ThreadPool(3 workers)
Atualiza spinners          ┌──────┬──────┬──────┐
    ↓                      Aéreo  Hotel  Turismo  ← executam em paralelo
    ↓                      └──────┴──────┴──────┘
    ↓                          ↓
    ↓                     Maestro consolida custos + recomendação
    ↓                          ↓
    ↓                     Salva resultado em memória
    ↓                          ↓
SSE envia {"event":"done"} ←──┘
    ↓
Frontend renderiza abas de resultado
```
