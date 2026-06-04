## User

[@teste.txt (1:2)](file:///home/armando/%C3%81rea%20de%20trabalho/TCA/my-travel-ai/temp/teste.txt#L1:2)

## Assistant

<thinking>
Got it, let's tackle this. First, the user wants an implementation plan for adding a log panel to their travel AI app. Let's start by understanding the existing structure first, right? Wait, the user provided a selection from teste.txt that describes the current flow: after clicking "Planejar Viagem", it shows "Agentes em Ação" with Maestro, Aéreo, Hotel, Turismo actions, plus Consolidação panel, then a summary. They want to add a new log panel below "Agentes em Ação", show real-time logs in both terminal and UI, capture events from those agents, keep original features.

First step: I need to check the existing project structure to make the plan accurate. Let's list the root directory is /home/armando/Área de trabalho/TCA/my-travel-ai. Let's first explore the project structure to see what's there. Wait, but the user said first create the plan, but the plan needs to be based on the actual codebase, right? So maybe first, let's get the project structure. Let's use list_directory on the root, then maybe look for existing components, especially the "Agentes em Ação" panel, the agents' code, how events are currently handled.

Wait, the user's request says "Neste primeiro momento crie primeiro o plano de implementação". So first, I need to create a detailed plan, but to make it useful, I should first gather context about the existing app. Let's start by exploring the project.

First, let's list the root directory of the project. Let's use list_directory on the project root. Then, look for frontend (UI) files, backend (where agents are defined), existing event systems, etc.

Wait, let's do that step by step. First, list the project root to see the structure. Let's call list_directory on "my-travel-ai" (since the root is that directory). Wait, the project root is /home/armando/Área de trabalho/TCA/my-travel-ai, so the relative path is just the root, so list_directory with path "my-travel-ai"? No, wait, the tool's path parameter is relative to the project root. Wait, the project's root directories are listed as /home/armando/Área de trabalho/TCA/my-travel-ai, so when using list_directory, the path should be the relative path within that root. So to list the root, the path is ""? No, wait, let's check the tool description: list_directory's path is the fully-qualified path relative to the project root. So if the project root is my-travel-ai, then to list its contents, the path is ".". Wait, no, let's see: the example says if the project has root directories directory1 and directory2, then list directory1 by using path "directory1". Oh right, the first component of the path must be a root directory. So the project's root directory is "my-travel-ai"? Wait no, the user said "the current project contains the following root directories: /home/armando/Área de trabalho/TCA/my-travel-ai". So the root directory name is "my-travel-ai"? Wait, no, the root directory is the top-level directory of the project. So when using tools, the path should start with that root directory. Wait, let's confirm: the tool says "the first component of the path should always be a root directory in a project." So the root directory here is "my-travel-ai"? Wait, no, the full path is /home/armando/Área de trabalho/TCA/my-travel-ai, so the root directory in the project context is "my-travel-ai"? Or is the entire path the root? Wait, no, the user's project root is that directory, so when using list_directory, the path is "my-travel-ai"? No, wait, let's try list_directory with path "my-travel-ai" to see what's inside. Alternatively, maybe the root is the directory itself, so the relative path is empty? No, let's check the example: if the project has root directories lorem and ipsum, then to list lorem's contents, path is "lorem". So in this case, the project's only root directory is "my-travel-ai", so to list its contents, path is "my-travel-ai".

Wait, but let's also check the temp directory where teste.txt is, but maybe first focus on the main app. Let's also look for existing agent files. Let's use find_path to search for files related to agents, like "agente", "maestro", "aereo", "hotel", "turismo". Also, look for the "Agentes em Ação" component, maybe in the frontend (like React, Vue, etc. files). Let's also check if there's a backend with agent logic, maybe Python, Node.js, etc.

Wait, but the user wants the plan first. But to make the plan accurate, I need to know the existing tech stack. Let's gather that info first. Let's do:

1. List the project root to see the structure.
2. Search for agent-related files.
3. Find the existing "Agentes em Ação" UI component.
4. Check how events are currently emitted (if any) from the agents.

Let's start with listing the project root. Let's call list_directory on "my-travel-ai". Then, use find_path to search for files with "agente" in the name. Also, grep for "Agentes em Ação" to find where that component is.

Wait, let's do that now. Let's make the tool calls. First, list_directory for the project root. Then, find_path for "**/*agente*". Then, grep for "Agentes em Ação" to find the UI component. Also, check the frontend framework: look for package.json, or if there's a src directory with components.

Wait, let's structure the plan after gathering context. But the user said first create the plan. But the plan needs to be based on the actual codebase. So first, gather context, then create the plan.

Wait, let's proceed step by step. First, explore the project. Let's call list_directory on "my-travel-ai" to see the top-level files and
</thinking>

Vou primeiro explorar a estrutura do projeto para entender o stack tecnológico, onde estão os agentes e o componente "Agentes em Ação" existente, antes de criar o plano de implementação.

Vamos começar listando a estrutura raiz do projeto e buscando arquivos relacionados aos agentes:

**Tool Call: List the `my-travel-ai` directory's contents**
Status: Completed

# Folders:
my-travel-ai/.venv
my-travel-ai/__pycache__
my-travel-ai/agents
my-travel-ai/docs
my-travel-ai/new_features
my-travel-ai/planos
my-travel-ai/skills
my-travel-ai/static
my-travel-ai/temp
my-travel-ai/tests

# Files:
my-travel-ai/.gitignore
my-travel-ai/README.md
my-travel-ai/main.py
my-travel-ai/models.py
my-travel-ai/package.json
my-travel-ai/projeto.md
my-travel-ai/requirements.txt
my-travel-ai/run.sh


**Tool Call: No matches**
Status: Completed

```json
{
  "offset": 0,
  "current_matches_page": [],
  "all_matches_len": 0
}
```

**Tool Call: Search files for regex `Agentes em Ação`**
Status: Completed

Found 2 matches:

## Matches in my-travel-ai/static/index.html

### html › body › section › div › div › h2 › L313-318
```
                <div class="agents-header">
                    <h2 class="section-title">🤖 Agentes em Ação</h2>
                    <p class="section-subtitle">
                        Sua equipe de especialistas em IA está trabalhando...
                    </p>
                </div>
```

## Matches in my-travel-ai/temp/teste.txt

### L1-3
```
Logo após o usuário clicar no botão "Planejar Viagem", a aplicação web mostra Agentes em Ação, mostrando as ações do Maestro, as ações do Agente Aéreo, as ações do Agente Hotel e as ações do Agente Turismo. Além disso, mostra as ações n o painel Consolidação. Ao final mostra um resumo das operações concluídas, incluindo se todas as operações foram concluídas com sucesso ou não. Procure manter as funcionalidades originais da aplicação e apenas adicionar o novo painel de logs.
Você pode criar um plano de implementação para capturar os logs dos principais eventos desta aplicação? Ou seja, capture os logs das atividades do agente maestro, do agente aereo, do agente hotel, do agente turismo. Esses logs devem ser exibidos no terminal da aplicação e também deve ser criado um novo painel web, na UI (User Inteface) da aplicação web, logo abaixo do painel que mostra "Agentes em Ação" com as ações dos agentes Maestro, Aereo, Hotel e Turismo. Este novo painel web de logs deve mostrar as ações e eventos que estão acontecendo e exibir as operações em tempo real para que o usuário possa visualizar as ações, eventos, operações dos agentes maestro, aereo, hotel e turismo na própria aplicação web. Ao final tambẽm mostre se todas as operações foram concluídas com sucesso ou não. Neste primeiro momento crie primeiro o plano de implementação, lembre-se de manter todas as funcionalidades originais da aplicação e apenas adicionar o novo painel de logs.

```


## Assistant

Agora vamos explorar a pasta `agents`, o `main.py`, `models.py` e o `static/index.html` para entender a arquitetura:

**Tool Call: List the `my-travel-ai/agents` directory's contents**
Status: Completed

# Folders:
my-travel-ai/agents/__pycache__

# Files:
my-travel-ai/agents/__init__.py
my-travel-ai/agents/aereo.py
my-travel-ai/agents/hotel.py
my-travel-ai/agents/maestro.py
my-travel-ai/agents/turismo.py


**Tool Call: Read file `main.py`**
Status: Completed

```my-travel-ai/main.py
     1	"""
     2	main.py — Ponto de entrada da aplicação FastAPI.
     3	
     4	Expõe os endpoints da API REST e serve a interface web estática.
     5	"""
     6	import sys
     7	import os
     8	
     9	# Garante que os módulos do projeto sejam encontrados
    10	sys.path.insert(0, os.path.dirname(__file__))
    11	
    12	from fastapi import FastAPI, HTTPException
    13	from fastapi.staticfiles import StaticFiles
    14	from fastapi.responses import FileResponse
    15	from pydantic import BaseModel, Field
    16	from datetime import date
    17	from typing import Optional, List
    18	
    19	from models import TravelRequest, TravelPreferences, TravelPlan
    20	from agents import maestro
    21	
    22	
    23	# ──────────────────────────────────────────────────────────────
    24	# Modelos de entrada da API (compatíveis com formulário web)
    25	# ──────────────────────────────────────────────────────────────
    26	
    27	class PlanRequest(BaseModel):
    28	    cidade_destino: str = Field(..., description="Cidade de destino")
    29	    data_saida: date = Field(..., description="Data de início (YYYY-MM-DD)")
    30	    data_retorno: date = Field(..., description="Data de retorno (YYYY-MM-DD)")
    31	    cidade_origem: Optional[str] = Field(default=None, description="Cidade de origem (opcional)")
    32	    quantidade_viajantes: int = Field(default=1, ge=1, description="Número de viajantes")
    33	    preferencia_voo: str = Field(default="melhor_custo_beneficio")
    34	    preferencia_hotel: str = Field(default="melhor_custo_beneficio")
    35	    categoria_hotel: Optional[str] = Field(default=None)
    36	    ritmo_roteiro: str = Field(default="moderado")
    37	    interesses: List[str] = Field(default_factory=list)
    38	
    39	
    40	# ──────────────────────────────────────────────────────────────
    41	# Aplicação FastAPI
    42	# ──────────────────────────────────────────────────────────────
    43	
    44	app = FastAPI(
    45	    title="🌍 Agente de Planejamento de Viagens",
    46	    description="API multiagente para geração de planos de viagem integrados: voos, hotéis e roteiro turístico.",
    47	    version="1.0.0",
    48	    docs_url="/docs",
    49	    redoc_url="/redoc",
    50	)
    51	
    52	
    53	@app.get("/api/health")
    54	async def health_check():
    55	    """Verifica se a API está operacional."""
    56	    return {
    57	        "status": "ok",
    58	        "service": "Travel Planner Multiagent API",
    59	        "version": "1.0.0",
    60	        "llm_enabled": bool(os.environ.get("GEMINI_API_KEY")),
    61	    }
    62	
    63	
    64	@app.post("/api/plan", response_model=None)
    65	async def generate_travel_plan(request: PlanRequest):
    66	    """
    67	    Gera um plano de viagem integrado.
    68	    
    69	    Aciona os agentes maestro, agente_aereo, agente_hotel e agente_turismo em paralelo
    70	    e retorna um plano consolidado com passagens, hotéis e roteiro turístico.
    71	    """
    72	    try:
    73	        # Constrói TravelRequest a partir do PlanRequest da API
    74	        travel_req = TravelRequest(
    75	            cidade_destino=request.cidade_destino,
    76	            data_saida=request.data_saida,
    77	            data_retorno=request.data_retorno,
    78	            cidade_origem=request.cidade_origem,
    79	            preferencias=TravelPreferences(
    80	                quantidade_viajantes=request.quantidade_viajantes,
    81	                quantidade_hospedes=request.quantidade_viajantes,
    82	                quantidade_quartos=max(1, request.quantidade_viajantes // 2),
    83	                preferencia_voo=request.preferencia_voo,
    84	                preferencia_hotel=request.preferencia_hotel,
    85	                categoria_hotel=request.categoria_hotel,
    86	                ritmo_roteiro=request.ritmo_roteiro,
    87	                interesses=request.interesses,
    88	            ),
    89	        )
    90	
    91	        plano = maestro.run(travel_req)
    92	
    93	        if plano.status == "erro":
    94	            raise HTTPException(status_code=422, detail={
    95	                "message": "Não foi possível processar a solicitação.",
    96	                "erros": plano.alertas,
    97	            })
    98	
    99	        return plano.model_dump()
   100	
   101	    except HTTPException:
   102	        raise
   103	    except Exception as e:
   104	        raise HTTPException(status_code=500, detail=str(e))
   105	
   106	
   107	# ──────────────────────────────────────────────────────────────
   108	# Servir interface web
   109	# ──────────────────────────────────────────────────────────────
   110	
   111	static_dir = os.path.join(os.path.dirname(__file__), "static")
   112	if os.path.exists(static_dir):
   113	    app.mount("/static", StaticFiles(directory=static_dir), name="static")
   114	
   115	    @app.get("/")
   116	    async def serve_frontend():
   117	        """Serve a interface web principal."""
   118	        return FileResponse(os.path.join(static_dir, "index.html"))

```


**Tool Call: Read file `static/index.html` (lines 300-450)**
Status: Completed

```my-travel-ai/static/index.html
   300	                                        />
   301	                                    </svg>
   302	                                </span>
   303	                            </button>
   304	                        </div>
   305	                    </form>
   306	                </div>
   307	            </div>
   308	        </section>
   309	
   310	        <!-- ── AGENTS PROGRESS ── -->
   311	        <section id="agents-progress" class="agents-section hidden">
   312	            <div class="container">
   313	                <div class="agents-header">
   314	                    <h2 class="section-title">🤖 Agentes em Ação</h2>
   315	                    <p class="section-subtitle">
   316	                        Sua equipe de especialistas em IA está trabalhando...
   317	                    </p>
   318	                </div>
   319	                <div class="agents-timeline">
   320	                    <div
   321	                        class="agent-card"
   322	                        id="agent-maestro"
   323	                        data-status="waiting"
   324	                    >
   325	                        <div class="agent-icon">🎼</div>
   326	                        <div class="agent-info">
   327	                            <div class="agent-name">Maestro</div>
   328	                            <div class="agent-desc">
   329	                                Validando e coordenando os agentes...
   330	                            </div>
   331	                        </div>
   332	                        <div class="agent-status-badge">Aguardando</div>
   333	                    </div>
   334	                    <div class="agent-connector"></div>
   335	                    <div class="agents-parallel">
   336	                        <div
   337	                            class="agent-card"
   338	                            id="agent-aereo"
   339	                            data-status="waiting"
   340	                        >
   341	                            <div class="agent-icon">✈️</div>
   342	                            <div class="agent-info">
   343	                                <div class="agent-name">Agente Aéreo</div>
   344	                                <div class="agent-desc">
   345	                                    Buscando melhores voos...
   346	                                </div>
   347	                            </div>
   348	                            <div class="agent-status-badge">Aguardando</div>
   349	                        </div>
   350	                        <div
   351	                            class="agent-card"
   352	                            id="agent-hotel"
   353	                            data-status="waiting"
   354	                        >
   355	                            <div class="agent-icon">🏨</div>
   356	                            <div class="agent-info">
   357	                                <div class="agent-name">Agente Hotel</div>
   358	                                <div class="agent-desc">
   359	                                    Pesquisando hospedagens...
   360	                                </div>
   361	                            </div>
   362	                            <div class="agent-status-badge">Aguardando</div>
   363	                        </div>
   364	                        <div
   365	                            class="agent-card"
   366	                            id="agent-turismo"
   367	                            data-status="waiting"
   368	                        >
   369	                            <div class="agent-icon">🗺️</div>
   370	                            <div class="agent-info">
   371	                                <div class="agent-name">Agente Turismo</div>
   372	                                <div class="agent-desc">
   373	                                    Montando roteiro diário...
   374	                                </div>
   375	                            </div>
   376	                            <div class="agent-status-badge">Aguardando</div>
   377	                        </div>
   378	                    </div>
   379	                    <div class="agent-connector"></div>
   380	                    <div
   381	                        class="agent-card"
   382	                        id="agent-consolidar"
   383	                        data-status="waiting"
   384	                    >
   385	                        <div class="agent-icon">📋</div>
   386	                        <div class="agent-info">
   387	                            <div class="agent-name">Consolidação</div>
   388	                            <div class="agent-desc">
   389	                                Montando plano final...
   390	                            </div>
   391	                        </div>
   392	                        <div class="agent-status-badge">Aguardando</div>
   393	                    </div>
   394	                </div>
   395	            </div>
   396	        </section>
   397	
   398	        <!-- ── RESULTS ── -->
   399	        <section id="results-section" class="results-section hidden">
   400	            <div class="container">
   401	                <!-- Sumário da viagem -->
   402	                <div class="trip-summary glass" id="trip-summary">
   403	                    <div class="summary-header">
   404	                        <div class="summary-badge" id="status-badge"></div>
   405	                        <h2 class="summary-title" id="summary-title"></h2>
   406	                    </div>
   407	                    <div class="summary-stats" id="summary-stats"></div>
   408	                    <div
   409	                        class="summary-recommendation"
   410	                        id="summary-recommendation"
   411	                    ></div>
   412	                </div>
   413	
   414	                <!-- Estimativa de custos -->
   415	                <div class="cost-cards" id="cost-cards"></div>
   416	
   417	                <!-- Tabs -->
   418	                <div class="tabs-container">
   419	                    <div class="tabs-nav" role="tablist">
   420	                        <button
   421	                            class="tab-btn active"
   422	                            role="tab"
   423	                            data-tab="flights"
   424	                            aria-selected="true"
   425	                            id="tab-flights"
   426	                        >
   427	                            ✈️ Voos
   428	                        </button>
   429	                        <button
   430	                            class="tab-btn"
   431	                            role="tab"
   432	                            data-tab="hotels"
   433	                            aria-selected="false"
   434	                            id="tab-hotels"
   435	                        >
   436	                            🏨 Hotéis
   437	                        </button>
   438	                        <button
   439	                            class="tab-btn"
   440	                            role="tab"
   441	                            data-tab="itinerary"
   442	                            aria-selected="false"
   443	                            id="tab-itinerary"
   444	                        >
   445	                            🗺️ Roteiro
   446	                        </button>
   447	                        <button
   448	                            class="tab-btn"
   449	                            role="tab"
   450	                            data-tab="alerts"

```


## Assistant

<thinking>
Now I have a good understanding of the project structure. Let me also read the agents files to understand how they work and where to add logging. Let me also check the JavaScript file that handles the frontend interactions.

Key findings so far:
1. Backend: FastAPI (main.py) with agents in /agents/ folder (maestro.py, aereo.py, hotel.py, turismo.py)
2. Frontend: static/index.html with "
</thinking>

Agora vamos ler os arquivos dos agentes e verificar se há um arquivo JavaScript no frontend:

**Tool Call: Read file `agents/maestro.py`**
Status: Completed

```my-travel-ai/agents/maestro.py
     1	"""
     2	maestro.py — Agente orquestrador principal do sistema de planejamento de viagens.
     3	
     4	Responsável por: validar entradas, normalizar dados, acionar os agentes especialistas
     5	em paralelo, tratar falhas parciais e consolidar a resposta final conforme definido
     6	em skill.md e plano.md.
     7	"""
     8	from datetime import date, datetime
     9	from typing import Optional
    10	import uuid
    11	import concurrent.futures
    12	
    13	from models import (
    14	    TravelRequest, TravelContext, TravelPreferences, AgentResult,
    15	    CostEstimation, IntegratedPlan, TravelPlan, ExecutionMetadata
    16	)
    17	from agents import aereo, hotel, turismo
    18	
    19	
    20	# ──────────────────────────────────────────────────────────────
    21	# Validação e normalização
    22	# ──────────────────────────────────────────────────────────────
    23	
    24	def _validar_request(req: TravelRequest) -> list[str]:
    25	    """Retorna lista de erros de validação."""
    26	    erros = []
    27	
    28	    if not req.cidade_destino or not req.cidade_destino.strip():
    29	        erros.append("Campo obrigatório ausente: 'cidade_destino'.")
    30	
    31	    if not req.data_saida:
    32	        erros.append("Campo obrigatório ausente: 'data_saida'.")
    33	
    34	    if not req.data_retorno:
    35	        erros.append("Campo obrigatório ausente: 'data_retorno'.")
    36	
    37	    if req.data_saida and req.data_retorno:
    38	        if req.data_retorno <= req.data_saida:
    39	            erros.append("'data_retorno' deve ser posterior à 'data_saida'.")
    40	
    41	        delta = (req.data_retorno - req.data_saida).days
    42	        if delta < 1:
    43	            erros.append("A viagem deve ter pelo menos 1 noite de hospedagem.")
    44	
    45	    return erros
    46	
    47	
    48	def _construir_contexto(req: TravelRequest, request_id: str) -> TravelContext:
    49	    """Transforma TravelRequest em TravelContext enriquecido."""
    50	    quantidade_dias = (req.data_retorno - req.data_saida).days + 1
    51	    quantidade_noites = (req.data_retorno - req.data_saida).days
    52	
    53	    return TravelContext(
    54	        request_id=request_id,
    55	        cidade_destino=req.cidade_destino.strip().title(),
    56	        data_saida=req.data_saida,
    57	        data_retorno=req.data_retorno,
    58	        cidade_origem=req.cidade_origem.strip().title() if req.cidade_origem else None,
    59	        quantidade_dias=quantidade_dias,
    60	        quantidade_noites=quantidade_noites,
    61	        preferencias=req.preferencias,
    62	        execucao=ExecutionMetadata(),
    63	    )
    64	
    65	
    66	# ──────────────────────────────────────────────────────────────
    67	# Consolidação da resposta
    68	# ──────────────────────────────────────────────────────────────
    69	
    70	def _calcular_estimativa_custos(
    71	    resultado_aereo: AgentResult,
    72	    resultado_hotel: AgentResult,
    73	) -> CostEstimation:
    74	    """Estima custos totais a partir dos resultados dos agentes."""
    75	    passagens = None
    76	    hospedagem = None
    77	
    78	    try:
    79	        if resultado_aereo.status in ("sucesso", "parcial"):
    80	            opcoes = resultado_aereo.data.get("opcoes", [])
    81	            if opcoes:
    82	                melhor = max(opcoes, key=lambda x: x.get("score", 0))
    83	                passagens = melhor.get("preco_estimado")
    84	    except Exception:
    85	        pass
    86	
    87	    try:
    88	        if resultado_hotel.status in ("sucesso", "parcial"):
    89	            opcoes = resultado_hotel.data.get("opcoes", [])
    90	            if opcoes:
    91	                melhor = max(opcoes, key=lambda x: x.get("score", 0))
    92	                hospedagem = melhor.get("preco_estimado_total")
    93	    except Exception:
    94	        pass
    95	
    96	    total = None
    97	    if passagens is not None and hospedagem is not None:
    98	        # Adiciona 20% estimado para passeios, alimentação e transporte local
    99	        passeios = round((passagens + hospedagem) * 0.20, 2)
   100	        total = round(passagens + hospedagem + passeios, 2)
   101	    else:
   102	        passeios = None
   103	
   104	    return CostEstimation(
   105	        passagens=passagens,
   106	        hospedagem=hospedagem,
   107	        passeios=passeios,
   108	        total_estimado=total,
   109	        moeda="BRL",
   110	    )
   111	
   112	
   113	def _gerar_recomendacao_geral(ctx: TravelContext, resultados: dict) -> str:
   114	    """Gera um texto de recomendação consolidado."""
   115	    status_geral = all(
   116	        r.status == "sucesso" for r in resultados.values()
   117	    )
   118	    status_txt = "com sucesso" if status_geral else "parcialmente"
   119	
   120	    passagens = resultados["aereo"].data.get("melhor_opcao_sugerida", {}) or {}
   121	    hotel_rec = resultados["hotel"].data.get("melhor_opcao_sugerida", {}) or {}
   122	
   123	    linhas = [
   124	        f"✈️ Sua viagem de {ctx.cidade_origem or 'sua cidade'} para "
   125	        f"**{ctx.cidade_destino}** foi planejada {status_txt}!",
   126	        f"📅 Período: {ctx.data_saida.strftime('%d/%m/%Y')} a {ctx.data_retorno.strftime('%d/%m/%Y')} "
   127	        f"({ctx.quantidade_dias} dias, {ctx.quantidade_noites} noites).",
   128	    ]
   129	
   130	    if passagens:
   131	        linhas.append(
   132	            f"🛫 Melhor opção de voo: **{passagens.get('companhia', 'N/A')}** "
   133	            f"— R$ {passagens.get('preco_estimado', 0):,.2f} "
   134	            f"({passagens.get('duracao_estimada', 'N/A')}, {passagens.get('escalas', 0)} escala(s))."
   135	        )
   136	
   137	    if hotel_rec:
   138	        linhas.append(
   139	            f"🏨 Hospedagem recomendada: **{hotel_rec.get('nome', 'N/A')}** "
   140	            f"em {hotel_rec.get('bairro', 'N/A')} "
   141	            f"— R$ {hotel_rec.get('preco_diaria', 0):,.2f}/noite "
   142	            f"(avaliação: {hotel_rec.get('avaliacao', 'N/A')})."
   143	        )
   144	
   145	    linhas.append(
   146	        "⚠️ Todos os valores são estimativas. Confirme preços e disponibilidade "
   147	        "diretamente nos sites oficiais antes de realizar qualquer reserva ou compra."
   148	    )
   149	    return "\n\n".join(linhas)
   150	
   151	
   152	# ──────────────────────────────────────────────────────────────
   153	# Execução principal
   154	# ──────────────────────────────────────────────────────────────
   155	
   156	def run(req: TravelRequest) -> TravelPlan:
   157	    """
   158	    Ponto de entrada do maestro.
   159	    Valida, constrói contexto, executa agentes em paralelo e consolida.
   160	    """
   161	    request_id = str(uuid.uuid4())
   162	
   163	    # 1. Validação
   164	    erros_validacao = _validar_request(req)
   165	    if erros_validacao:
   166	        return TravelPlan(
   167	            request_id=request_id,
   168	            status="erro",
   169	            resumo={
   170	                "cidade_destino": req.cidade_destino,
   171	                "data_saida": str(req.data_saida) if req.data_saida else None,
   172	                "data_retorno": str(req.data_retorno) if req.data_retorno else None,
   173	            },
   174	            resultado={},
   175	            plano_integrado=IntegratedPlan(
   176	                estimativa_custos=CostEstimation(),
   177	                recomendacao_geral="Não foi possível processar a solicitação.",
   178	            ),
   179	            alertas=erros_validacao,
   180	        )
   181	
   182	    # 2. Construção do contexto
   183	    ctx = _construir_contexto(req, request_id)
   184	
   185	    # 3. Execução paralela dos agentes especialistas
   186	    resultados: dict[str, AgentResult] = {}
   187	    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
   188	        futures = {
   189	            "aereo": executor.submit(aereo.run, ctx),
   190	            "hotel": executor.submit(hotel.run, ctx),
   191	            "turismo": executor.submit(turismo.run, ctx),
   192	        }
   193	        for nome, future in futures.items():
   194	            try:
   195	                resultados[nome] = future.result(timeout=60)
   196	            except Exception as e:
   197	                resultados[nome] = AgentResult(
   198	                    agent_name=f"agente_{nome}",
   199	                    status="erro",
   200	                    data={},
   201	                    erros=[f"Agente {nome} falhou: {str(e)}"],
   202	                    alertas=[f"Resultado do agente_{nome} não disponível."],
   203	                )
   204	
   205	    # 4. Determinação do status geral
   206	    statuses = [r.status for r in resultados.values()]
   207	    if all(s == "sucesso" for s in statuses):
   208	        status_geral = "sucesso"
   209	    elif all(s == "erro" for s in statuses):
   210	        status_geral = "erro"
   211	    else:
   212	        status_geral = "parcial"
   213	
   214	    # 5. Estimativa de custos e recomendação
   215	    estimativa = _calcular_estimativa_custos(resultados["aereo"], resultados["hotel"])
   216	    recomendacao = _gerar_recomendacao_geral(ctx, resultados)
   217	
   218	    # 6. Consolidação dos alertas
   219	    alertas_globais = [
   220	        "⚠️ Preços de passagens variam rapidamente. Confirme antes de comprar.",
   221	        "⚠️ Tarifas de hotel dependem de disponibilidade. Reserve com antecedência.",
   222	        "⚠️ Horários de atrações turísticas podem variar. Consulte fontes oficiais.",
   223	    ]
   224	    for resultado in resultados.values():
   225	        alertas_globais.extend(resultado.alertas)
   226	
   227	    # 7. Resposta final
   228	    return TravelPlan(
   229	        request_id=request_id,
   230	        status=status_geral,
   231	        resumo={
   232	            "cidade_destino": ctx.cidade_destino,
   233	            "cidade_origem": ctx.cidade_origem,
   234	            "data_saida": str(ctx.data_saida),
   235	            "data_retorno": str(ctx.data_retorno),
   236	            "duracao_dias": ctx.quantidade_dias,
   237	            "quantidade_noites": ctx.quantidade_noites,
   238	        },
   239	        resultado={
   240	            "passagens_aereas": resultados["aereo"],
   241	            "hoteis": resultados["hotel"],
   242	            "roteiro_turistico": resultados["turismo"],
   243	        },
   244	        plano_integrado=IntegratedPlan(
   245	            estimativa_custos=estimativa,
   246	            recomendacao_geral=recomendacao,
   247	        ),
   248	        alertas=list(dict.fromkeys(alertas_globais)),  # deduplica mantendo ordem
   249	    )

```


**Tool Call: Read file `agents/aereo.py`**
Status: Completed

```my-travel-ai/agents/aereo.py
     1	"""
     2	agente_aereo.py — Agente especializado em busca e análise de passagens aéreas.
     3	
     4	Implementa a lógica de geração e ranking de opções de voos seguindo os contratos
     5	definidos em skill.md e plano.md. Suporta engine LLM (Google Gemini) e engine
     6	de heurística local como fallback.
     7	"""
     8	from datetime import date, timedelta, datetime
     9	from typing import List, Optional
    10	import os
    11	import json
    12	
    13	from models import TravelContext, AgentResult, FlightOption
    14	
    15	
    16	# ──────────────────────────────────────────────────────────────
    17	# Base de conhecimento para heurística local
    18	# ──────────────────────────────────────────────────────────────
    19	
    20	_CONHECIMENTO_AEREO = {
    21	    # destino -> lista de dados por rota popular
    22	    "lisboa": [
    23	        {"companhia": "TAP Air Portugal", "escalas": 0, "duracao": "9h00", "preco_base": 3200, "hub": "GRU"},
    24	        {"companhia": "LATAM Airlines", "escalas": 1, "duracao": "14h30", "preco_base": 2800, "hub": "GRU"},
    25	        {"companhia": "Iberia", "escalas": 1, "duracao": "15h00", "preco_base": 2600, "hub": "GRU"},
    26	        {"companhia": "Air Europa", "escalas": 1, "duracao": "16h00", "preco_base": 2400, "hub": "GRU"},
    27	    ],
    28	    "paris": [
    29	        {"companhia": "Air France", "escalas": 0, "duracao": "11h00", "preco_base": 3800, "hub": "GRU"},
    30	        {"companhia": "LATAM Airlines", "escalas": 1, "duracao": "15h00", "preco_base": 3200, "hub": "GRU"},
    31	        {"companhia": "Iberia", "escalas": 1, "duracao": "16h30", "preco_base": 3000, "hub": "GRU"},
    32	    ],
    33	    "nova york": [
    34	        {"companhia": "LATAM Airlines", "escalas": 0, "duracao": "10h00", "preco_base": 3500, "hub": "GRU"},
    35	        {"companhia": "American Airlines", "escalas": 0, "duracao": "10h30", "preco_base": 3600, "hub": "GRU"},
    36	        {"companhia": "Delta Airlines", "escalas": 1, "duracao": "14h00", "preco_base": 3100, "hub": "GRU"},
    37	    ],
    38	    "miami": [
    39	        {"companhia": "LATAM Airlines", "escalas": 0, "duracao": "7h30", "preco_base": 2200, "hub": "GRU"},
    40	        {"companhia": "American Airlines", "escalas": 0, "duracao": "8h00", "preco_base": 2400, "hub": "GRU"},
    41	        {"companhia": "Gol", "escalas": 0, "duracao": "8h30", "preco_base": 2100, "hub": "GRU"},
    42	    ],
    43	    "buenos aires": [
    44	        {"companhia": "LATAM Airlines", "escalas": 0, "duracao": "3h00", "preco_base": 900, "hub": "GRU"},
    45	        {"companhia": "Aerolíneas Argentinas", "escalas": 0, "duracao": "3h15", "preco_base": 850, "hub": "GRU"},
    46	        {"companhia": "Gol", "escalas": 0, "duracao": "3h30", "preco_base": 780, "hub": "GRU"},
    47	    ],
    48	    "cancún": [
    49	        {"companhia": "LATAM Airlines", "escalas": 1, "duracao": "9h00", "preco_base": 2800, "hub": "GRU"},
    50	        {"companhia": "Avianca", "escalas": 1, "duracao": "10h00", "preco_base": 2500, "hub": "GRU"},
    51	    ],
    52	    "roma": [
    53	        {"companhia": "Alitalia / ITA Airways", "escalas": 0, "duracao": "12h00", "preco_base": 3700, "hub": "GRU"},
    54	        {"companhia": "LATAM Airlines", "escalas": 1, "duracao": "16h00", "preco_base": 3200, "hub": "GRU"},
    55	        {"companhia": "Iberia", "escalas": 1, "duracao": "15h00", "preco_base": 3100, "hub": "GRU"},
    56	    ],
    57	    "default": [
    58	        {"companhia": "LATAM Airlines", "escalas": 1, "duracao": "12h00", "preco_base": 2500, "hub": "GRU"},
    59	        {"companhia": "Gol", "escalas": 1, "duracao": "13h00", "preco_base": 2200, "hub": "GRU"},
    60	        {"companhia": "Azul", "escalas": 1, "duracao": "11h30", "preco_base": 2300, "hub": "VCP"},
    61	    ],
    62	}
    63	
    64	_HUBS_POR_ORIGEM = {
    65	    "são paulo": "GRU",
    66	    "sao paulo": "GRU",
    67	    "rio de janeiro": "GIG",
    68	    "brasília": "BSB",
    69	    "brasilia": "BSB",
    70	    "teresina": "THE",
    71	    "fortaleza": "FOR",
    72	    "recife": "REC",
    73	    "salvador": "SSA",
    74	    "manaus": "MAO",
    75	    "porto alegre": "POA",
    76	    "curitiba": "CWB",
    77	    "belo horizonte": "CNF",
    78	    "default": "GRU",
    79	}
    80	

```


**Tool Call: 2 matches**
Status: Completed

file:///home/armando/Área de trabalho/TCA/my-travel-ai/static/index.js

file:///home/armando/Área de trabalho/TCA/my-travel-ai/tests/index.test.js

## Assistant

<thinking>
Now I have a good understanding of the project structure. Let me analyze what I've learned:

1. **Project Structure:**
   - FastAPI backend (`main.py`)
   - Frontend: `static/index.html` and `static/index.js`
   - Agents: `maestro.py`, `aereo.py`, `hotel.py`, `turismo.py` in `agents/` folder
   - Models: `models.py`

2. **Current Flow:**
   - User clicks "Planejar Viagem" button
   - Frontend sends request to `/api/plan`
   - `main.py` calls `maestro.run()` which orchestrates the agents
   - Agents run in parallel using ThreadPoolExecutor
   - Results are returned to frontend
   - Frontend shows "Agentes em Ação" section with agent cards showing status

3. **What needs to be done:**
   - Add logging to capture events from all agents (maestro, aereo, hotel, turismo)
   - Logs should appear in terminal (backend)
   - Create a new web panel in the UI below "Agentes em Ação" to show logs in real-time
   - Show operations status (success/failure) at the end

4. **Key considerations:**
   - The current implementation is synchronous (maestro.run() is called and waits for all agents)
   - For real-time updates, we'll need to use WebSockets or Server-Sent Events (SSE)
   - Or we could poll for status updates
   - The agents currently run in parallel using ThreadPoolExecutor

Let me read more of the frontend JavaScript to understand how the current UI updates work, and also check if there's any existing logging mechanism.

Actually, looking at the request again - the user wants me to create an implementation plan first, not implement it yet. So I should create a detailed plan.

Let me gather a bit more information about the frontend JavaScript to understand the current flow better.
</thinking>

Agora vamos ler o arquivo JavaScript do frontend para entender como a UI atualiza o status dos agentes:

**Tool Call: Read file `static/index.js`**
Status: Completed

```
SUCCESS: File outline retrieved. This file is too large to read all at once, so the outline below shows the file's structure with line numbers.

IMPORTANT: Do NOT retry this call without line numbers - you will get the same outline.
Instead, use the line numbers below to read specific sections by calling this tool again with start_line and end_line parameters.

# File outline for /home/armando/Área de trabalho/TCA/my-travel-ai/static/index.js

const form [L4]
const btnSubmit [L5]
const btnNewPlan [L6]
const btnRetry [L7]
const agentsSection [L9]
const resultsSection [L10]
const errorSection [L11]
const THEME_KEY [L14]
const themeToggle [L15]
const themeIcon [L16]
const THEMES [L19-22]
 dark [L20]
  icon [L20]
  label [L20]
 light [L21]
  icon [L21]
  label [L21]
function getPreferredTheme() [L24-39]
 const saved [L26]
function applyTheme( ) [L41-55]
function toggleTheme() [L57-61]
 const current [L58]
 const next [L59]
const initialTheme [L64]
const AGENT_STEPS [L86-117]
 id [L88]
 badge [L89]
 done [L90]
 delay [L91]
 id [L94]
 badge [L95]
 done [L96]
 delay [L97]
 id [L100]
 badge [L101]
 done [L102]
 delay [L103]
 id [L106]
 badge [L107]
 done [L108]
 delay [L109]
 id [L112]
 badge [L113]
 done [L114]
 delay [L115]
function setAgentStatus( ) [L119-125]
 const card [L120]
 const badge [L123]
function runAgentAnimation() [L127-137]
function finishAgentAnimation( ) [L139-156]
 const agentMap [L140-144]
  passagens_aereas [L141]
  hoteis [L142]
  roteiro_turistico [L143]
 const agentResult [L149]
 const status [L150]
 const badge [L151]
const target [L161]
function formatCurrency( ) [L177-184]
 style [L180]
 currency [L181]
 maximumFractionDigits [L182]
function renderSummary( ) [L186-237]
 const s [L187]
 const pi [L188]
 const statusBadge [L191]
 sucesso [L193]
 parcial [L193]
 erro [L193]
 const title [L199]
 const stats [L203]
 const dataIda [L204]
 const dataVolta [L205]
 const formatDate [L206-211]
  day [L208]
  month [L209]
  year [L210]
 const rec [L233]
function renderCosts( ) [L239-266]
 const ec [L240]
 const container [L241]
 const items [L242-252]
  icon [L243]
  label [L243]
  value [L243]
  icon [L244]
  label [L244]
  value [L244]
  icon [L245]
  label [L245]
  value [L245]
  icon [L247]
  label [L248]
  value [L249]
  highlight [L250]
function renderFlights( ) [L268-339]
 const container [L269]
 const opcoes [L275]
 const melhor [L276]
 const limitacoes [L277]
 const bestCompanhia [L284]
 const flightCards [L286-326]
  const isBest [L288]
  const escalasText [L289-294]
 const limitacoesHtml [L328-336]
function renderHotels( ) [L341-423]
 const container [L342]
 const opcoes [L348]
 const regioes [L349]
 const limitacoes [L350]
 const hotelCards [L352-395]
  const stars [L354]
  const starStr [L355]
  const ratingNum [L356]
  const ratingPct [L357]
  const highlightTags [L358-361]
 const regioesHtml [L397-406]
 const limitacoesHtml [L408-416]
function renderItinerary( ) [L425-505]
 const container [L426]
 const roteiro [L432]
 const dicas [L433]
 const timeIcons [L435]
  manha [L435]
  tarde [L435]
  noite [L435]
 const dayCards [L437-484]
  const dataObj [L439]
  const dateStr [L440-444]
   weekday [L441]
   day [L442]
   month [L443]
  const timeBlocks [L446-459]
   const activities [L448]
  const obsHtml [L461-465]
 const dicasHtml [L486-495]
 const firstDay [L503]
function renderAlerts( ) [L507-528]
 const container [L508]
 const allAlerts [L509]
 const agentAlerts [L512]
 const allUnique [L519]
const card [L532]
function showSection( ) [L537-544]
function hideAllSections() [L546-550]
function validateForm( ) [L553-595]
 let valid [L554]
const formData [L601]
const data [L603-613]
 cidade_destino [L604]
 data_saida [L605]
 data_retorno [L606]
 cidade_origem [L607]
 quantidade_viajantes [L608]
 ritmo_roteiro [L609]
 interesses [L610]
 preferencia_voo [L611]
 preferencia_hotel [L612]
behavior [L631]
block [L631]
const response [L634-638]
 method [L635]
 headers [L636]
  Content-Type [L636]
 body [L637]
const result [L640]
detail [L643]
behavior [L671]
block [L671]
const messages [L678]
let errs [L679]
behavior [L701]
block [L701]
behavior [L706]
block [L706]
const today [L711]
const dataSaida [L712]
const dataRetorno [L713]

Showing symbols 1-178 (total symbols: 178)


NEXT STEPS: To read a specific symbol's implementation, call read_file with the same path plus start_line and end_line from the outline above.
For example, to read a function shown as [L100-150], use start_line: 100 and end_line: 150.
```


**Tool Call: Read file `models.py`**
Status: Completed

```my-travel-ai/models.py
     1	from datetime import date, datetime
     2	from pydantic import BaseModel, Field
     3	from typing import List, Optional, Dict, Any
     4	
     5	class TravelPreferences(BaseModel):
     6	    quantidade_viajantes: int = Field(default=1, description="Número de passageiros")
     7	    quantidade_hospedes: int = Field(default=1, description="Número de hóspedes")
     8	    quantidade_quartos: int = Field(default=1, description="Número de quartos")
     9	    preferencia_voo: str = Field(default="melhor_custo_beneficio", description="Preferência de voo (ex: menor_preco, menor_duracao, melhor_custo_beneficio)")
    10	    preferencia_hotel: str = Field(default="melhor_custo_beneficio", description="Preferência de hotel")
    11	    categoria_hotel: Optional[str] = Field(default=None, description="Categoria do hotel (ex: 3 estrelas, 4 estrelas)")
    12	    ritmo_roteiro: str = Field(default="moderado", description="Ritmo do roteiro (ex: leve, moderado, intenso)")
    13	    interesses: List[str] = Field(default_factory=list, description="Lista de interesses (ex: historia, gastronomia, museus)")
    14	
    15	class TravelRequest(BaseModel):
    16	    cidade_destino: str = Field(..., description="Cidade de destino da viagem")
    17	    data_saida: date = Field(..., description="Data de início da viagem (check-in)")
    18	    data_retorno: date = Field(..., description="Data de retorno (check-out)")
    19	    cidade_origem: Optional[str] = Field(default=None, description="Cidade de origem da viagem")
    20	    preferencias: TravelPreferences = Field(default_factory=TravelPreferences, description="Preferências da viagem")
    21	
    22	class ExecutionMetadata(BaseModel):
    23	    idioma: str = Field(default="pt-BR")
    24	    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    25	
    26	class TravelContext(BaseModel):
    27	    request_id: str
    28	    cidade_destino: str
    29	    data_saida: date
    30	    data_retorno: date
    31	    cidade_origem: Optional[str] = None
    32	    quantidade_dias: int
    33	    quantidade_noites: int
    34	    preferencias: TravelPreferences
    35	    execucao: ExecutionMetadata
    36	
    37	class FlightOption(BaseModel):
    38	    companhia: str
    39	    origem: str
    40	    destino: str
    41	    data_ida: date
    42	    data_volta: date
    43	    preco_estimado: Optional[float] = None
    44	    moeda: Optional[str] = "BRL"
    45	    duracao_estimada: Optional[str] = None
    46	    escalas: Optional[int] = 0
    47	    link_consulta: Optional[str] = None
    48	    observacoes: Optional[str] = "Preço e disponibilidade devem ser confirmados."
    49	    score: Optional[float] = Field(default=0.0, description="Score calculado para ranking")
    50	
    51	class HotelOption(BaseModel):
    52	    nome: str
    53	    bairro: Optional[str] = None
    54	    categoria: Optional[str] = None
    55	    preco_estimado_total: Optional[float] = None
    56	    preco_estimado_diaria: Optional[float] = None
    57	    moeda: Optional[str] = "BRL"
    58	    avaliacao: Optional[str] = None
    59	    destaques: List[str] = Field(default_factory=list)
    60	    link_consulta: Optional[str] = None
    61	    observacoes: Optional[str] = "Tarifa e disponibilidade devem ser confirmadas."
    62	    score: Optional[float] = Field(default=0.0, description="Score calculado para ranking")
    63	
    64	class TouristAttraction(BaseModel):
    65	    nome: str
    66	    categoria: str
    67	    bairro: Optional[str] = None
    68	    tempo_estimado_visita: Optional[str] = None
    69	    prioridade: int
    70	    observacoes: List[str] = Field(default_factory=list)
    71	    score: Optional[float] = Field(default=0.0, description="Score calculado para ranking")
    72	
    73	class DailyItinerary(BaseModel):
    74	    dia: int
    75	    data: date
    76	    tema: str
    77	    manha: List[str] = Field(default_factory=list)
    78	    tarde: List[str] = Field(default_factory=list)
    79	    noite: List[str] = Field(default_factory=list)
    80	    observacoes: List[str] = Field(default_factory=list)
    81	
    82	class AgentResult(BaseModel):
    83	    agent_name: str
    84	    status: str  # sucesso, parcial, erro
    85	    data: Any
    86	    fontes: List[str] = Field(default_factory=list)
    87	    alertas: List[str] = Field(default_factory=list)
    88	    erros: List[str] = Field(default_factory=list)
    89	    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    90	
    91	class CostEstimation(BaseModel):
    92	    passagens: Optional[float] = None
    93	    hospedagem: Optional[float] = None
    94	    passeios: Optional[float] = None
    95	    total_estimado: Optional[float] = None
    96	    moeda: str = "BRL"
    97	
    98	class IntegratedPlan(BaseModel):
    99	    estimativa_custos: CostEstimation
   100	    recomendacao_geral: str

```


## Assistant

Agora tenho uma visão clara da arquitetura. O backend é FastAPI (Python) com agentes síncronos executados via `ThreadPoolExecutor`, e o frontend é HTML/JS estático. O fluxo atual é: o JS faz um POST para `/api/plan` e recebe a resposta final de uma vez — não há streaming.

Para criar o painel de logs em tempo real, precisamos adicionar **Server-Sent Events (SSE)** ou **WebSocket** no backend para emitir eventos/logs conforme os agentes executam, e no frontend consumir esses eventos para preencher o novo painel.

Aqui está o **Plano de Implementação** detalhado:

---

## 📋 Plano de Implementação — Painel de Logs em Tempo Real

### 1. Visão Geral da Arquitetura Proposta

```
┌─────────────┐     POST /api/plan      ┌──────────────────┐
│   Frontend  │ ──────────────────────► │  FastAPI Backend │
│   (HTML/JS) │                         │                  │
│             │ ◄──── GET /api/stream   │  Maestro Agent   │
│             │     (SSE / EventSource) │  Aereo Agent     │
│             │                         │  Hotel Agent     │
│             │                         │  Turismo Agent   │
└─────────────┘                         └──────────────────┘
```

### 2. Backend (Python / FastAPI)

#### 2.1. Criar um sistema de logging centralizado (`agents/logger.py`)
- Criar um `EventLogger` thread-safe que armazena eventos em uma fila (`queue.Queue`).
- Cada evento terá: `timestamp`, `agent` (maestro/aereo/hotel/turismo), `level` (info/success/warning/error), `message`.
- Fornecer funções auxiliares: `log_info(agent, msg)`, `log_success(agent, msg)`, `log_error(agent, msg)`.

#### 2.2. Instrumentar os agentes existentes
- Em `maestro.py`: adicionar logs no início (`"Maestro: validando request"`), antes de disparar agentes paralelos, e ao consolidar resultados.
- Em `aereo.py`, `hotel.py`, `turismo.py`: adicionar logs nos pontos-chave (início da busca, uso de LLM vs heurística, conclusão com status).
- **Importante**: manter a assinatura `run(ctx)` dos agentes inalterada; apenas injetar chamadas de log.

#### 2.3. Criar endpoint SSE no `main.py`
- `GET /api/stream/{request_id}` → retorna `StreamingResponse` com `text/event-stream`.
- O endpoint lê da fila do `EventLogger` e envia eventos JSON formatados como SSE (`data: {...}\n\n`).
- Usar um `request_id` único para correlacionar a requisição do plano com o stream de logs.
- O `EventLogger` deve manter um dicionário de filas por `request_id` e limpar após o término.

#### 2.4. Modificar o endpoint `POST /api/plan`
- Gerar um `request_id` antes de chamar `maestro.run()`.
- Executar o maestro em uma thread separada (já é feito via `ThreadPoolExecutor` internamente, mas agora precisamos que o endpoint retorne o `request_id` imediatamente para o frontend começar a consumir o SSE).
- O endpoint deve retornar: `{ "request_id": "...", "status": "processing" }` imediatamente, e o resultado final será enviado via SSE ou via um segundo GET.

> **Alternativa simplificada** (menos invasiva): manter o `POST /api/plan` síncrono, mas fazer o maestro emitir logs para uma fila global, e criar um endpoint SSE que o frontend abre **antes** de disparar o POST. O frontend faria: (1) abre SSE, (2) faz POST, (3) processa logs em tempo real, (4) ao receber evento `done`, faz GET para buscar o resultado final.

### 3. Frontend (HTML + JavaScript)

#### 3.1. Adicionar novo painel de logs no `index.html`
- Logo abaixo da seção `#agents-progress` (após a linha ~396), adicionar:
```html
<section id="logs-section" class="logs-section hidden">
  <div class="container">
    <h2 class="section-title">📋 Logs da Execução</h2>
    <div class="logs-container" id="logs-container">
      <!-- Logs aparecem aqui em tempo real -->
    </div>
    <div id="logs-summary" class="logs-summary hidden"></div>
  </div>
</section>
```
- Adicionar CSS no `index.html` (ou arquivo CSS separado) para estilizar o painel de logs (fundo escuro, fonte monoespaçada, cores por nível).

#### 3.2. Atualizar `index.js`
- Antes de fazer o POST para `/api/plan`, abrir um `EventSource` para `/api/stream/{request_id}`.
- Ao receber eventos SSE:
  - Criar um elemento `<div class="log-entry log-{level}">` com timestamp e mensagem.
  - Fazer scroll automático para o final do `#logs-container`.
- Ao receber evento `done` (ou `error`), mostrar o resumo final (todas as operações concluídas com sucesso ou não) na `#logs-summary`.
- Manter o comportamento original dos cartões de agentes ("Agentes em Ação") inalterado — o painel de logs é **adicional**.

### 4. Logs no Terminal (Backend)

- O `EventLogger` também deve chamar `print()` ou usar o módulo `logging` do Python para que os eventos apareçam no terminal onde o servidor FastAPI está rodando.
- Formato sugerido: `[2026-06-04 10:30:15] [MAESTRO] [INFO] Validando request...`

### 5. Ordem de Implementação Sugerida

| Passo | O que fazer | Arquivos |
|-------|-------------|----------|
| 1 | Criar `agents/logger.py` com `EventLogger` | Novo arquivo |
| 2 | Instrumentar `maestro.py` com logs | `agents/maestro.py` |
| 3 | Instrumentar `aereo.py`, `hotel.py`, `turismo.py` | `agents/aereo.py`, `hotel.py`, `turismo.py` |
| 4 | Adicionar endpoint SSE em `main.py` | `main.py` |
| 5 | Adicionar painel HTML de logs | `static/index.html` |
| 6 | Atualizar JS para consumir SSE e renderizar logs | `static/index.js` |
| 7 | Testar fluxo completo (terminal + UI) | — |

### 6. Considerações Importantes

- ✅ **Manter todas as funcionalidades originais**: o painel "Agentes em Ação" continua funcionando exatamente como hoje.
- ✅ **Não quebrar a API atual**: o `POST /api/plan` pode continuar retornando o plano final (ou ser adaptado conforme a estratégia escolhida).
- ✅ **Thread-safety**: o `EventLogger` deve usar `queue.Queue` ou locks, pois os agentes rodam em threads do `ThreadPoolExecutor`.
- ⚠️ **Limpeza de memória**: remover filas de `request_id` antigos após o término da execução para evitar vazamento de memória.

---

Este é o plano completo. Quer que eu comece a implementar a partir do **Passo 1** (criar o `agents/logger.py`) ou prefere ajustar algo no plano?
