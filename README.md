# Instruções

Este é um **protótipo** de IA multiagente com interface web. Algumas funcionalidades não estão completamente implementadas, pois o objetivo deste protótipo é demonstrar como agentes de IA podem funcionar utilizando modelos de LLM.  

## Funcionalidades Implementadas
- 4 agentes modulares (maestro, agente_aereo, agente_hotel, agente_turismo)
- Execução paralela dos 3 agentes especialistas via concurrent.futures
- Engine híbrida: Heurística local por padrão + Gemini LLM se GEMINI_API_KEY estiver configurada
- Base de conhecimento rica para 7 destinos populares (Lisboa, Paris, Nova York, Miami, Buenos Aires, Roma + genérico)
- Interface premium com Glassmorphism, dark mode, animação dos agentes em tempo real e 4 abas de resultado
- Validação completa de datas, resiliência a falhas parciais

## Execução

```bash
export GEMINI_API_KEY=sua_chave_aqui
./run.sh
```

Saída esperada

```bash
🚀 Iniciando servidor em http://localhost:8000
   Acesse a interface web em http://localhost:8000
   Documentação da API em   http://localhost:8000/docs
```

## Projeto

Planejamento do protótipo da solução disponível em [planos](planos)

Telas disponíveis em [docs/telas](docs/telas)

Imagem de serviços de API disponível em [docs/servicos](docs/servicos)      

Testes automáticos disponíveis em [tests/test_agents.py](tests/test_agents.py)

## Informações

Dúvidas, mais informações ou sugestões envie um e-mail para armando@ufpi.edu.br

Observação: esta aplicação é apenas um protótipo didático para trabalhar os conceitos básicos de Agentes de IA Generativa, não use em produção.
