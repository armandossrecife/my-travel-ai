# Descrição

- [prompt.md](prompt.md): prompt base para criar os arquivos plano.md e skill.md
- [plano.md](plano.md): Plano base para criar os agentes da aplicação
- [skill.md](skill.md): skill base para criar os prompts de cada agente da aplicação
- [plano_implementacao.md](plano_implementacao.md): plano de implementação gerado pelo Antigravity usando o Modelo Gemini Flash 3.5
- [tarefas_plano_implementacao.md](tarefas_plano_implementacao.md): tarefas do plano de implementação gerado pelo plano_implementacao.md

Observação:
1. Você pode criar os arquivos [plano.md](plano.md) e [skill.md](https://github.com/armandossrecife/my-travel-ai/blob/main/skills/skill.md) usando seu assistente (chat-bot) de IA preferido. Neste exemplo, o [prompt base](prompt.md) foi passado para o ChatGPT usando o modelo GPT 5.5
2. Uma vez criados os arquivos plano.md e skill.md você pode usar uma ferramenta de Agende de Geração de Código ([Antigravity](https://antigravity.google), [Claude Code](https://claude.com/product/claude-code), [OpenCode](https://opencode.ai), [Zed.dev](https://zed.dev)) para criar seu protótipo. Nesta etapa, talvez você precise de crédito extra, dependendo do modelo LLM escolhido e da ferramenta. Aqui você deve trabalhar como um arquiteto de solução, descrevendo os principais componentes, seus relacionamentos, restrições, requisitos funcionais e não-funcionais, stack de tecnologia e etc. Junto com a ferramenta, você deve criar planos, revisá-los, implementá-los e testar os artefatos gerados.  

## Prompt de criação da aplicação do TravelAI

Use o seguinte prompt para criar a aplicação TravelAI em um Agente de Código (exemplo: Google Antigravity)

```bash
Baseado no plano @plano.md e na skill @skill.md você pode criar uma aplicação de agente de viagem que o usuário informa uma cidade de destino, uma cidade de origem, uma data de início de viagem, a data de final da viagem e a aplicação mostre possíveis cenários de pacote aéreo, pacote de hotel e roteiro de turismo. Procure usar frameworks opersource e ferramentas oper source baseados na linguagem python.
```
