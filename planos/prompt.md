# Prompt Base 

Prompt de criação dos arquivos de plano.md e skill.md

```bash
Você pode criar um plano.md que represente o planejamento de um orquestrador de agentes que permita sugerir um plano de uma viagem 
para um usuário de forma que o usuário deverá informar uma viagem com destino (cidade), data de saída (início) da viagem, data de retorno (final) da viagem, 
para que o usuário possa comprar as passagens aéreas, reservar um hotel e fazer um roteiro turístico com os pontos mais importantes da cidade de destino para cada dia viagem. 
Este plano.md deve ter um agente orquestrador (que será chamado de maestro) que será o agente que vai orquestrar os demais agentes, deverá ter um agente que procure por 
passagens aéreas em sites públicos que consultam preços de passagens aéreas, esse agente será chamado de agente_aereo, este agente recebe a data de início de viagem, 
data de final da viagem e cidade de destino, também terá outro agente que faça busca de preços de hoteis em sites públicos que consultam hoteis, 
este agente será chamado de agente_hotel, este agente recebe a data de início de viagem, data de final da viagem e cidade de destino, 
também terá outro agente que faça a busca dos principais roteiros turísticos de uma cidade destino, tendo como entrada a cidade destino, 
os dias de início e fim de viagem e gerando uma lista dos principais pontos turísticos. 
Neste plano.md deve ser criado baseado em uma skill.md que seja capaz de criar estes quatro agentes 
(agente orquestrador, agente das passagens aéreas, agente do hotel e agente de pontos turísticos), você pode criar o plano.md e 
o skills.md com o máximo de detalhes de forma este plano.md possa ser referência para criar uma aplicação que possa implementar estes 4 (quatro) agentes. 
Crie também uma skill.md com um conjunto de prompts que sejam referência como habilidade para criar esses agentes de forma detalhada e integrada.
```
