# Descrição

- prompt.md: prompt base para criar os arquivos plano.md e skill.md
- plano.md: Plano base para criar os agentes da aplicação
- skill.md: skill base para criar os prompts de cada agente da aplicação
- plano_implementacao.md: plano de implementação gerado pelo Antigravity usando o Modelo Gemini Flash 3.5
- tarefas_plano_implementacao.md: tarefas do plano de implementação gerado pelo plano_implementacao.md

## Prompt de criação da aplicação do TravelAI

Use o seguinte prompt para criar a aplicação TravelAI em um Agente de Código (exemplo: Google Antigravity)

```bash
Baseado no plano @plano.md e na skill @skill.md você pode criar uma aplicação de agente de viagem que o usuário informa uma cidade de destino, uma cidade de origem, uma data de início de viagem, a data de final da viagem e a aplicação mostre possíveis cenários de pacote aéreo, pacote de hotel e roteiro de turismo. Procure usar frameworks opersource e ferramentas oper source baseados na linguagem python.
```
