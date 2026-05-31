# 📋 Documentação Técnica de Software
## Projeto: my-travel-ai
**Repositório:** https://github.com/armandossrecife/my-travel-ai  
**Versão do Documento:** 1.0.0  
**Última Atualização:** Maio 2026  
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
| **Testes automatizados** | ✅ Implementado | 25 testes passando |
| **Interface web funcional** | ✅ Implementado | Frontend estático |

> ⚠️ **AVISO CRÍTICO**: Esta aplicação é um **demonstrador de arquitetura**, não um produto para reservas reais. Todos os preços e disponibilidades são estimativas que devem ser confirmadas em fontes oficiais.

### 1.3 Stack Tecnológico

```yaml
Backend:
  - Python 3.10+
  - FastAPI 0.95+
  - Pydantic 2.0+
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
  - pytest (testes unitários)
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
│  │  main.py                    │    │
│  │  • GET  /api/health         │    │
│  │  • POST /api/plan           │    │
│  │  • GET  / (frontend)        │    │
│  └─────────────────────────────┘    │
└────────────┬────────────────────────┘
             │ Modelos Pydantic
             ▼
┌─────────────────────────────────────┐
│      CAMADA DE DOMÍNIO/CONTRATOS    │
│  ┌─────────────────────────────┐    │
│  │  models.py                  │    │
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
│  │  agents/maestro.py           │    │
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
              FastAPI (main.py)
                    ↓
              TravelRequest (Pydantic)
                    ↓
              maestro.run()
                    ├─▶ agente_aereo.run() ──▶ FlightOption[]
                    ├─▶ agente_hotel.run() ──▶ HotelOption[]
                    └─▶ agente_turismo.run() ─▶ DailyItinerary[]
                    ↓
              Consolidação + Cálculo de custos
                    ↓
              TravelPlan (resposta JSON)
                    ↓
              Frontend (renderização em abas)
```

**Características do padrão:**
- ✅ Execução paralela via `ThreadPoolExecutor` (3 workers)
- ✅ Tratamento de falhas parciais (um agente falhar não quebra o fluxo)
- ✅ Status granular: `sucesso`, `parcial`, `erro`
- ✅ Timeout configurável por agente (60s padrão)
- ✅ Consolidação centralizada de alertas e recomendações

---

## 3. Estrutura do Código

```
my-travel-ai/
├── 📄 README.md                    # Documentação de alto nível
├── 📄 main.py                      # Entry point: FastAPI + endpoints
├── 📄 models.py                    # Contratos Pydantic (domínio)
├── 📄 requirements.txt             # Dependências Python
├── 📄 run.sh                       # Script de inicialização
│
├── 📁 agents/                      # Módulo de agentes especializados
│   ├── 📄 __init__.py
│   ├── 📄 maestro.py              # Orquestrador principal
│   ├── 📄 aereo.py                # Agente de passagens aéreas
│   ├── 📄 hotel.py                # Agente de hospedagem
│   └── 📄 turismo.py              # Agente de roteiro turístico
│
├── 📁 static/                      # Frontend estático
│   ├── 📄 index.html              # Interface principal
│   ├── 📄 index.css               # Estilos (Glassmorphism)
│   └── 📄 index.js                # Lógica frontend + fetch API
│
├── 📁 tests/                       # Suíte de testes automatizados
│   └── 📄 test_agents.py          # Testes unitários dos agentes
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

### 4.1 `main.py` — API e Ponto de Entrada

**Responsabilidades:**
- Inicializar aplicação FastAPI com metadados
- Expor endpoints REST documentados (OpenAPI)
- Servir frontend estático na rota raiz
- Validar entrada da API e converter para domínio
- Orquestrar chamada ao `maestro` e retornar resposta

**Endpoints:**

| Método | Rota | Descrição | Request | Response |
|--------|------|-----------|---------|----------|
| `GET` | `/api/health` | Health check da API | - | `{"status": "ok", "llm_enabled": bool}` |
| `POST` | `/api/plan` | Gerar plano de viagem | `PlanRequest` | `TravelPlan` (JSON) |
| `GET` | `/` | Servir frontend | - | `index.html` |

**Código-chave:**
```python
@app.post("/api/plan", response_model=None)  # ⚠️ Melhorar: definir response_model
async def generate_travel_plan(request: PlanRequest):
    # 1. Converter PlanRequest → TravelRequest
    travel_req = TravelRequest(
        cidade_destino=request.cidade_destino,
        # ... mapeamento de campos
    )
    
    # 2. Executar orquestrador
    plano = maestro.run(travel_req)
    
    # 3. Tratamento de erros
    if plano.status == "erro":
        raise HTTPException(status_code=422, detail={"erros": plano.alertas})
    
    # 4. Retornar plano serializado
    return plano.model_dump()
```

**Pontos de Atenção para Manutenção:**
- ⚠️ `response_model=None` perde validação automática do FastAPI
- ⚠️ Sem middleware CORS configurado (necessário para frontend separado)
- ⚠️ Sem autenticação/rate limiting (risco de abuso em produção)
- ⚠️ Erros expõem `str(e)` — sanitizar para produção

---

### 4.2 `models.py` — Modelagem de Domínio com Pydantic

**Contratos Principais:**

```python
# Entrada da API (mapeamento do formulário)
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

# Modelo interno de domínio
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

### 4.3 `agents/maestro.py` — Orquestrador Principal

**Fluxo de Execução:**

```mermaid
graph TD
    A[Recebe TravelRequest] --> B[Gerar request_id UUID]
    B --> C[Validar campos obrigatórios]
    C --> D{Validação OK?}
    D -->|Não| E[Retornar TravelPlan com status=erro]
    D -->|Sim| F[Construir TravelContext enriquecido]
    F --> G[ThreadPoolExecutor: 3 workers]
    G --> H[agente_aereo.run(ctx)]
    G --> I[agente_hotel.run(ctx)]
    G --> J[agente_turismo.run(ctx)]
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

### 4.4 `agents/aereo.py` — Agente de Passagens Aéreas

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
    
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    
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

### 4.5 `agents/hotel.py` — Agente de Hospedagem

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

### 4.6 `agents/turismo.py` — Agente de Roteiro Turístico

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
  "llm_enabled": false
}
```

**Campos:**
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `status` | string | Sempre `"ok"` se a API estiver operacional |
| `service` | string | Nome do serviço |
| `version` | string | Versão da API |
| `llm_enabled` | boolean | `true` se `GEMINI_API_KEY` estiver configurada |

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
- `data_retorno > data_saida`: validação lógica
- `quantidade_viajantes >= 1`: restrição mínima

**Resposta de Sucesso (200 OK):** `TravelPlan` (ver seção 5.2)

**Respostas de Erro:**

| Status | Cenário | Exemplo de `detail` |
|--------|---------|-------------------|
| `422` | Validação falhou | `{"message": "Não foi possível processar", "erros": ["'data_retorno' deve ser posterior..."]}` |
| `500` | Erro interno não tratado | `{"detail": "Traceback da exceção..."}` ⚠️ sanitizar em produção |

### 6.3 Documentação Automática

Acesse em execução:
- 📚 **Swagger UI**: `http://localhost:8000/docs`
- 📖 **ReDoc**: `http://localhost:8000/redoc`

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
  
  // 5. Envia para API
  const response = await fetch('/api/plan', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
  });
  
  // 6. Renderiza resultado em abas
  const plano = await response.json();
  renderResults(plano);
});
```

### 8.3 Componentes de UI

| Componente | Descrição | Tecnologias |
|------------|-----------|-------------|
| Formulário | Coleta dados da viagem | HTML5 form + validation |
| Animação de Agentes | Feedback visual durante processamento | CSS animations + JS delays simulados |
| Abas de Resultado | Organização do plano em seções | HTML tabs + CSS transitions |
| Cards de Opções | Exibição de voos/hotéis comparáveis | CSS Grid + flexbox |
| Roteiro Diário | Timeline visual do itinerário | CSS flex + date formatting |

### 8.4 Limitações do Frontend Atual

- ⚠️ Animação dos agentes é **simulada** (delays fixos), não reflete progresso real do backend
- ⚠️ Sem framework frontend (React/Vue) — pode dificultar manutenção em escala
- ⚠️ Sem internacionalização (i18n)
- ⚠️ Acessibilidade básica (ARIA labels mínimos)

---

## 9. Testes e Qualidade

### 9.1 Suíte de Testes (`tests/test_agents.py`)

**Execução:**
```bash
pytest tests/test_agents.py -v
# Resultado esperado: 25 passed in ~0.20s
```

**Cobertura Funcional:**

| Categoria | Testes | Descrição |
|-----------|--------|-----------|
| Validação de Entrada | 3 | Rejeição de cidade ausente, datas inválidas, retorno < saída |
| Cálculos de Domínio | 2 | Cálculo de dias/noites, normalização de cidade |
| Contratos de Agente | 6 | Estrutura de resposta de cada agente (aereo/hotel/turismo) |
| Resiliência | 2 | Destino genérico, fallback em caso de erro |
| Metadados | 2 | Geração de `request_id` único, presença de alertas |
| Orquestração | 10 | Validação do maestro: status, consolidação, tratamento de falhas |

### 9.2 Lacunas de Teste (Recomendações)

```python
# 1. Testes de API com TestClient
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_post_api_plan_success():
    response = client.post("/api/plan", json={
        "cidade_destino": "Lisboa",
        "data_saida": "2026-07-10",
        "data_retorno": "2026-07-17"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["sucesso", "parcial"]

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
#     await page.goto("http://localhost:8000")
#     # ... preencher formulário e validar resultado
```

### 9.3 Métricas de Qualidade

| Métrica | Valor Atual | Meta Recomendada |
|---------|-------------|-----------------|
| Testes passando | 25/25 | Manter 100% |
| Cobertura de código | ~60% (estimado) | ≥80% |
| Tempo de execução dos testes | 0.20s | <1s |
| Dependências externas nos testes | 0 | Manter 0 (mock tudo) |

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
# main.py - Adicionar após app = FastAPI(...)

from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# 1. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://meudominio.com"],  # Especificar em produção!
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# 2. Rate Limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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
curl http://localhost:8000/api/health
# Resposta: {"status": "ok", "llm_enabled": false}
```

### 11.2 Logs Estruturados Recomendados

```python
# requirements.txt - Adicionar
structlog==24.1.0
python-json-logger==2.0.7

# Configuração inicial (main.py)
import structlog

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
)

logger = structlog.get_logger()

# Uso no maestro:
logger.info("maestro.iniciado", request_id=request_id, destino=ctx.cidade_destino)
logger.debug("agente.executado", agent="aereo", status=resultado.status, duration_ms=duration_ms)
```

### 11.3 Métricas para Prometheus (Sugestão)

```python
# requirements.txt - Adicionar
prometheus-fastapi-instrumentator==6.1.0

# main.py
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
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. (Opcional) Configurar chave Gemini para testes com LLM
export GEMINI_API_KEY="sua_chave_aqui"  # Linux/Mac
# ou
set GEMINI_API_KEY=sua_chave_aqui  # Windows CMD
# ou
$env:GEMINI_API_KEY="sua_chave_aqui"  # PowerShell

# 5. Executar testes
pytest tests/ -v

# 6. Iniciar servidor
./run.sh
# ou manualmente:
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 7. Acessar aplicação
# Frontend: http://localhost:8000
# API Docs: http://localhost:8000/docs
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

1. **Atualizar `_CONHECIMENTO_AEREO` em `agents/aereo.py`:**
```python
"novo_destino": [
    {"companhia": "Companhia Real", "escalas": 1, "duracao": "12h00", "preco_base": 2800, "hub": "GRU"},
    # ... 2-3 opções realistas
],
```

2. **Atualizar `_CONHECIMENTO_HOTEL` em `agents/hotel.py`:**
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

3. **Atualizar `_PONTOS_TURISTICOS` e `_DICAS_GERAIS` em `agents/turismo.py`:**
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
curl -X POST http://localhost:8000/api/plan \
  -H "Content-Type: application/json" \
  -d '{"cidade_destino": "Novo Destino", "data_saida": "2026-08-01", "data_retorno": "2026-08-08"}'

# Teste automatizado (adicionar em tests/test_agents.py)
def test_novo_destino_heuristica():
    ctx = TravelContext(..., cidade_destino="Novo Destino", ...)
    resultado = aereo.run(ctx)
    assert resultado.status == "sucesso"
    assert len(resultado.data["opcoes"]) >= 1
```

### 12.4 Adicionando um Novo Agente Especialista

**Exemplo: `agente_clima.py`**

1. **Criar `agents/clima.py` seguindo o contrato:**
```python
from models import TravelContext, AgentResult

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

2. **Registrar no `maestro.py`:**
```python
# Importar
from agents import clima

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
| ✅ Definir `response_model=TravelPlan` no endpoint | Alta | Baixo | Validação automática + docs melhores |
| ✅ Criar Enums para `status`, `ritmo_roteiro`, preferências | Média | Baixo | Segurança de tipo + autocomplete |
| 🔄 Adicionar testes de API com `TestClient` | Alta | Médio | Cobertura de integração |
| 🔄 Logging estruturado com `structlog` | Média | Médio | Observabilidade básica |
| 🔄 Sanitização de inputs para LLM | Alta | Baixo | Segurança contra prompt injection |

### 13.2 Médio Prazo (1-2 meses)

| Item | Descrição | Dependências |
|------|-----------|--------------|
| 🔗 Integração com APIs reais | Amadeus/Skyscanner para voos, Booking/Expedia para hotéis | Chaves de API, contratos de uso |
| 🌐 Grounding para turismo | Google Places API + Wikipedia para validação de atrações | API keys, tratamento de rate limits |
| 📡 Progresso real dos agentes | WebSocket ou Server-Sent Events para feedback em tempo real | Refatoração do frontend |
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
🚀 Iniciando servidor em http://localhost:8000
   Acesse a interface web em http://localhost:8000
   Documentação da API em   http://localhost:8000/docs

# Terminal 2: Testar via curl
$ curl -X POST http://localhost:8000/api/plan \
  -H "Content-Type: application/json" \
  -d '{
    "cidade_destino": "Lisboa",
    "data_saida": "2026-07-10",
    "data_retorno": "2026-07-17",
    "cidade_origem": "Teresina",
    "quantidade_viajantes": 2,
    "ritmo_roteiro": "moderado",
    "interesses": ["história", "gastronomia"]
  }' | jq '.resumo, .plano_integrado.estimativa_custos'

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
