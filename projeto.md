# 📋 Documentação Técnica de Software
## Projeto: my-travel-ai
**Repositório:** https://github.com/armandossrecife/my-travel-ai  
**Versão do Documento:** 1.2.0  
**Última Atualização:** Junho 2026  
**Classificação:** Protótipo Acadêmico/Técnico

**Autor:**: Armando Soares Sousa

**IA**: Apoio de documentação via GPT 5.5 e Qwen 3.6

---

## 📑 Índice

1. [Visão Geral do Projeto](#1-visão-geral-do-projeto)
2. [Arquitetura do Sistema](#2-arquitetura-do-sistema)
3. [Estrutura do Código](#3-estrutura-do-código)
4. [Componentes Principais](#4-componentes-principais)
5. [Modelos de Dados](#5-modelos-de-dados)
6. [API REST](#6-api-rest)
7. [Estratégia de IA Generativa](#7-estratégia-de-ia-generativa)
8. [Frontend](#8-frontend)
9. [Testes e Qualidade](#9-testes-e-qualidade)
10. [Segurança e Privacidade](#10-segurança-e-privacidade)
11. [Operação e Observabilidade](#11-operação-e-observabilidade)
12. [Guia de Desenvolvimento](#12-guia-de-desenvolvimento)
13. [Roadmap de Evolução](#13-roadmap-de-evolução)
14. [Referências e Recursos](#14-referências-e-recursos)

---

## 1. Visão Geral do Projeto

### 1.1 Propósito
O `my-travel-ai` é um protótipo de aplicação web para **planejamento inteligente de viagens** baseado em arquitetura multiagente. O sistema recebe dados básicos de uma viagem e gera um plano consolidado contendo:

- ✈️ Sugestões de passagens aéreas
- 🏨 Opções de hospedagem
- 🗺️ Roteiro turístico diário
- 💰 Estimativa de custos
- ⚠️ Alertas de confirmação

### 1.2 Escopo e Limitações Importantes

| Característica | Status | Observação |
|---------------|--------|-----------|
| Consultas a APIs reais de voos | ❌ Não implementado | Usa heurística local ou LLM |
| Consultas a APIs de hotéis | ❌ Não implementado | Dados simulados |
| Validação de disponibilidade | ❌ Não implementado | Estimativas apenas |
| Persistência de dados | ❌ Não implementado | Sem banco de dados |
| Autenticação de usuários | ❌ Não implementado | Acesso aberto |
| **Arquitetura multiagente** | ✅ Implementado | Orquestrador + 3 especialistas |
| **Integração opcional com LLM** | ✅ Implementado | Google Gemini via env var |
| **Testes automatizados** | ✅ Implementado | 123 testes passando |
| **Interface web funcional** | ✅ Implementado | Frontend estático |

> ⚠️ **AVISO CRÍTICO**: Esta aplicação é um **demonstrador de arquitetura**, não um produto para reservas reais. Todos os preços e disponibilidades são estimativas que devem ser confirmadas em fontes oficiais.

### 1.3 Stack Tecnológico

```yaml
Backend:
  - Python 3.10+
  - FastAPI 0.110+
  - Pydantic 2.6+
  - Uvicorn (ASGI server)
  - concurrent.futures (paralelismo)

Frontend:
  - HTML5, CSS3, JavaScript (Vanilla)
  - Glassmorphism UI design
  - Fetch API para comunicação com backend

IA/ML:
  - Google Gemini (opcional, via GEMINI_API_KEY)
  - Heurística local como fallback

DevOps:
  - pytest (testes backend, frontend e integração)
  - requirements.txt (dependências)
  - run.sh (script de inicialização)
```

---

## 2. Arquitetura do Sistema

### 2.1 Diagrama de Camadas

```
┌─────────────────────────────────────┐
│         CAMADA DE APRESENTAÇÃO      │
│  ┌─────────────────────────────┐    │
│  │  static/index.html          │    │
│  │  static/index.css           │    │
│  │  static/index.js            │    │
│  └─────────────────────────────┘    │
└────────────┬────────────────────────┘
             │ HTTP/JSON
             ▼
┌─────────────────────────────────────┐
│         CAMADA DE API (FastAPI)     │
│  ┌─────────────────────────────┐    │
│  │  app/main.py                │    │
│  │  app/api/routes/*.py        │    │
│  │  • GET  /api/health         │    │
│  │  • POST /api/plan           │    │
│  │  • GET  /api/stream/{id}    │    │
│  │  • GET  /api/result/{id}    │    │
│  │  • GET  / (frontend)        │    │
│  └─────────────────────────────┘    │
└────────────┬────────────────────────┘
             │ Modelos Pydantic
             ▼
┌─────────────────────────────────────┐
│      CAMADA DE DOMÍNIO/CONTRATOS    │
│  ┌─────────────────────────────┐    │
│  │  app/api/schemas.py         │    │
│  │  app/models/travel.py       │    │
│  │  • TravelRequest            │    │
│  │  • TravelContext            │    │
│  │  • TravelPlan               │    │
│  │  • FlightOption, etc.       │    │
│  └─────────────────────────────┘    │
└────────────┬────────────────────────┘
             │ Contexto enriquecido
             ▼
┌──────────────────────────────────────┐
│      CAMADA DE AGENTES (Orquestração)│
│  ┌──────────────────────────────┐    │
│  │  app/agents/maestro.py       │    │
│  │  • Validação de entrada      │    │
│  │  • Execução paralela         │    │
│  │  • Consolidação de resultados│    │
│  └──────────────────────────────┘    │
└────┬──────────┬──────────┬───────────┘
     │          │          │
     ▼          ▼          ▼
┌────────┐┌────────┐┌────────┐
│aereo.py││hotel.py││turismo │
│        ││        ││.py     │
└────────┘└────────┘└────────┘
     │          │          │
     ▼          ▼          ▼
┌─────────────────────────────────────┐
│   CAMADA DE IA/HEURÍSTICA           │
│  • Base de conhecimento local       │
│  • Integração opcional com Gemini   │
│  • Fallback automático              │
└─────────────────────────────────────┘
```

### 2.2 Padrão Multiagente: Orquestrador-Especialistas

```python
# Fluxo lógico simplificado
Usuario → Frontend → POST /api/plan
                    ↓
              FastAPI (app.main:app)
                    ↓
              PlanRequest (app/api/schemas.py)
                    ↓
              TravelRequest (Pydantic)
                    ↓
              Background job + request_id
                    ↓
              maestro.run(request_id=...)
                    ├─▶ app.agents.aereo.run() ──▶ FlightOption[]
                    ├─▶ app.agents.hotel.run() ──▶ HotelOption[]
                    └─▶ app.agents.turismo.run() ─▶ DailyItinerary[]
                    ↓
              Consolidação + Cálculo de custos
                    ↓
              TravelPlan em memória
                    ↓
              SSE (/api/stream/{id}) + /api/result/{id}
                    ↓
              Frontend (logs + renderização em abas)
```

**Características do padrão:**
- ✅ Execução paralela via `ThreadPoolExecutor` (3 workers)
- ✅ Tratamento de falhas parciais (um agente falhar não quebra o fluxo)
- ✅ Status granular: `sucesso`, `parcial`, `erro`
- ✅ Timeout configurável por agente (60s padrão)
- ✅ Consolidação centralizada de alertas e recomendações
- ✅ Progresso em tempo real via Server-Sent Events (SSE)

---

## 3. Estrutura do Código

```
my-travel-ai/
├── 📄 README.md                    # Documentação de alto nível
├── 📄 requirements.txt             # Dependências Python
├── 📄 run.sh                       # Script de inicialização
│
├── 📁 app/                         # Código da aplicação
│   ├── 📄 __init__.py
│   ├── 📄 main.py                  # Factory FastAPI e app.main:app
│   ├── 📁 api/
│   │   ├── 📄 schemas.py           # Schemas da API (PlanRequest)
│   │   └── 📁 routes/
│   │       ├── 📄 health.py        # GET /api/health
│   │       ├── 📄 plan.py          # POST /api/plan
│   │       ├── 📄 stream.py        # GET /api/stream/{request_id}
│   │       └── 📄 result.py        # GET /api/result/{request_id}
│   ├── 📁 models/
│   │   └── 📄 travel.py            # Contratos Pydantic de domínio
│   ├── 📁 agents/
│   │   ├── 📄 maestro.py           # Orquestrador principal
│   │   ├── 📄 aereo.py             # Agente de passagens aéreas
│   │   ├── 📄 hotel.py             # Agente de hospedagem
│   │   ├── 📄 turismo.py           # Agente de roteiro turístico
│   │   ├── 📄 logger.py            # Eventos em memória para SSE
│   │   ├── 📄 base_local.py        # Bases locais de conhecimento
│   │   └── 📄 config.py            # Configurações de agentes/LLM
│   ├── 📁 services/
│   │   └── 📄 planning_jobs.py     # Jobs em background + results_store
│   └── 📁 ui/
│       └── 📄 static.py            # Montagem de / e /static
│
├── 📁 static/                      # Frontend estático
│   ├── 📄 index.html              # Interface principal
│   ├── 📄 index.css               # Estilos (Glassmorphism)
│   ├── 📄 index_corrected.css     # Correções/variações de estilo
│   └── 📄 index.js                # Lógica frontend + fetch API
│
├── 📁 tests/                       # Suíte de testes automatizados
│   ├── 📁 backend/                # API, modelos e agentes
│   ├── 📁 frontend/               # HTML, CSS e funções JS
│   ├── 📁 integration/            # Fluxos completos e SSE
│   └── 📄 run_tests.sh            # Runner da suíte
│
├── 📁 skills/                      # Documentação de habilidades dos agentes
│   └── 📄 skill.md                # Especificação comportamental
│
├── 📁 planos/                      # Documentação de planejamento
│   ├── 📄 README.md
│   ├── 📄 plano.md
│   ├── 📄 plano_implementacao.md
│   ├── 📄 prompt.md
│   └── 📄 tarefas_plano_implementacao.md
│
├── 📁 docs/                        # Assets de documentação
│   ├── 📁 servicos/
│   │   └── 🖼️ API_Servicos.png
│   └── 📁 telas/
│       └── 🖼️ T01.png ... T08.png
│
└── 📄 .gitignore                   # Arquivos ignorados pelo Git
```

### 3.1 Arquivos para Limpeza Pré-Deploy

```bash
# Remover antes de versionamento ou distribuição:
rm -rf __MACOSX/ ._* __pycache__/ .pytest_cache/ .DS_Store
```

---

## 4. Componentes Principais

### 4.1 `app/main.py` e `app/api/routes/*` — API e Ponto de Entrada

**Responsabilidades:**
- `app/main.py`: criar a aplicação FastAPI, incluir routers e montar a UI estática
- `app/api/schemas.py`: definir `PlanRequest`
- `app/api/routes/health.py`: expor status da API
- `app/api/routes/plan.py`: validar entrada, converter para `TravelRequest` e iniciar job em background
- `app/api/routes/stream.py`: transmitir progresso em tempo real via SSE
- `app/api/routes/result.py`: consultar resultado final por `request_id`
- `app/ui/static.py`: servir `static/index.html` e arquivos de `/static`

**Endpoints:**

| Método | Rota | Descrição | Request | Response |
|--------|------|-----------|---------|----------|
| `GET` | `/api/health` | Health check da API | - | `{"status": "ok", "llm_enabled": bool}` |
| `POST` | `/api/plan` | Iniciar geração de plano | `PlanRequest` | `{"request_id": "...", "status": "processing"}` |
| `GET` | `/api/stream/{request_id}` | Acompanhar progresso via SSE | - | Eventos `data: {...}` |
| `GET` | `/api/result/{request_id}` | Consultar resultado final | - | `{"status": "processing"}` ou `TravelPlan` |
| `GET` | `/` | Servir frontend | - | `index.html` |

**Código-chave:**
```python
@router.post("/api/plan")
async def generate_travel_plan(request: PlanRequest):
    # 1. Converter PlanRequest → TravelRequest
    travel_req = TravelRequest(
        cidade_destino=request.cidade_destino,
        # ... mapeamento de campos
    )
    
    # 2. Criar fila de eventos e iniciar execução em background
    request_id = str(uuid.uuid4())
    event_logger.create_queue(request_id)
    thread = threading.Thread(
        target=run_maestro_background,
        args=(request_id, travel_req),
    )
    thread.start()
    
    # 3. Retornar identificador para SSE/polling
    return {"request_id": request_id, "status": "processing"}
```

**Pontos de Atenção para Manutenção:**
- ⚠️ Sem middleware CORS configurado (necessário para frontend separado)
- ⚠️ Sem autenticação/rate limiting (risco de abuso em produção)
- ⚠️ Erros expõem `str(e)` — sanitizar para produção
- ⚠️ `results_store` é em memória; reiniciar o servidor apaga resultados

---

### 4.2 `app/api/schemas.py` e `app/models/travel.py` — Modelagem de Domínio com Pydantic

**Contratos Principais:**

```python
# Entrada da API (app/api/schemas.py)
class PlanRequest(BaseModel):
    cidade_destino: str = Field(...)
    data_saida: date = Field(...)
    data_retorno: date = Field(...)
    cidade_origem: Optional[str] = None
    quantidade_viajantes: int = Field(default=1, ge=1)
    preferencia_voo: str = Field(default="melhor_custo_beneficio")
    preferencia_hotel: str = Field(default="melhor_custo_beneficio")
    categoria_hotel: Optional[str] = None
    ritmo_roteiro: str = Field(default="moderado")  # leve | moderado | intenso
    interesses: List[str] = Field(default_factory=list)

# Modelo interno de domínio (app/models/travel.py)
class TravelRequest(BaseModel):
    cidade_destino: str
    data_saida: date
    data_retorno: date
    cidade_origem: Optional[str]
    preferencias: TravelPreferences

# Contexto enriquecido para agentes
class TravelContext(BaseModel):
    request_id: str                    # UUID único
    cidade_destino: str                # Normalizado (.title())
    data_saida: date
    data_retorno: date
    quantidade_dias: int               # Calculado
    quantidade_noites: int             # Calculado
    preferencias: TravelPreferences
    execucao: ExecutionMetadata

# Resultado consolidado
class TravelPlan(BaseModel):
    request_id: str
    status: Literal["sucesso", "parcial", "erro"]  # ⚠️ Atualizar para Enum
    resumo: Dict[str, Any]
    resultado: Dict[str, AgentResult]  # Chaves: "passagens_aereas", "hoteis", "roteiro_turistico"
    plano_integrado: IntegratedPlan
    alertas: List[str]
    fontes: List[str]
    timestamp: str
```

**Modelos de Entidade:**

| Classe | Propósito | Campos Principais |
|--------|-----------|------------------|
| `FlightOption` | Representa uma opção de voo | `companhia`, `preco_estimado`, `duracao_estimada`, `escalas`, `score` |
| `HotelOption` | Representa uma opção de hotel | `nome`, `bairro`, `categoria`, `preco_estimado_total`, `avaliacao`, `score` |
| `TouristAttraction` | Ponto turístico | `nome`, `categoria`, `bairro`, `tempo_estimado_visita`, `prioridade` |
| `DailyItinerary` | Roteiro de um dia | `dia`, `data`, `tema`, `manha/tarde/noite` (listas), `observacoes` |
| `AgentResult` | Resultado padronizado de agente | `agent_name`, `status`, `data`, `fontes`, `alertas`, `erros` |
| `CostEstimation` | Estimativa financeira | `passagens`, `hospedagem`, `passeios`, `total_estimado`, `moeda` |

**Melhorias Recomendadas:**
```python
# 1. Usar Enum para campos com valores fixos
from enum import Enum

class StatusAgente(str, Enum):
    SUCESSO = "sucesso"
    PARCIAL = "parcial"
    ERRO = "erro"

class RitmoRoteiro(str, Enum):
    LEVE = "leve"
    MODERADO = "moderado"
    INTENSO = "intenso"

# 2. Tipagem específica para AgentResult.data
class FlightAgentData(BaseModel):
    opcoes: List[FlightOption]
    melhor_opcao_sugerida: Optional[Dict]
    limitacoes: List[str]

# 3. Validação semântica adicional
@field_validator('data_retorno')
def validar_data_retorno(cls, v, info):
    if v <= info.data['data_saida']:
        raise ValueError('data_retorno deve ser posterior a data_saida')
    return v
```

---

### 4.3 `app/agents/maestro.py` — Orquestrador Principal

**Fluxo de Execução:**

```mermaid
graph TD
    A[Recebe TravelRequest] --> B[Gerar request_id UUID]
    B --> C[Validar campos obrigatórios]
    C --> D{Validação OK?}
    D -->|Não| E[Retornar TravelPlan com status=erro]
    D -->|Sim| F[Construir TravelContext enriquecido]
    F --> G[ThreadPoolExecutor: 3 workers]
    G --> H[app.agents.aereo.run(ctx)]
    G --> I[app.agents.hotel.run(ctx)]
    G --> J[app.agents.turismo.run(ctx)]
    H --> K[Aguardar resultados com timeout=60s]
    I --> K
    J --> K
    K --> L[Tratar falhas individuais]
    L --> M[Calcular estimativa de custos]
    M --> N[Gerar recomendação geral]
    N --> O[Consolidar alertas globais]
    O --> P[Retornar TravelPlan consolidado]
```

**Funções Principais:**

| Função | Responsabilidade | Retorno |
|--------|-----------------|---------|
| `_validar_request(req)` | Valida campos obrigatórios e consistência de datas | `List[str]` de erros |
| `_construir_contexto(req, request_id)` | Transforma `TravelRequest` em `TravelContext` com cálculos | `TravelContext` |
| `_calcular_estimativa_custos()` | Calcula custos totais a partir dos melhores resultados | `CostEstimation` |
| `_gerar_recomendacao_geral()` | Gera texto descritivo consolidado | `str` |
| `run(req)` | **Ponto de entrada**: orquestra todo o fluxo | `TravelPlan` |

**Lógica de Consolidação de Custos:**
```python
def _calcular_estimativa_custos(resultado_aereo, resultado_hotel) -> CostEstimation:
    # Extrai melhor opção de cada agente pelo score
    melhor_voo = max(opcoes, key=lambda x: x.get("score", 0))
    melhor_hotel = max(opcoes, key=lambda x: x.get("score", 0))
    
    # Calcula passeios como 20% do subtotal
    subtotal = (melhor_voo.preco_estimado or 0) + (melhor_hotel.preco_estimado_total or 0)
    passeios = round(subtotal * 0.20, 2)
    total = round(subtotal + passeios, 2)
    
    return CostEstimation(
        passagens=melhor_voo.preco_estimado,
        hospedagem=melhor_hotel.preco_estimado_total,
        passeios=passeios,
        total_estimado=total,
        moeda="BRL"
    )
```

**Pontos de Melhoria:**
- ⚠️ `future.result(timeout=60)` é chamada sequencialmente; usar `as_completed()` para processar conforme terminam
- ⚠️ Fórmula de score não é transparente para o usuário final
- ⚠️ Sem métricas de tempo de execução por agente
- ⚠️ Dependência implícita na estrutura de `AgentResult.data` (frágil a mudanças)

---

### 4.4 `app/agents/aereo.py` — Agente de Passagens Aéreas

**Base de Conhecimento Local:**
```python
_CONHECIMENTO_AEREO = {
    "lisboa": [
        {"companhia": "TAP Air Portugal", "escalas": 0, "duracao": "9h00", "preco_base": 3200, "hub": "GRU"},
        {"companhia": "LATAM Airlines", "escalas": 1, "duracao": "14h30", "preco_base": 2800, "hub": "GRU"},
        # ... mais opções
    ],
    # ... outros destinos: paris, nova york, miami, buenos aires, cancún, roma
    "default": [...]  # Fallback para destinos não mapeados
}
```

**Algoritmo de Score de Voo:**
```python
def _calcular_score_voo(voo: dict) -> float:
    # Pesos definidos em skill.md
    peso_preco = 0.40
    peso_duracao = 0.25
    peso_escalas = 0.20
    peso_confianca = 0.15
    
    nota_escalas = 1 - (voo["escalas"] / 3)  # 0-3 escalas
    nota_preco = 1 - ((preco - preco_min) / (preco_max - preco_min))
    nota_duracao = max(0, 1 - (duracao_horas / 24))
    nota_confianca = 0.8  # Fonte heurística
    
    return round(
        peso_preco * nota_preco +
        peso_duracao * nota_duracao +
        peso_escalas * nota_escalas +
        peso_confianca * nota_confianca,
        4
    )
```

**Integração com LLM (Google Gemini):**
```python
def _gerar_opcoes_llm(ctx: TravelContext) -> List[FlightOption]:
    # Prompt estruturado solicitando JSON array
    prompt = f"""Você é o agente_aereo...
    Gere uma lista JSON de exatamente 3 opções...
    Responda SOMENTE com um JSON array, sem markdown...
    """
    
response = client.models.generate_content(model="gemini-3.1-flash-lite", contents=prompt)
    
    # Parsing resiliente de JSON
    raw = response.text.strip()
    if raw.startswith("```"):  # Remove markdown
        raw = raw.split("```")[1]
    if raw.startswith("json"):
        raw = raw[4:]
    
    data = json.loads(raw)
    return [FlightOption(**item) for item in data]
```

**Fallback Automático:**
```python
def run(ctx: TravelContext) -> AgentResult:
    try:
        use_llm = bool(os.environ.get("GEMINI_API_KEY", ""))
        opcoes = _gerar_opcoes_llm(ctx) if use_llm else _gerar_opcoes_heuristica(ctx)
        # ... processamento
    except Exception as e:
        # Fallback para heurística em caso de falha do LLM
        print(f"[agente_aereo] LLM falhou: {e}. Usando heurística local.")
        return _gerar_opcoes_heuristica(ctx)
```

**Destinos Suportados na Heurística:**
- Lisboa, Paris, Nova York, Miami, Buenos Aires, Cancún, Roma
- Qualquer outro destino usa base `default`

---

### 4.5 `app/agents/hotel.py` — Agente de Hospedagem

**Estrutura da Base de Conhecimento:**
```python
_CONHECIMENTO_HOTEL = {
    "lisboa": {
        "regioes_recomendadas": ["Baixa-Chiado", "Belém", "Alfama", ...],
        "hoteis": [
            {
                "nome": "Hotel Altis Belém",
                "bairro": "Belém",
                "categoria": "5 estrelas",
                "preco_diaria": 650,
                "avaliacao": "9.2/10",
                "destaques": ["Piscina", "Vista para o Tejo", "Spa"]
            },
            # ... mais hotéis
        ]
    },
    # ... outros destinos
}
```

**Cálculo de Score de Hotel:**
```python
def _calcular_score_hotel(hotel: dict, ctx: TravelContext) -> float:
    # Fatores considerados:
    # - Localização (bairro recomendado?)
    # - Avaliação (normalizada 0-1)
    # - Preço (invertido: menor = melhor)
    # - Comodidades (quantidade de destaques)
    
    peso_localizacao = 0.35
    peso_avaliacao = 0.30
    peso_preco = 0.25
    peso_comodidades = 0.10
    
    # ... cálculos de normalização
    return round(score_final, 4)
```

**Particularidades:**
- Calcula `preco_estimado_total = preco_diaria * quantidade_noites`
- Recomenda regiões/bairros baseado em conhecimento local
- Inclui alertas sobre taxas locais e políticas de cancelamento

---

### 4.6 `app/agents/turismo.py` — Agente de Roteiro Turístico

**Base de Pontos Turísticos:**
```python
_PONTOS_TURISTICOS = {
    "lisboa": [
        {"nome": "Torre de Belém", "categoria": "histórico", "bairro": "Belém", 
         "tempo": "1h30", "prioridade": 1},
        {"nome": "Mosteiro dos Jerónimos", "categoria": "histórico", "bairro": "Belém", 
         "tempo": "2h00", "prioridade": 2},
        # ... 8+ atrações
    ],
    # ... outros destinos
}
```

**Algoritmo de Distribuição de Roteiro:**
```python
def _gerar_rota_heuristica(ctx: TravelContext) -> dict:
    # 1. Ordena atrações por prioridade
    # 2. Reserva Dia 1 para chegada (agenda leve)
    # 3. Reserva último dia para retorno
    # 4. Distribui atrações nos dias intermediários conforme ritmo:
    #    - leve: 1 atração/dia
    #    - moderado: 2 atrações/dia
    #    - intenso: 3 atrações/dia
    # 5. Agrupa atrações por proximidade geográfica (bairro)
    # 6. Adiciona observações práticas por destino
```

**Dicas Contextuais:**
```python
_DICAS_GERAIS = {
    "lisboa": [
        "🚊 Use o Passe Lisboa para metrô, eléctrico e ônibus.",
        "🍽️ Almoce entre 12h-14h para evitar filas.",
        "🎭 Reserve ingressos do Mosteiro dos Jerónimos com antecedência.",
        # ...
    ],
    # ... outros destinos
}
```

---

## 5. Modelos de Dados — Referência Completa

### 5.1 Diagrama de Classes (Simplificado)

```
TravelRequest
├─ cidade_destino: str
├─ data_saida: date
├─ data_retorno: date
├─ cidade_origem: Optional[str]
└─ preferencias: TravelPreferences

TravelPreferences
├─ quantidade_viajantes: int
├─ quantidade_hospedes: int
├─ quantidade_quartos: int
├─ preferencia_voo: str  # "melhor_custo_beneficio" | "menor_preco" | "menor_duracao"
├─ preferencia_hotel: str
├─ categoria_hotel: Optional[str]
├─ ritmo_roteiro: str    # "leve" | "moderado" | "intenso"
└─ interesses: List[str]

TravelContext (enriquecido)
├─ request_id: str  # UUID
├─ quantidade_dias: int  # calculado
├─ quantidade_noites: int  # calculado
└─ execucao: ExecutionMetadata

AgentResult (padrão de retorno)
├─ agent_name: str
├─ status: str  # "sucesso" | "parcial" | "erro"
├─ data: Dict  # Estrutura específica por agente
├─ fontes: List[str]
├─ alertas: List[str]
└─ erros: List[str]

TravelPlan (resposta final)
├─ request_id: str
├─ status: str
├─ resumo: Dict
├─ resultado: Dict[str, AgentResult]
├─ plano_integrado: IntegratedPlan
├─ alertas: List[str]
└─ timestamp: str
```

### 5.2 Exemplo de Payload de Resposta

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "sucesso",
  "resumo": {
    "cidade_destino": "Lisboa",
    "cidade_origem": "Teresina",
    "data_saida": "2026-07-10",
    "data_retorno": "2026-07-17",
    "duracao_dias": 8,
    "quantidade_noites": 7
  },
  "resultado": {
    "passagens_aereas": {
      "agent_name": "agente_aereo",
      "status": "sucesso",
      "data": {
        "opcoes": [...],
        "melhor_opcao_sugerida": {
          "companhia": "Air Europa",
          "preco_estimado": 3000.00,
          "duracao_estimada": "16h00",
          "escalas": 1
        }
      },
      "fontes": ["Heurística local"],
      "alertas": ["⚠️ Valores são estimativas..."]
    },
    "hoteis": { ... },
    "roteiro_turistico": { ... }
  },
  "plano_integrado": {
    "estimativa_custos": {
      "passagens": 3000.00,
      "hospedagem": 2548.00,
      "passeios": 1109.60,
      "total_estimado": 6657.60,
      "moeda": "BRL"
    },
    "recomendacao_geral": "✈️ Sua viagem de Teresina para **Lisboa** foi planejada com sucesso!..."
  },
  "alertas": [
    "⚠️ Preços de passagens variam rapidamente. Confirme antes de comprar.",
    "⚠️ Tarifas de hotel dependem de disponibilidade. Reserve com antecedência."
  ],
  "fontes": ["Heurística local"],
  "timestamp": "2026-05-31T14:30:00"
}
```

---

## 6. API REST — Especificação Detalhada

### 6.1 Health Check

```http
GET /api/health
```

**Resposta de Sucesso (200 OK):**
```json
{
  "status": "ok",
  "service": "Travel Planner Multiagent API",
  "version": "1.0.0",
  "llm_enabled": false,
  "active_logs": 0
}
```

**Campos:**
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `status` | string | Sempre `"ok"` se a API estiver operacional |
| `service` | string | Nome do serviço |
| `version` | string | Versão da API |
| `llm_enabled` | boolean | `true` se `GEMINI_API_KEY` estiver configurada |
| `active_logs` | integer | Quantidade de filas SSE ativas em memória |

### 6.2 Gerar Plano de Viagem

```http
POST /api/plan
Content-Type: application/json
```

**Request Body (`PlanRequest`):**
```json
{
  "cidade_destino": "Lisboa",
  "data_saida": "2026-07-10",
  "data_retorno": "2026-07-17",
  "cidade_origem": "Teresina",
  "quantidade_viajantes": 2,
  "preferencia_voo": "melhor_custo_beneficio",
  "preferencia_hotel": "melhor_custo_beneficio",
  "categoria_hotel": "4 estrelas",
  "ritmo_roteiro": "moderado",
  "interesses": ["história", "gastronomia", "museus"]
}
```

**Validações Automáticas (Pydantic):**
- `cidade_destino`: obrigatório, não vazio
- `data_saida`/`data_retorno`: obrigatórios, formato ISO 8601
- `quantidade_viajantes >= 1`: restrição mínima

**Validações de Domínio (Maestro):**
- `data_retorno > data_saida`
- viagem com pelo menos 1 noite
- normalização de cidade de destino/origem antes de executar agentes

**Resposta de Sucesso (200 OK):**
```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "message": "Processamento iniciado. Use GET /api/stream/550e8400-e29b-41d4-a716-446655440000 para acompanhar."
}
```

O `TravelPlan` final fica disponível via SSE em `/api/stream/{request_id}` ou por polling em `/api/result/{request_id}`.

**Respostas de Erro:**

| Status | Cenário | Exemplo de `detail` |
|--------|---------|-------------------|
| `422` | Validação Pydantic falhou | Resposta padrão do FastAPI |
| `500` | Erro interno não tratado | `{"detail": "Traceback da exceção..."}` ⚠️ sanitizar em produção |

### 6.3 Streaming de Logs e Resultado

```http
GET /api/stream/{request_id}
Accept: text/event-stream
```

Eventos normais:
```text
data: {"timestamp":"2026-06-05T19:55:01","agent":"aereo","level":"info","message":"Iniciando busca de voos para Lisboa"}
```

Evento final:
```text
data: {"event":"done","result":{...TravelPlan...}}
```

Consulta direta do resultado:
```http
GET /api/result/{request_id}
```

Enquanto o processamento não terminou:
```json
{"status": "processing"}
```

Após a conclusão: `TravelPlan` completo (ver seção 5.2).

### 6.4 Documentação Automática

Acesse em execução:
- 📚 **Swagger UI**: `http://127.0.0.1:8000/docs`
- 📖 **ReDoc**: `http://127.0.0.1:8000/redoc`

---

## 7. Estratégia de IA Generativa

### 7.1 Arquitetura Híbrida: Heurística + LLM

```
┌─────────────────────────────────┐
│  Decisão: Usar LLM?             │
│  if GEMINI_API_KEY configurada: │
│    └─▶ Tentar geração via Gemini│
│        ├─▶ Sucesso: parse JSON  │
│        └─▶ Falha: fallback      │
│  else:                          │
│    └─▶ Usar heurística local    │
└─────────────────────────────────┘
```

### 7.2 Prompt Engineering por Agente

**Padrão Comum:**
1. Definir papel do agente ("Você é o agente_X, especialista em...")
2. Injetar contexto da viagem estruturado
3. Solicitar saída em JSON puro (sem markdown)
4. Especificar schema exato de resposta
5. Incluir regras de validação semântica

**Exemplo (Agente Aéreo):**
```python
prompt = f"""Você é o agente_aereo, especialista em passagens aéreas.

Dados da viagem:
- Cidade origem: {ctx.cidade_origem or 'Não informada'}
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
    "preco_estimado": 3000.00,
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
```

### 7.3 Parsing Resiliente de JSON do LLM

```python
def _parse_json_llm(raw_response: str) -> dict:
    raw = raw_response.strip()
    
    # Remove blocos markdown ```json ... ```
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1] if len(parts) > 1 else raw
    
    # Remove prefixo "json" se presente
    if raw.lower().startswith("json"):
        raw = raw[4:].strip()
    
    return json.loads(raw)
```

### 7.4 Riscos e Mitigações

| Risco | Impacto | Mitigação Atual | Mitigação Recomendada |
|-------|---------|----------------|----------------------|
| JSON inválido do LLM | Falha no parsing | Try/except + fallback | JSON Schema + validação Pydantic |
| Alucinação de preços | Informação enganosa | Alertas explícitos | Grounding com APIs reais |
| Dados desatualizados | Decisões inadequadas | Disclaimer de estimativa | Cache com TTL + atualização periódica |
| Prompt injection | Vazamento/comportamento indesejado | Validação básica de entrada | Sanitização + sistema de mensagens estruturadas |
| Custo inesperado de API | Orçamento estourado | Uso opcional | Rate limiting + monitoramento de custos |

---

## 8. Frontend

### 8.1 Estrutura `static/`

```
static/
├── index.html    # Estrutura semântica + containers dinâmicos
├── index.css     # Glassmorphism, dark mode, animações CSS
└── index.js      # Lógica de formulário + fetch + renderização
```

### 8.2 Fluxo de Interação

```javascript
// 1. Usuário preenche formulário
// 2. Submissão interceptada por JavaScript
document.querySelector('#travelForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  // 3. Coleta dados e monta payload
  const payload = {
    cidade_destino: document.getElementById('destino').value,
    data_saida: document.getElementById('saida').value,
    // ...
  };
  
  // 4. Exibe animação de "agentes trabalhando"
  showAgentAnimation();
  
  // 5. Envia para API e recebe request_id
  const response = await fetch('/api/plan', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
  });
  const initResult = await response.json();
  
  // 6. Abre SSE para logs e resultado final
  const eventSource = new EventSource(`/api/stream/${initResult.request_id}`);
  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.event === 'done') {
      eventSource.close();
      renderResults(data.result);
    } else {
      addLogEntry(data);
    }
  };
});
```

### 8.3 Componentes de UI

| Componente | Descrição | Tecnologias |
|------------|-----------|-------------|
| Formulário | Coleta dados da viagem com validação visual | HTML5 form + JS validation |
| Animação de Agentes | Feedback visual durante processamento | CSS animations + SSE/EventSource |
| Abas de Resultado | Organização do plano em 4 seções | HTML tabs + CSS transitions |
| Cards de Opções | Exibição de voos/hotéis comparáveis | CSS Grid + flexbox |
| Roteiro Diário | Timeline visual do itinerário | CSS flex + date formatting |
| **Glassmorphism Design** | **Efeito de vidro fosco com blur e transparência** | **CSS backdrop-filter + rgba colors** |
| **Dark/Light Mode** | **Alternância suave de tema com persistência** | **CSS variables + localStorage + JS toggle** |
| **Formatação de Moeda** | **Exibição automática em BRL ou USD** | **JS Intl.NumberFormat API** |
| **Validação de Formulário** | **Feedback visual imediato com destaque em campos** | **JS DOM manipulation + CSS classes** |

### 8.4 Limitações do Frontend Atual

- ⚠️ A animação visual usa delays para entrada dos cards, mas logs reais chegam por SSE
- ⚠️ Sem framework frontend (React/Vue) — pode dificultar manutenção em escala
- ⚠️ Sem internacionalização (i18n)
- ⚠️ Acessibilidade básica (ARIA labels mínimos)

### 8.5 Novas Funcionalidades de UI (Implementadas)

#### **Design System Moderno**
- **Glassmorphism**: Efeito de vidro fosco com `backdrop-filter: blur()` e transparência
- **CSS Variables**: Sistema de temas com variáveis CSS para cores e transições
- **Responsivo**: Adaptação para diferentes tamanhos de tela

#### **Sistema de Temas (Dark/Light Mode)**
- **Toggle Button**: Botão no header para alternar entre temas
- **Persistência**: Salvamento da preferência no `localStorage`
- **Detecção Automática**: Leitura de `prefers-color-scheme` do sistema
- **Transição Suave**: Animação de 0.3s entre temas

#### **Animações Avançadas**
- **Agent Cards**: Animação sequencial dos agentes durante processamento
- **Logs em Tempo Real**: Eventos de backend via `EventSource` e endpoint SSE
- **Status Badges**: Atualização visual de status (pending → processing → done/error)
- **Loading States**: Feedback visual enquanto API processa

#### **Validação e Formatação**
- **Form Validation**: Validação de campos obrigatórios com feedback visual
- **Date Validation**: Verificação de datas (retorno > saída)
- **Currency Formatting**: `formatCurrency()` com suporte a BRL e USD
- **Error Handling**: Exibição de alertas e erros amigáveis

#### **Arquivos da Interface**
- `static/index.html` - Estrutura semântica da página
- `static/index.css` - Estilos com Glassmorphism e temas
- `static/index.js` - Lógica de interação, validação e chamadas à API
- `static/index_corrected.css` - Correções de estilo específicas

---

## 9. Testes e Qualidade

### 9.1 Suíte de Testes Backend (`tests/backend/`)

**Execução:**
```bash
python3 -m pytest tests/backend -v
```

**Cobertura Funcional:**

| Categoria | Testes | Descrição |
|-----------|--------|-----------|
| API | `test_api_health.py`, `test_api_plan.py`, `test_api_result.py`, `test_api_stream.py` | Endpoints REST, SSE, status e request_id |
| Modelos | `test_models.py` | Contratos Pydantic e serialização |
| Agentes | `test_agents_complete.py` | Maestro, agentes especialistas, heurística e estrutura de resposta |

### 9.2 Testes Frontend/UI (`tests/frontend/`)

**Localização**: `tests/frontend/`

Como o ambiente pode não ter Node.js, foram criados testes em **Python** que simulam a lógica das funções JavaScript.

**Execução:**
```bash
python3 -m pytest tests/frontend -v
```

**O que é testado:**
- ✅ `formatCurrency()` - Formatação de moeda (BRL, USD, null, undefined)
- ✅ `validateForm()` - Validação de formulário (campos obrigatórios, datas)
- ✅ `getPreferredTheme()` - Detecção de tema (localStorage, preferência do sistema)
- ✅ `applyTheme()` - Aplicação de tema e salvamento
- ✅ `toggleTheme()` - Alternância dark/light mode
- ✅ Sintaxe do arquivo JavaScript (verificação de chaves, parênteses, funções)
- ✅ Integração completa (validar → formatar)
- ✅ Estrutura HTML e consistência CSS

### 9.3 Testes JavaScript Nativos com Jest (Opcional)

**Localização**: `tests/frontend/js_unit_tests/index.test.js` e `package.json`

Caso tenha **Node.js** instalado, há configuração para testes nativos em Jest:

**Execução:**
```bash
# Instalar dependências (apenas primeira vez)
npm install

# Executar testes Jest
npm test
```

**Pré-requisitos:**
- Node.js instalado
- `npm install` executado

**O que é testado:**
- Funções JavaScript com mocks do DOM (jsdom)
- Simulação de `localStorage`, `matchMedia`, `document`
- Testes de integração da lógica de UI

### 9.4 Como Executar Todos os Testes

```bash
# 1. Testes Python (Backend)
cd my-travel-ai
python3 -m pytest tests/backend -v

# 2. Testes Frontend/UI
python3 -m pytest tests/frontend -v

# 3. Testes Jest (se tiver Node.js)
npm test

# 4. Testes de Integração
python3 -m pytest tests/integration -v

# Ou tudo de uma vez
python3 -m pytest tests/backend tests/frontend tests/integration -q
```

### 9.5 Lacunas de Teste (Recomendações)

```python
# 1. Testes de API com TestClient
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_post_api_plan_success():
    response = client.post("/api/plan", json={
        "cidade_destino": "Lisboa",
        "data_saida": "2026-07-10",
        "data_retorno": "2026-07-17"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "processing"
    assert "request_id" in data

# 2. Testes com LLM habilitado (mock do Gemini)
@patch('google.genai.Client')
def test_agente_aereo_com_llm(mock_client):
    # Configurar mock para retornar JSON válido
    # Validar parsing e fallback

# 3. Testes de concorrência
def test_maestro_timeout_handling():
    # Simular agente lento >60s
    # Validar tratamento de timeout

# 4. Testes de frontend (sugestão: Playwright)
# async def test_form_submission_and_rendering(page):
#     await page.goto("http://127.0.0.1:8000")
#     # ... preencher formulário e validar resultado

# 5. Testes adicionais para UI (sugeridos)
# - test_theme_persistence: Testar se tema salva e carrega do localStorage
# - test_form_validation_errors: Testar exibição de erros no formulário
# - test_currency_formatting_edge_cases: Testar valores extremos na formatação
# - test_agent_animation_sequence: Testar sequência de animação dos agentes
```

### 9.6 Métricas de Qualidade

| Métrica | Valor Atual | Meta Recomendada |
|---------|-------------|-----------------|
| Testes automatizados passando | 123/123 | Manter 100% |
| Testes Backend | Implementados em `tests/backend/` | Manter 100% |
| Testes Frontend | Implementados em `tests/frontend/` | Manter 100% |
| Testes de Integração | Implementados em `tests/integration/` | Manter 100% |
| Cobertura de código | ~60% (estimado) | ≥80% |
| Tempo de execução dos testes | ~7-9s | <15s |
| Dependências externas nos testes | 0 | Manter 0 (mock tudo) |
| Testes E2E (UI) | 0 | Adicionar Playwright/Cypress |

### 9.7 Testes de Integração (Backend + Frontend + API)

**Localização**: `tests/integration/`

Valida o fluxo completo de ponta a ponta da aplicação, garantindo a comunicação correta entre todas as camadas.

**O que é testado**:
- ✅ Fluxo completo: Envio de formulário → Processamento de agentes → Exibição de resultados
- ✅ Integração frontend-backend via chamadas à API REST
- ✅ Fallback entre heurística local e LLM (se `GEMINI_API_KEY` estiver configurada)
- ✅ Tratamento de erros parciais e resiliência do maestro

**Execução:**
```bash
python3 -m pytest tests/integration -v
```

---

## 10. Segurança e Privacidade

### 10.1 Estado Atual

✅ **Boas Práticas Implementadas:**
- Chave de API (`GEMINI_API_KEY`) via variável de ambiente, não hardcoded
- Sem armazenamento de dados sensíveis ou histórico de usuários
- Disclaimer explícito sobre natureza estimativa dos dados
- Validação básica de entrada com Pydantic

❌ **Lacunas Críticas para Produção:**

| Vulnerabilidade | Impacto | Recomendação |
|----------------|---------|--------------|
| Sem autenticação | Acesso não autorizado | Implementar JWT/OAuth2 |
| Sem rate limiting | Abuso/DoS | Adicionar `slowapi` ou middleware customizado |
| Logs sem sanitização | Vazamento de dados em stack traces | Usar `structlog` com masking de campos sensíveis |
| CORS não configurado | Vulnerabilidade em frontend separado | Adicionar `CORSMiddleware` com origins explícitas |
| Exposição de erros internos | Information disclosure | Middleware de erro com sanitização |
| Sem validação de tamanho de campos | Buffer overflow/DoS | Adicionar `max_length` em campos Pydantic |

### 10.2 Middleware de Segurança Recomendado

```python
# app/main.py - adicionar dentro de create_app(), após criar api_app

from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# 1. CORS
api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://meudominio.com"],  # Especificar em produção!
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# 2. Rate Limiting
limiter = Limiter(key_func=get_remote_address)
api_app.state.limiter = limiter
api_app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Aplicar decorator nos endpoints
@app.post("/api/plan")
@limiter.limit("10/minute")  # Máx 10 requisições/minuto por IP
async def generate_travel_plan(request: Request, plan: PlanRequest):
    # ...
```

### 10.3 Sanitização de Entradas para LLM

```python
def _sanitizar_para_llm(texto: str, max_length: int = 500) -> str:
    """Remove caracteres perigosos e limita tamanho para prompts."""
    # Remove possíveis tentativas de prompt injection
    texto = texto.replace("```", "").replace("{{", "").replace("}}", "")
    # Limita tamanho para evitar custos excessivos
    return texto[:max_length].strip()

# Uso no agente:
prompt = f"""...
- Interesses: {_sanitizar_para_llm(', '.join(ctx.preferencias.interesses))}
..."""
```

---

## 11. Operação e Observabilidade

### 11.1 Health Check Básico

```bash
curl http://127.0.0.1:8000/api/health
# Resposta: {"status": "ok", "llm_enabled": false, "active_logs": 0}
```

### 11.2 Captura Estruturada de Logs (Implementada)

O projeto implementa captura estruturada de logs para rastrear eventos em todas as camadas da aplicação:

**Backend:**
- `app/agents/logger.py` mantém um `EventLogger` thread-safe com filas por `request_id`.
- Eventos são impressos no terminal e enviados ao endpoint SSE.
- `app/services/planning_jobs.py` mantém `results_store` em memória para o plano final.

**Frontend:**
- Logs de interação do usuário e chamadas à API via `console.log` estruturado no JavaScript.
- Registro de alternância de tema, validação de formulário e respostas da API.
- Exibição direta no console do navegador para depuração.

**Integração:**
- Captura de logs de comunicação entre frontend e backend, incluindo tempos de resposta e erros de rede.
- Registro de fallback entre heurística local e LLM (se configurado).

### 11.3 Métricas para Prometheus (Sugestão)

```python
# requirements.txt - Adicionar
prometheus-fastapi-instrumentator==6.1.0

# app/main.py
from prometheus_fastapi_instrumentator import Instrumentator

@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)

# Métricas automáticas geradas:
# - http_requests_total{method, status, handler}
# - http_request_duration_seconds{handler}
# - http_request_size_bytes, http_response_size_bytes

# Métricas customizadas sugeridas:
# - travel_agent_duration_seconds{agent="aereo|hotel|turismo"}
# - travel_agent_failures_total{agent, error_type}
# - travel_llm_calls_total{status="success|fallback|error"}
# - travel_llm_parse_errors_total
# - travel_plan_generation_total{status="sucesso|parcial|erro"}
```

### 11.4 Dashboard Grafana (Exemplo de Queries)

```promql
# Taxa de sucesso de planos de viagem
sum(rate(travel_plan_generation_total{status="sucesso"}[5m])) 
/ 
sum(rate(travel_plan_generation_total[5m])) * 100

# Latência p95 por agente
histogram_quantile(0.95, 
  sum(rate(travel_agent_duration_seconds_bucket[5m])) by (le, agent)
)

# Taxa de fallback LLM → heurística
sum(rate(travel_llm_fallback_total[5m])) 
/ 
sum(rate(travel_llm_calls_total[5m])) * 100
```

---

## 12. Guia de Desenvolvimento

### 12.1 Setup do Ambiente

```bash
# 1. Clonar repositório
git clone https://github.com/armandossrecife/my-travel-ai.git
cd my-travel-ai

# 2. Criar ambiente virtual (recomendado)
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. (Opcional) Configurar chave Gemini para testes com LLM
export GEMINI_API_KEY="sua_chave_aqui"  # Linux/Mac
# ou
set GEMINI_API_KEY=sua_chave_aqui  # Windows CMD
# ou
$env:GEMINI_API_KEY="sua_chave_aqui"  # PowerShell

# 5. Executar testes
python3 -m pytest tests/backend tests/frontend tests/integration -q

# 6. Iniciar servidor
./run.sh
# ou manualmente:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 7. Acessar aplicação
# Frontend: http://127.0.0.1:8000
# API Docs: http://127.0.0.1:8000/docs
```

### 12.2 Convenções de Código

```python
# 1. Tipagem obrigatória com Pydantic/Type Hints
def calcular_score(valor: float, minimo: float, maximo: float) -> float:
    """Documentação no estilo Google."""
    if maximo == minimo:
        return 1.0
    return 1.0 - ((valor - minimo) / (maximo - minimo))

# 2. Logging estruturado (não print)
logger.debug("processando_opcao", indice=i, total=len(opcoes))

# 3. Tratamento de erros específico
try:
    resultado = operacao_riscosa()
except ValueError as e:
    logger.warning("validacao_falhou", erro=str(e), contexto=ctx.request_id)
    raise HTTPException(status_code=422, detail=f"Validação: {e}")
except Exception as e:
    logger.exception("erro_inesperado", request_id=ctx.request_id)
    raise HTTPException(status_code=500, detail="Erro interno do servidor")

# 4. Separação clara entre heurística e LLM
def gerar_dados(ctx: TravelContext, usar_llm: bool = False) -> dict:
    if usar_llm and os.environ.get("GEMINI_API_KEY"):
        return _gerar_com_llm(ctx)
    return _gerar_com_heuristica(ctx)  # Fallback garantido
```

### 12.3 Adicionando um Novo Destino

**Passo a Passo:**

1. **Atualizar `_CONHECIMENTO_AEREO` em `app/agents/base_local.py`:**
```python
"novo_destino": [
    {"companhia": "Companhia Real", "escalas": 1, "duracao": "12h00", "preco_base": 2800, "hub": "GRU"},
    # ... 2-3 opções realistas
],
```

2. **Atualizar `_CONHECIMENTO_HOTEL` em `app/agents/base_local.py`:**
```python
"novo_destino": {
    "regioes_recomendadas": ["Bairro A", "Bairro B"],
    "hoteis": [
        {
            "nome": "Hotel Exemplo",
            "bairro": "Bairro A",
            "categoria": "4 estrelas",
            "preco_diaria": 300,
            "avaliacao": "8.5/10",
            "destaques": ["Wi-Fi", "Café da manhã"]
        },
        # ... 2-3 opções
    ]
},
```

3. **Atualizar `_PONTOS_TURISTICOS` e `_DICAS_GERAIS` em `app/agents/base_local.py`:**
```python
"novo_destino": [
    {"nome": "Atração Principal", "categoria": "histórico", "bairro": "Centro", 
     "tempo": "2h00", "prioridade": 1},
    # ... 5-8 atrações
],

_dicas_gerais["novo_destino"] = [
    "💡 Dica prática 1",
    "💡 Dica prática 2",
]
```

4. **Testar:**
```bash
# Teste manual via API
curl -X POST http://127.0.0.1:8000/api/plan \
  -H "Content-Type: application/json" \
  -d '{"cidade_destino": "Novo Destino", "data_saida": "2026-08-01", "data_retorno": "2026-08-08"}'

# Teste automatizado (adicionar em tests/backend/test_agents_complete.py)
def test_novo_destino_heuristica():
    ctx = TravelContext(..., cidade_destino="Novo Destino", ...)
    resultado = aereo.run(ctx)
    assert resultado.status == "sucesso"
    assert len(resultado.data["opcoes"]) >= 1
```

### 12.4 Adicionando um Novo Agente Especialista

**Exemplo: `app/agents/clima.py`**

1. **Criar `app/agents/clima.py` seguindo o contrato:**
```python
from app.models import AgentResult, TravelContext

def run(ctx: TravelContext) -> AgentResult:
    try:
        # 1. Obter dados (heurística ou API real)
        dados_clima = _obter_previsao(ctx.cidade_destino, ctx.data_saida, ctx.data_retorno)
        
        # 2. Processar e estruturar
        recomendacoes = _gerar_recomendacoes(dados_clima, ctx.preferencias)
        
        # 3. Retornar no padrão AgentResult
        return AgentResult(
            agent_name="agente_clima",
            status="sucesso",
            data={
                "previsao_diaria": [...],
                "recomendacoes_roupas": recomendacoes,
                "alertas_climaticos": [...]
            },
            fontes=["Heurística local" or "OpenWeatherMap API"],
            alertas=["⚠️ Previsões podem mudar. Consulte antes da viagem."]
        )
    except Exception as e:
        return AgentResult(
            agent_name="agente_clima",
            status="parcial",  # Falha não crítica
            data={},
            erros=[str(e)],
            alertas=["Informações climáticas não disponíveis."]
        )
```

2. **Registrar no `app/agents/maestro.py`:**
```python
# Importar
from app.agents import clima

# No método run(), adicionar à execução paralela:
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:  # Aumentar workers
    futures = {
        "aereo": executor.submit(aereo.run, ctx),
        "hotel": executor.submit(hotel.run, ctx),
        "turismo": executor.submit(turismo.run, ctx),
        "clima": executor.submit(clima.run, ctx),  # Novo agente
    }
    # ... restante do código

# Na consolidação, incluir no resultado:
return TravelPlan(
    # ...
    resultado={
        "passagens_aereas": resultados["aereo"],
        "hoteis": resultados["hotel"],
        "roteiro_turistico": resultados["turismo"],
        "clima": resultados["clima"],  # Novo campo
    },
    # ...
)
```

3. **Atualizar frontend (opcional):**
- Adicionar aba "Clima" em `static/index.js`
- Renderizar `plano.resultado.clima.data`

---

## 13. Roadmap de Evolução

### 13.1 Curto Prazo (1-2 sprints)

| Item | Prioridade | Esforço | Benefício |
|------|-----------|---------|-----------|
| ✅ Remover artefatos (`__MACOSX`, `__pycache__`) | Alta | Baixo | Limpeza do repositório |
| ✅ Refatorar arquitetura para `app/api`, `app/models`, `app/agents`, `app/services`, `app/ui` | Alta | Médio | Separação clara de responsabilidades |
| ✅ Adicionar testes de API com `TestClient` | Alta | Médio | Cobertura de integração |
| 🔄 Definir `response_model` explícito para endpoints assíncronos | Alta | Baixo | Validação automática + docs melhores |
| 🔄 Criar Enums para `status`, `ritmo_roteiro`, preferências | Média | Baixo | Segurança de tipo + autocomplete |
| 🔄 Logging estruturado com `structlog` | Média | Médio | Observabilidade básica |
| 🔄 Sanitização de inputs para LLM | Alta | Baixo | Segurança contra prompt injection |

### 13.2 Médio Prazo (1-2 meses)

| Item | Descrição | Dependências |
|------|-----------|--------------|
| 🔗 Integração com APIs reais | Amadeus/Skyscanner para voos, Booking/Expedia para hotéis | Chaves de API, contratos de uso |
| 🌐 Grounding para turismo | Google Places API + Wikipedia para validação de atrações | API keys, tratamento de rate limits |
| 📡 Evoluir progresso em tempo real | SSE já implementado; aprimorar granularidade/estado persistente | Observabilidade e UX |
| 💾 Persistência de planos | PostgreSQL/SQLite para salvar históricos de viagem | Modelagem de banco, migrações |
| 🔐 Autenticação básica | JWT para usuários registrados | Sistema de usuários, hash de senhas |
| 🧪 Avaliação automática de roteiros | Métricas de qualidade baseadas em dados reais | Dataset de avaliação, scoring |

### 13.3 Longo Prazo (3-6 meses)

| Item | Visão | Impacto |
|------|-------|---------|
| 🤖 Plataforma multiagente escalável | Agentes como microsserviços independentes | Alta disponibilidade, evolução independente |
| 🧠 RAG para conhecimento turístico | Base vetorial com guias oficiais, reviews verificados | Respostas mais precisas e atualizadas |
| 🎯 Otimização multiobjetivo | Balancear preço, tempo, conforto, interesses via algoritmos | Recomendações personalizadas e justificáveis |
| 📊 Observabilidade completa | Prometheus + Grafana + tracing distribuído | Monitoramento proativo, debugging eficiente |
| ♿ Acessibilidade e i18n | WCAG 2.1 AA + suporte a múltiplos idiomas | Inclusão e alcance global |
| 📱 Aplicativo móvel | React Native/Flutter consumindo a mesma API | Experiência omnichannel |

---

## 14. Referências e Recursos

### 14.1 Documentação Oficial

- 🐍 [Python Documentation](https://docs.python.org/3/)
- ⚡ [FastAPI Documentation](https://fastapi.tiangolo.com/)
- 🔍 [Pydantic Documentation](https://docs.pydantic.dev/latest/)
- 🧪 [pytest Documentation](https://docs.pytest.org/)
- 🌐 [Google Gemini API](https://ai.google.dev/gemini-api/docs)

### 14.2 Padrões e Boas Práticas

- 🏗️ [12-Factor App](https://12factor.net/) — Para evolução para produção
- 🔐 [OWASP Top 10](https://owasp.org/www-project-top-ten/) — Segurança em APIs
- 📐 [OpenAPI Specification](https://swagger.io/specification/) — Documentação de APIs
- 🔄 [Semantic Versioning](https://semver.org/) — Controle de versão

### 14.3 Ferramentas Recomendadas

| Categoria | Ferramenta | Uso no Projeto |
|-----------|-----------|----------------|
| Linting | `ruff`, `black`, `mypy` | Qualidade de código Python |
| Testes | `pytest-cov`, `pytest-asyncio` | Cobertura e testes assíncronos |
| API Testing | `httpie`, `Postman`, `curl` | Testes manuais de endpoints |
| Frontend Dev | `Live Server`, `Browser DevTools` | Desenvolvimento da UI |
| Monitoring | `Prometheus`, `Grafana`, `Loki` | Observabilidade em produção |
| CI/CD | `GitHub Actions`, `Docker` | Automação de deploy |

### 14.4 Contato e Suporte

- 📧 **Desenvolvedor Principal**: armando@ufpi.edu.br
- 🐙 **Repositório**: https://github.com/armandossrecife/my-travel-ai
- 📋 **Issue Tracker**: Use GitHub Issues para bugs e feature requests
- 💬 **Discussões**: GitHub Discussions para dúvidas e propostas

---

## 📎 Apêndice A: Exemplo de Execução Completa

```bash
# Terminal 1: Iniciar servidor
$ ./run.sh
🚀 Iniciando servidor em http://127.0.0.1:8000
   Acesse a interface web em http://127.0.0.1:8000
   Documentação da API em   http://127.0.0.1:8000/docs

# Terminal 2: Testar via curl
$ REQUEST_ID=$(curl -s -X POST http://127.0.0.1:8000/api/plan \
  -H "Content-Type: application/json" \
  -d '{
    "cidade_destino": "Lisboa",
    "data_saida": "2026-07-10",
    "data_retorno": "2026-07-17",
    "cidade_origem": "Teresina",
    "quantidade_viajantes": 2,
    "ritmo_roteiro": "moderado",
    "interesses": ["história", "gastronomia"]
  }' | jq -r '.request_id')

$ curl -s "http://127.0.0.1:8000/api/result/$REQUEST_ID" \
  | jq '.resumo, .plano_integrado.estimativa_custos'

{
  "cidade_destino": "Lisboa",
  "cidade_origem": "Teresina",
  "data_saida": "2026-07-10",
  "data_retorno": "2026-07-17",
  "duracao_dias": 8,
  "quantidade_noites": 7
}
{
  "passagens": 3000.0,
  "hospedagem": 2548.0,
  "passeios": 1109.6,
  "total_estimado": 6657.6,
  "moeda": "BRL"
}
```

---

## 📎 Apêndice B: Checklist de Deploy em Produção

```markdown
## ✅ Pré-Deploy

- [ ] Remover artefatos: `__MACOSX/`, `__pycache__/`, `.pytest_cache/`
- [ ] Validar `.gitignore` cobre arquivos sensíveis e de build
- [ ] Definir variáveis de ambiente em produção:
  - `GEMINI_API_KEY` (opcional)
  - `ENV=production`
  - `LOG_LEVEL=INFO`
- [ ] Configurar CORS com origins explícitas
- [ ] Implementar rate limiting (ex: 10 req/min por IP)
- [ ] Sanitizar logs para não expor dados sensíveis
- [ ] Adicionar health check em load balancer
- [ ] Configurar timeout de workers (Uvicorn/Gunicorn)
- [ ] Testar com carga simulada (ex: `locust`)

## ✅ Pós-Deploy

- [ ] Monitorar métricas: latência, erro rate, custo LLM
- [ ] Configurar alertas para falhas >5% ou latência p95 >2s
- [ ] Revisar logs estruturados semanalmente
- [ ] Atualizar base de conhecimento trimestralmente
- [ ] Reavaliar necessidade de autenticação conforme uso
```

---

> **Nota Final**: Este documento técnico foi elaborado para servir como referência viva para a equipe de engenharia. Recomenda-se atualizá-lo a cada mudança significativa na arquitetura ou nos contratos. Para dúvidas sobre decisões de design, consulte os arquivos em `planos/` e `skills/skill.md`.

**Versão do Documento**: 1.0.0  
**Próxima Revisão Programada**: Agosto 2026  
**Responsável pela Manutenção**: Equipe de Engenharia de Software
