# Plano de Implementação de Testes - My Travel AI

## 1. Visão Geral

Este documento apresenta o plano detalhado para organização, refatoração e implementação de testes para o projeto **my-travel-ai**, cobrindo o backend (API FastAPI) e o frontend (HTML/JavaScript).

### Objetivos
- Organizar todos os testes em uma estrutura centralizada
- Refazer testes do backend (API) com cobertura adequada
- Refazer testes do frontend (JavaScript) com validação completa
- Criar roteiro de execução dos testes
- **Não alterar código original** da aplicação
- **Não alterar funcionalidades** já implementadas

---

## 2. Estrutura de Diretórios Proposta

```
my-travel-ai/
├── tests/                          # Diretório centralizado de testes
│   ├── README.md                   # Documentação dos testes
│   ├── conftest.py                 # Configurações compartilhadas pytest
│   ├── run_tests.sh               # Script de execução de testes
│   │
│   ├── backend/                    # Testes do Backend (API)
│   │   ├── __init__.py
│   │   ├── test_api_health.py      # Testes do endpoint /api/health
│   │   ├── test_api_plan.py        # Testes do endpoint /api/plan
│   │   ├── test_api_stream.py      # Testes do endpoint SSE /api/stream
│   │   ├── test_api_result.py      # Testes do endpoint /api/result
│   │   ├── test_models.py          # Testes dos modelos Pydantic
│   │   └── test_agents_complete.py # Testes completos dos agentes
│   │
│   ├── frontend/                   # Testes do Frontend
│   │   ├── __init__.py
│   │   ├── test_js_functions.py    # Testes das funções JavaScript (Python)
│   │   ├── test_html_structure.py  # Testes da estrutura HTML
│   │   ├── test_css_consistency.py # Testes de consistência CSS
│   │   └── js_unit_tests/          # Testes unitários JS (se Node disponível)
│   │       └── (arquivos .js)
│   │
│   ├── integration/                # Testes de Integração
│   │   ├── __init__.py
│   │   ├── test_full_flow.py       # Fluxo completo: Frontend → API → Agentes
│   │   └── test_sse_flow.py        # Teste de streaming SSE completo
│   │
│   └── fixtures/                   # Dados de teste
│       ├── sample_requests.json    # Exemplos de requisições válidas
│       ├── sample_responses.json   # Exemplos de respostas esperadas
│       └── test_data.py           # Dados de teste em Python
```

---

## 3. Plano de Testes do Backend (API)

### 3.1. Testes da API FastAPI (`test_api_*.py`)

#### **test_api_health.py**
- [x] Testar endpoint GET `/api/health`
- [x] Validar estrutura da resposta (status, service, version, llm_enabled, active_logs)
- [x] Verificar se retorna HTTP 200
- [ ] Testar comportamento com/sem GEMINI_API_KEY

#### **test_api_plan.py**
- [x] Testar POST `/api/plan` com dados válidos
- [x] Validar retorno de request_id
- [x] Validar status "processing"
- [x] Testar validação de entrada (cidade_destino obrigatório)
- [x] Testar validação de datas (retorno > saída)
- [x] Testar conversão PlanRequest → TravelRequest
- [ ] Testar tratamento de erro 500
- [ ] Testar campos opcionais (cidade_origem, interesses)

#### **test_api_stream.py**
- [x] Testar GET `/api/stream/{request_id}` válido
- [x] Testar request_id inexistente
- [x] Validar formato SSE (data: {...}\n\n)
- [x] Testar desconexão do cliente
- [ ] Testar recebimento de eventos em tempo real
- [ ] Testar evento de conclusão "done"

#### **test_api_result.py**
- [x] Testar GET `/api/result/{request_id}` durante processamento
- [x] Testar GET `/api/result/{request_id}` após conclusão
- [x] Testar request_id inexistente
- [x] Validar estrutura do resultado final

### 3.2. Testes dos Modelos (`test_models.py`)

#### **TravelRequest**
- [x] Validação de campos obrigatórios
- [x] Validação de tipos de dados
- [x] Validação de datas (retorno > saída na API, não no modelo)

#### **TravelPreferences**
- [x] Valores padrão corretos
- [x] Validação de quantidade_viajantes >= 1

#### **AgentResult**
- [x] Estrutura correta (agent_name, status, data, alertas, erros)
- [x] Status válidos: "sucesso", "parcial", "erro"

### 3.3. Testes dos Agentes (`test_agents_complete.py`)

#### **Maestro (Orquestrador)**
- [x] Validação de entrada (cidade_destino vazia)
- [x] Validação de datas (retorno anterior à saída)
- [x] Cálculo correto de dias e noites
- [x] Normalização de cidade_destino
- [x] Geração de request_id único
- [x] Resiliência com destino desconhecido

#### **Agente Aéreo**
- [x] Retorna opções de voo
- [x] Opções têm companhia e preço
- [x] Limitações presentes
- [x] Melhor opção sugerida
- [x] Tratamento sem cidade_origem

#### **Agente Hotel**
- [x] Retorna opções de hotel
- [x] Cálculo correto de noites
- [x] Preço total > preço diária
- [x] Regiões recomendadas presentes

#### **Agente Turismo**
- [x] Retorna roteiro por dia
- [x] Número correto de dias no roteiro
- [x] Primeiro dia = chegada
- [x] Último dia = retorno
- [x] Pontos turísticos e dicas presentes

---

## 4. Plano de Testes do Frontend

### 4.1. Testes das Funções JavaScript (`test_js_functions.py`)

#### **formatCurrency()**
- [x] Formatar valor válido BRL (R$ 1.234,56)
- [x] Formatar valor válido USD (US$ 100.00)
- [x] Tratar valor null → "N/D"
- [x] Tratar valor undefined → "N/D"
- [x] Formatar valor zero
- [x] Formatar valor negativo

#### **validateForm()**
- [x] Dados válidos → true
- [x] Cidade vazia → false
- [x] Cidade com espaços → false
- [x] Data saída ausente → false
- [x] Data retorno ausente → false
- [x] Retorno anterior à saída → false
- [x] Datas iguais → false

#### **Funções de Tema**
- [x] getPreferredTheme() - lógica dark/light
- [x] applyTheme() - aplicação correta
- [x] toggleTheme() - alternância correta

#### **Funções de Renderização (simuladas)**
- [ ] renderSummary() - estrutura correta
- [ ] renderCosts() - exibição de custos
- [ ] renderFlights() - cards de voos
- [ ] renderHotels() - cards de hotéis
- [ ] renderItinerary() - roteiro por dia

### 4.2. Testes da Estrutura HTML (`test_html_structure.py`)

- [ ] Verificar elementos obrigatórios presentes
- [ ] Verificar formulário com todos os campos
- [ ] Verificar botões (submit, new plan, retry)
- [ ] Verificar seções (agents, results, error, logs)
- [ ] Verificar links para CSS e JS
- [ ] Validar HTML básico (tags fechadas)

### 4.3. Testes de Consistência CSS (`test_css_consistency.py`)

- [ ] Verificar se index.css existe
- [ ] Verificar se index_corrected.css existe
- [ ] Comparar se há duplicação desnecessária
- [ ] Validar sintaxe CSS básica

---

## 5. Testes de Integração

### 5.1. Fluxo Completo (`test_full_flow.py`)

1. [ ] Enviar requisição POST `/api/plan`
2. [ ] Capturar request_id
3. [ ] Fazer polling em `/api/result/{request_id}`
4. [ ] Validar resultado final completo
5. [ ] Verificar se todos os agentes executaram

### 5.2. Fluxo SSE (`test_sse_flow.py`)

1. [ ] Iniciar plano via POST `/api/plan`
2. [ ] Conectar em `/api/stream/{request_id}`
3. [ ] Receber eventos em tempo real
4. [ ] Validar formato dos eventos
5. [ ] Receber evento de conclusão "done"

---

## 6. Roteiro de Execução dos Testes

### 6.1. Script de Execução (`run_tests.sh`)

```bash
#!/bin/bash

echo "🧪 MY TRAVEL AI - SUITE DE TESTES"
echo "=================================="
echo ""

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Testes do Backend (API + Agentes)
echo -e "${YELLOW}📦 Executando Testes do Backend...${NC}"
echo "----------------------------------------"
python -m pytest tests/backend/ -v --tb=short
BACKEND_RESULT=$?

if [ $BACKEND_RESULT -eq 0 ]; then
    echo -e "${GREEN}✅ Testes do Backend: PASSOU${NC}"
else
    echo -e "${RED}❌ Testes do Backend: FALHOU${NC}"
fi

echo ""

# 2. Testes do Frontend
echo -e "${YELLOW}🌐 Executando Testes do Frontend...${NC}"
echo "----------------------------------------"
python -m pytest tests/frontend/ -v --tb=short
FRONTEND_RESULT=$?

if [ $FRONTEND_RESULT -eq 0 ]; then
    echo -e "${GREEN}✅ Testes do Frontend: PASSOU${NC}"
else
    echo -e "${RED}❌ Testes do Frontend: FALHOU${NC}"
fi

echo ""

# 3. Testes de Integração (opcional, pode demorar)
echo -e "${YELLOW}🔗 Executando Testes de Integração...${NC}"
echo "----------------------------------------"
python -m pytest tests/integration/ -v --tb=short
INTEGRATION_RESULT=$?

if [ $INTEGRATION_RESULT -eq 0 ]; then
    echo -e "${GREEN}✅ Testes de Integração: PASSOU${NC}"
else
    echo -e "${RED}❌ Testes de Integração: FALHOU${NC}"
fi

echo ""
echo "=================================="
echo -e "${YELLOW}📊 RESUMO DOS TESTES${NC}"
echo "=================================="

if [ $BACKEND_RESULT -eq 0 ]; then
    echo -e "Backend:  ${GREEN}PASSOU${NC}"
else
    echo -e "Backend:  ${RED}FALHOU${NC}"
fi

if [ $FRONTEND_RESULT -eq 0 ]; then
    echo -e "Frontend: ${GREEN}PASSOU${NC}"
else
    echo -e "Frontend: ${RED}FALHOU${NC}"
fi

if [ $INTEGRATION_RESULT -eq 0 ]; then
    echo -e "Integração: ${GREEN}PASSOU${NC}"
else
    echo -e "Integração: ${RED}FALHOU${NC}"
fi

echo ""
echo "=================================="

# Exit com erro se algum teste falhou
if [ $BACKEND_RESULT -ne 0 ] || [ $FRONTEND_RESULT -ne 0 ] || [ $INTEGRATION_RESULT -ne 0 ]; then
    exit 1
fi

exit 0
```

### 6.2. Comandos Individuais

```bash
# Todos os testes
python -m pytest tests/ -v

# Apenas backend
python -m pytest tests/backend/ -v

# Apenas frontend
python -m pytest tests/frontend/ -v

# Apenas integração
python -m pytest tests/integration/ -v

# Com cobertura (se pytest-cov instalado)
python -m pytest tests/ --cov=. --cov-report=html

# Testes específicos
python -m pytest tests/backend/test_api_health.py -v
python -m pytest tests/frontend/test_js_functions.py -v
```

---

## 7. Dependências e Configuração

### 7.1. Requirements para Testes (`requirements-test.txt`)

```
pytest>=7.0.0
pytest-asyncio>=0.21.0
httpx>=0.24.0  # Para testes da API FastAPI
```

### 7.2. Configuração pytest (`conftest.py`)

```python
import sys
import os
import pytest
from datetime import date

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models import TravelRequest, TravelPreferences

@pytest.fixture
def sample_travel_request():
    """Fixture com uma requisição de viagem válida."""
    return TravelRequest(
        cidade_destino="Lisboa",
        data_saida=date(2026, 7, 10),
        data_retorno=date(2026, 7, 17),
        cidade_origem="Teresina",
        preferencias=TravelPreferences(
            quantidade_viajantes=2,
            preferencia_voo="melhor_custo_beneficio"
        )
    )

@pytest.fixture
def sample_plan_request_data():
    """Fixture com dados para PlanRequest (API)."""
    return {
        "cidade_destino": "Paris",
        "data_saida": "2026-08-01",
        "data_retorno": "2026-08-10",
        "cidade_origem": "São Paulo",
        "quantidade_viajantes": 2,
        "preferencia_voo": "menor_preco",
        "preferencia_hotel": "melhor_custo_beneficio",
        "ritmo_roteiro": "moderado",
        "interesses": ["museus", "gastronomia"]
    }
```

---

## 8. Cronograma de Implementação

### Fase 1: Organização (1 dia)
- [ ] Criar estrutura de diretórios `tests/backend/`, `tests/frontend/`, `tests/integration/`
- [ ] Mover arquivos existentes para novos locais
- [ ] Criar `conftest.py` e `run_tests.sh`

### Fase 2: Refatoração Backend (2 dias)
- [ ] Refatorar `test_agents.py` existente → `tests/backend/test_agents_complete.py`
- [ ] Criar `tests/backend/test_api_health.py`
- [ ] Criar `tests/backend/test_api_plan.py`
- [ ] Criar `tests/backend/test_api_stream.py`
- [ ] Criar `tests/backend/test_api_result.py`
- [ ] Criar `tests/backend/test_models.py`

### Fase 3: Refatoração Frontend (1-2 dias)
- [ ] Refatorar `test_js_functions.py` existente → `tests/frontend/`
- [ ] Adicionar testes para funções de renderização
- [ ] Criar `tests/frontend/test_html_structure.py`
- [ ] Criar `tests/frontend/test_css_consistency.py`

### Fase 4: Testes de Integração (1 dia)
- [ ] Criar `tests/integration/test_full_flow.py`
- [ ] Criar `tests/integration/test_sse_flow.py`

### Fase 5: Documentação e Finalização (1 dia)
- [ ] Criar `tests/README.md`
- [ ] Testar script `run_tests.sh`
- [ ] Validar cobertura de testes
- [ ] Documentar como executar

---

## 9. Considerações Importantes

### 9.1. O que NÃO será alterado
- ✅ Código original em `main.py`
- ✅ Código original em `models.py`
- ✅ Código original em `agents/*.py`
- ✅ Interface `static/index.html`
- ✅ Lógica em `static/index.js`
- ✅ Estilos em `static/index.css` e `static/index_corrected.css`

### 9.2. Desafios Identificados
- **Ambiente sem Node.js**: Testes JS serão feitos via simulação em Python (conforme já existe)
- **API Key do Gemini**: Testes devem funcionar com ou sem a chave (modo simulação)
- **Testes SSE**: Requerem tratamento assíncrono adequado

### 9.3. Estratégia para Testes Assíncronos
```python
# Usar httpx com AsyncClient para testar endpoints FastAPI
from httpx import AsyncClient, ASGITransport
from main import app

async def test_api_plan_async():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/plan", json={...})
        assert response.status_code == 200
```

---

## 10. Próximos Passos

1. **Aprovação do Plano**: Revisar este documento e validar a abordagem
2. **Iniciar Fase 1**: Criar estrutura de diretórios
3. **Executar Fases Sequencialmente**: Seguir cronograma
4. **Validação Contínua**: Testar após cada fase

---

**Documento criado em**: 04/06/2026  
**Versão**: 1.0  
**Status**: Aguardando Aprovação
