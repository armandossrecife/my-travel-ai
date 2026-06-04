# Instruções

Este é um **protótipo** de IA multiagente com interface web. Algumas funcionalidades não estão completamente implementadas, pois o objetivo deste protótipo é demonstrar como agentes de IA podem funcionar utilizando modelos de LLM.

## Funcionalidades Implementadas
- 4 agentes modulares (maestro, agente_aereo, agente_hotel, agente_turismo)
- Execução paralela dos 3 agentes especialistas via concurrent.futures
- Engine híbrida: Heurística local por padrão + Gemini LLM se GEMINI_API_KEY estiver configurada
- Base de conhecimento rica para 7 destinos populares (Lisboa, Paris, Nova York, Miami, Buenos Aires, Roma + genérico)
- **Interface Premium com UI Avançada:**
  - Design Glassmorphism moderno
  - Dark mode / Light mode com alternância suave
  - Animação dos agentes em tempo real durante o processamento
  - 4 abas de resultados (Passagens, Hotéis, Roteiro, Resumo)
  - Formulário validado com feedback visual
  - Formatação automática de moeda (BRL, USD)
  - Responsivo para diferentes tamanhos de tela
- Validação completa de datas, resiliência a falhas parciais
- Captura estruturada de logs para monitoramento de backend, frontend e integração de API

## Interface Web (UI)

A interface do usuário foi desenvolvida com foco em experiência do usuário (UX) e design moderno:

### Recursos da UI:
- **Glassmorphism**: Efeito de vidro fosco com blur e transparência
- **Tema Escuro/Claro**: Alternância suave com salvamento de preferência no localStorage
- **Animação de Agentes**: Visualização em tempo real do processamento de cada agente
- **Abas de Resultados**: Organização clara das informações (Passagens, Hotéis, Roteiro, Resumo)
- **Validação de Formulário**: Feedback visual imediato com destaque nos campos obrigatórios
- **Formatação de Moeda**: Exibição automática em formato brasileiro (R$) ou internacional (US$)

### Arquivos da Interface:
- `static/index.html` - Estrutura da página
- `static/index.css` - Estilos com Glassmorphism e temas
- `static/index.js` - Lógica de interação, validação e chamadas à API
- `static/index_corrected.css` - Correções de estilo

## Execução

```bash
export GEMINI_API_KEY=sua_chave_aqui
./run.sh
```

Saída esperada:

```bash
🚀 Iniciando servidor em http://localhost:8000
   Acesse a interface web em http://localhost:8000
   Documentação da API em   http://localhost:8000/docs
```

## Captura de Logs

O projeto implementa captura estruturada de logs para rastrear eventos em todas as camadas da aplicação:

### Backend
- Utiliza o módulo `logging` nativo do Python com configuração de rotação de arquivos.
- Registra requisições à API, execução de agentes, erros e tempos de processamento.
- Armazenamento: `logs/app.log`

### Frontend
- Logs de interação do usuário e chamadas à API via `console.log` estruturado no JavaScript.
- Registro de alternância de tema, validação de formulário e respostas da API.
- Exibição direta no console do navegador para depuração.

### Integração
- Captura de logs de comunicação entre frontend e backend, incluindo tempos de resposta e erros de rede.
- Registro de fallback entre heurística local e LLM (se configurado).

## Testes da Aplicação

O projeto possui testes automatizados para validar tanto o backend (Python) quanto a lógica do frontend (JavaScript).

### Testes Backend (Python)

Localização: `tests/test_agents.py`

Testa os agentes de IA, modelos Pydantic e integração da API.

```bash
# Executar testes Python
cd my-travel-ai
python -m pytest tests/test_agents.py -v
```

### Testes Frontend (JavaScript/UI)

Como o ambiente pode não ter Node.js, criamos testes em Python que simulam a lógica das funções JavaScript:

**Localização**: `tests/test_js_functions.py`

**O que é testado**:
- ✅ `formatCurrency()` - Formatação de moeda (BRL, USD, null, undefined)
- ✅ `validateForm()` - Validação de formulário (campos obrigatórios, datas)
- ✅ `getPreferredTheme()` - Detecção de tema (localStorage, preferência do sistema)
- ✅ `applyTheme()` - Aplicação de tema e salvamento
- ✅ `toggleTheme()` - Alternância dark/light mode
- ✅ Sintaxe do arquivo JavaScript
- ✅ Integração completa (validar → formatar)

```bash
# Executar testes das funções JavaScript
cd my-travel-ai
python tests/test_js_functions.py
```

**Saída esperada**:
```
🧪 Executando testes das funções JavaScript...

📋 TestFormatCurrency
--------------------------------------------------
  ✅ test_format_negative_value
  ✅ test_format_null_value
  ...

📊 Resultado: 20/20 testes passaram
```

### Testes JavaScript Nativos (Jest - Opcional)

Caso tenha Node.js instalado, há configuração para testes nativos em Jest:

**Arquivos**: `package.json` e `tests/index.test.js`

```bash
# Instalar dependências (apenas primeira vez)
npm install

# Executar testes Jest
npm test
```

### Testes de Integração

Valida o fluxo completo de ponta a ponta da aplicação, garantindo a comunicação correta entre todas as camadas:

**Localização**: `tests/test_integration.py`

**O que é testado**:
- ✅ Fluxo completo: Envio de formulário → Processamento de agentes → Exibição de resultados
- ✅ Integração frontend-backend via chamadas à API REST
- ✅ Fallback entre heurística local e LLM (se `GEMINI_API_KEY` estiver configurada)
- ✅ Tratamento de erros parciais e resiliência do maestro

```bash
# Executar testes de integração
cd my-travel-ai
python -m pytest tests/test_integration.py -v
```

## Como Executar Todos os Testes

```bash
# 1. Testes Python (Backend)
python -m pytest tests/test_agents.py -v

# 2. Testes das funções JavaScript (Python)
python tests/test_js_functions.py

# 3. Testes Jest (se tiver Node.js)
npm test

# 4. Testes de Integração
python -m pytest tests/test_integration.py -v
```

## Projeto

Planejamento do protótipo da solução disponível em [planos](planos)

Telas disponíveis em [docs/telas](docs/telas)

Imagem de serviços de API disponível em [docs/servicos](docs/servicos)

Testes automáticos disponíveis em:
- Backend: [tests/test_agents.py](tests/test_agents.py)
- Frontend/UI: [tests/test_js_functions.py](tests/test_js_functions.py)
- Jest (opcional): [tests/index.test.js](tests/index.test.js)

## Informações

Dúvidas, mais informações ou sugestões envie um e-mail para armando@ufpi.edu.br

Observação: esta aplicação é apenas um protótipo didático para trabalhar os conceitos básicos de Agentes de IA Generativa, não use em produção.
