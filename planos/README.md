# Descrição

- [prompt.md](prompt.md): prompt base para criar os arquivos plano.md e skill.md
- [plano.md](plano.md): Plano base para criar os agentes da aplicação
- [skill.md](skill.md): skill base para criar os prompts de cada agente da aplicação
- [plano_implementacao.md](plano_implementacao.md): plano de implementação gerado pelo Antigravity usando o Modelo Gemini Flash 3.5
- [tarefas_plano_implementacao.md](tarefas_plano_implementacao.md): tarefas do plano de implementação gerado pelo plano_implementacao.md

Observação:
1. Você pode criar os arquivos [plano.md](plano.md) e [skill.md](https://github.com/armandossrecife/my-travel-ai/blob/main/skills/skill.md) usando seu assistente (chat-bot) de IA preferido. Neste exemplo, o [prompt base](prompt.md) foi passado para o ChatGPT usando o modelo GPT 5.5
2. Uma vez criados os arquivos plano.md e skill.md você pode usar uma ferramenta de Agende de Geração de Código ([Antigravity](https://antigravity.google), [Claude Code](https://claude.com/product/claude-code), [OpenCode](https://opencode.ai), [Zed.dev](https://zed.dev)) para criar seu protótipo.

>Nesta etapa, esteja ciente de que o consumo de créditos/tokens pode variar significativamente, dependendo do modelo de LLM e da ferramenta escolhida.
>
> Atue como um **arquiteto de soluções**, definindo com clareza:
> - **Componentes principais** do sistema e suas interações;
> - **Restrições técnicas** e de negócio;
> - **Requisitos funcionais e não-funcionais**;
> - **Stack tecnológica** recomendada;
> - **Critérios de aceitação** e métricas de sucesso.
>
> Em colaboração com a ferramenta de IA, conduza um ciclo iterativo de: **planejamento → revisão → implementação → teste**, garantindo a qualidade e a aderência dos artefatos gerados aos objetivos do projeto.

## Prompt de criação da aplicação do TravelAI

Use o seguinte prompt para criar a aplicação TravelAI em um Agente de Código (exemplo: Google Antigravity)

```bash
Baseado no plano @plano.md e na skill @skill.md você pode criar uma aplicação de agente de viagem que o usuário informa uma cidade de destino, uma cidade de origem, uma data de início de viagem, a data de final da viagem e a aplicação mostre possíveis cenários de pacote aéreo, pacote de hotel e roteiro de turismo. Procure usar frameworks opersource e ferramentas oper source baseados na linguagem python.
```
