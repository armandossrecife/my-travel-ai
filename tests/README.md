# Testes - My Travel AI

Este diretório contém todos os testes automatizados para o projeto **my-travel-ai**.

## Estrutura de Diretórios

```
tests/
├── README.md                   # Este arquivo
├── conftest.py                 # Configurações compartilhadas pytest
├── run_tests.sh               # Script de execução de testes
│
├── backend/                    # Testes do Backend (API FastAPI)
│   ├── __init__.py
│   ├── test_api_health.py      # Testes do endpoint /api/health
│   ├── test_api_plan.py        # Testes do endpoint /api/plan
│   ├── test_api_stream.py      # Testes do endpoint SSE /api/stream
│   ├── test_api_result.py      # Testes do endpoint /api/result
│   ├── test_models.py          # Testes dos modelos Pydantic
│   └── test_agents_complete.py # Testes completos dos agentes
│
├── frontend/                   # Testes do Frontend
│   ├── __init__.py
│   ├── test_js_functions.py    # Testes das funções JavaScript (Python)
│   ├── test_html_structure.py  # Testes da estrutura HTML
│   ├── test_css_consistency.py # Testes de consistência CSS
│   └── js_unit_tests/          # Testes unitários JS (se Node disponível)
│       └── index.test.js
│
├── integration/                # Testes de Integração
│   ├── __init__.py
│   ├── test_full_flow.py       # Fluxo completo: API → Agentes
│   └── test_sse_flow.py        # Teste de streaming SSE completo
│
└── fixtures/                   # Dados de teste
    ├── sample_requests.json    # Exemplos de requisições válidas
    ├── sample_responses.json   # Exemplos de respostas esperadas
    └── test_data.py           # Dados de teste em Python
```

---

## Como Executar os Testes

### Executar Todos os Testes

```bash
cd my-travel-ai/tests
./run_tests.sh
```

Ou:

```bash
python -m pytest tests/ -v
```

### Executar por Categoria

#### Apenas Backend
```bash
python -m pytest tests/backend/ -v
```

#### Apenas Frontend
```bash
python -m pytest tests/frontend/ -v
```

#### Apenas Integração
```bash
python -m pytest tests/integration/ -v
```

### Executar Teste Específico
```bash
python -m pytest tests/backend/test_api_health.py -v
python -m pytest tests/frontend/test_js_functions.py -v
```

### Com Cobertura (se pytest-cov instalado)
```bash
python -m pytest tests/ --cov=. --cov-report=html
```

---

## Dependências

### Instalar dependências de teste:
```bash
pip install pytest pytest-asyncio httpx
```

Ou use o arquivo `requirements.txt` do projeto que já inclui as dependências.

---

## O que os Testes Cobrem

### Backend (API FastAPI)
- ✅ Endpoints da API (/api/health, /api/plan, /api/stream, /api/result)
- ✅ Validação de entrada (dados obrigatórios, formatos)
- ✅ Modelos Pydantic (TravelRequest, TravelPreferences, etc.)
- ✅ Agentes (maestro, aéreo, hotel, turismo)
- ✅ Resiliência e tratamento de erros

### Frontend (HTML/JS)
- ✅ Funções JavaScript (formatCurrency, validateForm, temas)
- ✅ Estrutura HTML (elementos obrigatórios, formulário)
- ✅ Consistência CSS (sintaxe, temas, responsividade)

### Integração
- ✅ Fluxo completo: Requisição → Processamento → Resultado
- ✅ Streaming SSE: Recebimento de eventos em tempo real
- ✅ Múltiplas requisições simultâneas

---

## Fixtures Disponíveis (conftest.py)

O arquivo `conftest.py` fornece fixtures compartilhadas:

- `sample_travel_request`: TravelRequest válido
- `sample_travel_context`: TravelContext válido para agentes
- `sample_plan_request_data`: Dados para API PlanRequest
- `invalid_plan_request_data`: Dados inválidos para testes
- `sample_form_data`: Dados simulados do formulário HTML
- `sample_api_response`: Resposta simulada da API
- `make_request`: Factory para TravelRequest customizado
- `make_context`: Factory para TravelContext customizado

---

## Notas Importantes

### O que NÃO é alterado
- ✅ Código original em `main.py`
- ✅ Código original em `models.py`
- ✅ Código original em `agents/*.py`
- ✅ Interface `static/index.html`
- ✅ Lógica em `static/index.js`
- ✅ Estilos em `static/*.css`

### Desafios Conhecidos
- **Ambiente sem Node.js**: Testes JS são feitos via simulação em Python
- **API Key do Gemini**: Testes funcionam com ou sem a chave (modo simulação)
- **Testes SSE**: Requerem tratamento assíncrono adequado

---

## Adicionar Novos Testes

### Para Backend:
1. Crie um arquivo `test_*.py` em `tests/backend/`
2. Use as fixtures do `conftest.py`
3. Importe `client` do `main.py` para testes da API

### Para Frontend:
1. Crie um arquivo `test_*.py` em `tests/frontend/`
2. Use simulação em Python para lógica JavaScript
3. Leia arquivos estáticos para validar estrutura

### Para Integração:
1. Crie um arquivo `test_*.py` em `tests/integration/`
2. Use `client` para fazer requisições completas
3. Valide fluxos end-to-end

---

## Troubleshooting

### Erro: `ModuleNotFoundError: No module named 'main'`
**Solução**: Execute os testes a partir do diretório raiz do projeto ou verifique se o `conftest.py` está configurado corretamente.

### Erro: `422 Validation Error`
**Solução**: Verifique se os dados enviados para a API estão no formato correto (datas em YYYY-MM-DD, campos obrigatórios preenchidos).

### Testes SSE travando
**Solução**: Os testes SSE têm timeout implícito. Se travarem, verifique se o servidor não está processando indefinidamente.

---

## Contribuição

Ao adicionar novos testes:
1. Siga o padrão de nomenclatura: `test_*.py`
2. Use docstrings descritivas
3. Use as fixtures do `conftest.py` quando possível
4. Mantenha os testes independentes

---

**Documentação atualizada em**: 04/06/2026  
**Versão**: 1.0  
**Status**: Implementado
