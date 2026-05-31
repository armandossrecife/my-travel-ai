# Plano de Implementação — Agente de Planejamento de Viagens Multiagente

Este documento apresenta a especificação técnica e o plano de ação para a criação de uma aplicação de planejamento de viagens inteligente baseada no padrão multiagente detalhado em `plano.md` e `skill.md`.

Este plano foi gerado via Google Antigravity usando o modelo Gemini Flash 3.5

## User Review Required

> [!NOTE]
> Proposta de Arquitetura de Execução:
> Para garantir que a aplicação funcione perfeitamente de forma imediata e autônoma (mesmo sem chaves de API pagas configuradas), propomos uma **Arquitetura Híbrida de Inteligência**. Cada agente terá duas engines de execução:
> 1. **Engine LLM**: Utiliza a API do Gemini via biblioteca `google-genai` (se a variável de ambiente `GEMINI_API_KEY` estiver configurada), para geração altamente dinâmica baseada nos prompts do `skill.md`.
> 2. **Engine de Heurística Generativa Local**: Caso a chave não esteja configurada, uma engine local em Python simula as respostas dos agentes de forma inteligente, mapeando o destino (ex: se for Lisboa, sugere Belém, Alfama, voos da TAP, hotéis locais reais) e gerando itinerários coerentes e precisos com base na data e duração informadas.

## Proposed Changes

A solução será desenvolvida em Python no backend com uma interface web interativa em Vanilla HTML, CSS e JavaScript no frontend, proporcionando alta performance e estética visual extraordinária (Glassmorphism moderno).

Abaixo está o mapeamento dos novos arquivos a serem criados no diretório do projeto `/Users/armando/Desktop/AgentesIA/antigravity/projetos/viagem`:

### [Backend e Modelos]

#### [NEW] [requirements.txt](file:///Users/armando/Desktop/AgentesIA/antigravity/projetos/viagem/requirements.txt)
Declaração de dependências do Python:
- `fastapi` e `uvicorn[standard]` (para a API de alta performance)
- `pydantic` (validação e normalização de dados)
- `httpx` (para chamadas HTTP)
- `google-genai` (para o agente baseado em LLM)
- `pytest` (para testes unitários de qualidade)

#### [NEW] [models.py](file:///Users/armando/Desktop/AgentesIA/antigravity/projetos/viagem/models.py)
Modelos de dados Pydantic estritos, implementando exatamente os contratos de `TravelContext`, `AgentResult`, `FlightOption`, `HotelOption`, `TouristAttraction`, `DailyItinerary` e a resposta integrada `TravelPlan`.

### [Agentes]

#### [NEW] [agents/aereo.py](file:///Users/armando/Desktop/AgentesIA/antigravity/projetos/viagem/agents/aereo.py)
Implementa o `AgenteAereo`. Calcula opções de voos de ida e volta, pontua voos usando a equação de `skill.md`, e classifica a melhor opção baseada em custo-benefício.

#### [NEW] [agents/hotel.py](file:///Users/armando/Desktop/AgentesIA/antigravity/projetos/viagem/agents/hotel.py)
Implementa o `AgenteHotel`. Gera opções de hotéis na região ideal, calcula noites, políticas de cancelamento e gera um ranking ponderado dos hotéis.

#### [NEW] [agents/turismo.py](file:///Users/armando/Desktop/AgentesIA/antigravity/projetos/viagem/agents/turismo.py)
Implementa o `AgenteTurismo`. Constrói um itinerário diário dividido em manhã/tarde/noite, agrupa atrações próximas e adiciona avisos e dicas práticas.

#### [NEW] [agents/maestro.py](file:///Users/armando/Desktop/AgentesIA/antigravity/projetos/viagem/agents/maestro.py)
O orquestrador central. Valida entradas (destino, datas coerentes), dispara a execução paralela ou sequencial dos agentes especialistas, trata erros parciais de forma resiliente, e formata o Markdown final de recomendação.

### [Frontend & Interface Web]

#### [NEW] [static/index.html](file:///Users/armando/Desktop/AgentesIA/antigravity/projetos/viagem/static/index.html)
Estrutura da aplicação single-page (SPA). Interface limpa com formulário flutuante moderno de input, área de progresso das ações dos agentes em tempo real ("Maestro analisando...", "Aéreo buscando..."), e dashboard rico de resultados com abas dedicadas para:
1. Painel Geral (Maestro Resumo)
2. Voos Recomendados
3. Hotéis & Hospedagem
4. Roteiro de Turismo Interativo
5. Orçamento & Alertas

#### [NEW] [static/index.css](file:///Users/armando/Desktop/AgentesIA/antigravity/projetos/viagem/static/index.css)
Visual de altíssimo nível (Premium Theme). Design escuro sofisticado com efeitos de vidro translúcido (Glassmorphism), gradientes vibrantes no estilo Neon Cyber (azul-turquesa e roxo profundo), tipografia de alta qualidade via Google Fonts (Inter e Outfit) e transições e micro-animações suaves para cada interação do usuário.

#### [NEW] [static/index.js](file:///Users/armando/Desktop/AgentesIA/antigravity/projetos/viagem/static/index.js)
Controla a lógica do cliente. Envia os dados assincronamente à API, simula uma linha do tempo ativa dos agentes trabalhando em segundo plano para prender o usuário, e renderiza os cards de voos, hotéis e a linha do tempo do roteiro de forma extremamente dinâmica.

### [Infraestrutura & Execução]

#### [NEW] [main.py](file:///Users/armando/Desktop/AgentesIA/antigravity/projetos/viagem/main.py)
Arquivo de inicialização principal. Expõe endpoints FastAPI (`/api/plan` para gerar o planejamento de viagem, `/api/health` para status) e monta a pasta `static` para servir a interface web na raiz.

#### [NEW] [run.sh](file:///Users/armando/Desktop/AgentesIA/antigravity/projetos/viagem/run.sh)
Script utilitário para instalar as dependências via `uv pip` e iniciar o servidor FastAPI localmente de forma simples.

## Verification Plan

### Automated Tests
Para validar as regras e contratos definidos na skill, criaremos uma suíte de testes unitários em `tests/test_agents.py` cobrindo:
1. **Validação do Maestro**: Rejeição de datas de saída após o retorno, ausência de campos obrigatórios.
2. **Resiliência do Fluxo**: Simulação de falha no `AgenteAereo` garantindo que a resposta final continue com `status: parcial`, trazendo os dados de hotel e turismo normalmente.
3. **Cálculo de Rankings**: Verificação das fórmulas matemáticas de peso do Voo e Hotel.

Execução dos testes usando:
```bash
uv run pytest tests/
```

### Manual Verification
1. Subiremos o servidor FastAPI com:
   ```bash
   ./run.sh
   ```
2. Abriremos o navegador na URL local `http://127.0.0.1:8000`.
3. Testaremos vários fluxos:
   - Viagem curta (Lisboa, 10-07 a 17-07).
   - Input inválido (retorno anterior à saída) para verificar a elegante mensagem de erro do formulário.
   - Cenário com cidade de origem fornecida e sem ela.