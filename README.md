# My Travel AI

Protótipo didático de IA multiagente com API FastAPI e interface web para planejamento de viagens. A aplicação combina agentes especialistas para sugerir passagens, hospedagens e roteiro turístico, usando heurística local por padrão e Google Gemini quando `GEMINI_API_KEY` está configurada.

> Esta aplicação é um protótipo educacional para trabalhar conceitos básicos de agentes de IA generativa. Não use em produção sem revisar segurança, persistência, observabilidade e fontes reais de dados.

## Funcionalidades

- 4 agentes modulares: maestro, aéreo, hotel e turismo.
- Execução paralela dos 3 agentes especialistas com `concurrent.futures`.
- Engine híbrida: heurística local por padrão e Gemini LLM opcional.
- Base de conhecimento local para destinos populares como Lisboa, Paris, Nova York, Miami, Buenos Aires e Roma.
- API com endpoints para health check, criação de plano, consulta de resultado e streaming SSE.
- Interface web estática com tema claro/escuro, progresso dos agentes, abas de resultado, validação de formulário e formatação de moeda.
- Testes automatizados para backend, frontend e integração.

## Arquitetura

O projeto foi refatorado para separar responsabilidades em pacotes dentro de `app/`:

```text
app/
├── main.py                 # Factory e instância FastAPI (app.main:app)
├── api/
│   ├── schemas.py          # Schemas da API, incluindo PlanRequest
│   └── routes/             # Rotas health, plan, stream e result
├── models/
│   └── travel.py           # Modelos Pydantic de domínio
├── agents/
│   ├── maestro.py          # Orquestrador
│   ├── aereo.py            # Agente de passagens
│   ├── hotel.py            # Agente de hospedagens
│   ├── turismo.py          # Agente de roteiro
│   └── logger.py           # Eventos e filas para SSE
├── services/
│   └── planning_jobs.py    # Execução em background e armazenamento em memória
└── ui/
    └── static.py           # Montagem de / e /static
```

A interface permanece em:

- `static/index.html`
- `static/index.css`
- `static/index.js`
- `static/index_corrected.css`

Novos imports devem usar `app.*`. Os módulos antigos de fachada (`main.py`, `models.py`, `agents/*`) foram removidos.

## API

- `GET /api/health` - status da aplicação e indicação de LLM habilitado.
- `POST /api/plan` - inicia a geração de um plano e retorna `request_id`.
- `GET /api/stream/{request_id}` - envia logs/eventos em tempo real via SSE.
- `GET /api/result/{request_id}` - retorna `processing` ou o plano final.
- `GET /` - serve a interface web.
- `GET /docs` - documentação interativa do FastAPI.

## Execução

Com Gemini:

```bash
export GEMINI_API_KEY=sua_chave_aqui
./run.sh
```

Sem Gemini, basta executar:

```bash
./run.sh
```

O script instala dependências com `uv` e inicia:

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Saída esperada:

```bash
🚀 Iniciando servidor em http://127.0.0.1:8000
   Acesse a interface web em http://127.0.0.1:8000
   Documentação da API em   http://127.0.0.1:8000/docs
```

## Testes

Executar a suíte completa:

```bash
python3 -m pytest tests/backend tests/frontend tests/integration -q
```

Ou por categoria:

```bash
python3 -m pytest tests/backend -v
python3 -m pytest tests/frontend -v
python3 -m pytest tests/integration -v
```

Também existe o script:

```bash
./tests/run_tests.sh
```

### Organização dos Testes

- `tests/backend/` - API FastAPI, modelos Pydantic e agentes.
- `tests/frontend/` - estrutura HTML, consistência CSS e funções JS simuladas em Python.
- `tests/integration/` - fluxo completo e SSE.
- `tests/frontend/js_unit_tests/` - testes Jest opcionais.

Para testes JavaScript nativos, quando Node.js estiver disponível:

```bash
npm install
npm test
```

## Logs e Progresso

O progresso do processamento é exposto por eventos em memória:

- `app/agents/logger.py` mantém filas por `request_id`.
- `app/services/planning_jobs.py` armazena resultados em memória.
- `GET /api/stream/{request_id}` consome os eventos via SSE.
- O frontend também registra interações e respostas no console do navegador.

## Observações Técnicas

- O armazenamento de resultados é em memória; reiniciar o servidor apaga jobs/resultados.
- A heurística local não consulta disponibilidade real de voos, hotéis ou atrações.
- Quando `GEMINI_API_KEY` está presente, os agentes tentam usar Gemini e fazem fallback para heurística local em caso de erro.
- Valores, disponibilidade e horários devem ser confirmados em fontes oficiais antes de qualquer compra/reserva.

## Material de Projeto

- Planejamento: [planos](planos)
- Revisões/documentação auxiliar: [docs](docs)
- Testes automáticos: [tests](tests)

## Contato

Dúvidas, informações ou sugestões: armando@ufpi.edu.br
