---
title: Metodologia
---

# Metodologia do Projeto

## 1. Finalidade

Este documento descreve **como a equipe organiza e executa o trabalho do projeto**,
desde a descoberta do produto até a validação de cada incremento. Os métodos e as
técnicas adotados não são atividades isoladas: eles formam um ciclo integrado de
decisão, desenvolvimento, verificação e aprendizado.

A metodologia foi adaptada ao contexto do MED:

- projeto acadêmico desenvolvido ao longo de um semestre;
- produto construído com participação do *Product Owner* e do cliente;
- equipe distribuída entre Produto/UX, Mobile, Dados/IA, Qualidade e DevOps;
- três repositórios, com responsabilidades e branches de integração diferentes;
- entregas incrementais organizadas em sprints e releases;
- funcionamento do aplicativo e da inferência 100% offline;
- necessidade de acompanhar escopo, prazo, custo, qualidade e riscos.

O objetivo dessa combinação é manter o produto alinhado à necessidade do cliente,
permitir mudanças de forma rastreável e produzir evidências de que cada entrega foi
construída, verificada e validada.

As práticas não foram criadas pela equipe. Elas vêm do Scrum, do XP, do Kanban, do
PMBOK e da *Lean Inception*, com adaptações ao contexto acima. A
[seção 10](#10-origem-das-praticas-e-adaptacoes) mostra a origem de cada prática e
como o time a aplica, e a [seção 5.1](#51-fases-do-semestre-o-planejado-e-o-praticado)
compara o processo planejado com o que foi de fato praticado no semestre.

## 2. Ciclo de trabalho

O projeto percorre continuamente seis etapas. Embora a descoberta tenha maior
intensidade no início do semestre, novas informações podem fazer a equipe retornar a
etapas anteriores.

| Etapa | Como acontece no MED | Entrada | Saída esperada |
|---|---|---|---|
| **1. Descobrir** | Equipe, PO e cliente discutem problema, pessoas usuárias, jornadas, restrições e hipóteses | Necessidade apresentada pelo cliente | Visão compartilhada e hipóteses registradas |
| **2. Delimitar e priorizar** | Funcionalidades são avaliadas por valor, esforço e experiência; o MVP é organizado em ondas | Visão e hipóteses | Canvas MVP, sequenciador e Product Backlog priorizado |
| **3. Planejar** | Histórias e tarefas são selecionadas conforme prioridade, dependências e capacidade | Backlog priorizado e resultados da sprint anterior | Objetivo e backlog da sprint |
| **4. Desenvolver** | O trabalho é executado em branches, acompanhado no Zenhub e integrado por Pull Request | Item pronto para desenvolvimento | Incremento implementado e revisado |
| **5. Verificar e validar** | Pipelines, testes, revisão e demonstração confrontam a entrega com os critérios de aceitação | Incremento desenvolvido | Evidências técnicas e aceite ou ajustes solicitados |
| **6. Medir e adaptar** | A equipe analisa entrega, prazo, custo, qualidade, riscos e feedback | Dados da sprint e feedback | Backlog, processo e planos atualizados |

O encadeamento principal é:

> Visão do Produto → funcionalidades → sequenciador → Canvas MVP →
> Product Backlog → sprint → incremento → verificação e validação →
> medição e adaptação.

## 3. Descoberta e definição do produto

A descoberta utiliza a Lean Inception para construir entendimento compartilhado
antes de transformar necessidades em trabalho de desenvolvimento. A equipe não
considera a dinâmica encerrada apenas porque os quadros foram preenchidos: suas
decisões precisam aparecer no backlog, no roadmap e nos incrementos.

No MED, a descoberta ocorreu em reuniões com o PO, o cliente e o professor, entre
agosto e setembro de 2026. As decisões estão registradas nas
[atas de reunião](../atas-reunioes/index.md) e foram consolidadas nos seguintes
artefatos:

| Decisão necessária | Técnica utilizada | Evidência produzida |
|---|---|---|
| Qual problema resolver, para quem e com qual diferencial | Visão do Produto | [Síntese da Visão](../produto/visao.md) |
| O que o produto é, faz e não faz | É / Não é / Faz / Não faz | [Lean Inception](../produto/lean-inception.md) |
| Quem usa o produto e em qual contexto | Personas e jornadas | [Lean Inception](../produto/lean-inception.md) |
| Quais soluções podem atender às necessidades | Brainstorming de funcionalidades | [Funcionalidades](../produto/funcionalidades.md) |
| O que entrega maior valor com esforço e risco aceitáveis | Revisão técnica, de negócio e de UX | [Funcionalidades](../produto/funcionalidades.md) |
| Qual é a ordem incremental de entrega | Sequenciador | [Sequenciador](../produto/sequenciador.md) |
| Qual recorte permite validar as principais hipóteses | Canvas MVP | [Canvas MVP](../produto/canvas-mvp.md) |

Uma nova informação do cliente só altera o produto depois que seu impacto sobre
escopo, arquitetura, prazo, custo e riscos é discutido. A decisão é registrada em
ata ou issue e, quando aprovada, atualiza os artefatos afetados e o backlog.

## 4. Do escopo ao planejamento

### 4.1 Integração dos planos

A Estrutura Analítica do Projeto (EAP) delimita o escopo total em entregas e
pacotes de trabalho. Esses pacotes orientam a criação de épicos, histórias e tarefas.
O roadmap distribui resultados ao longo das sprints e releases, enquanto o plano
de custos associa o período à linha de base acompanhada por EVM-Ágil.

| Artefato | Pergunta respondida | Como orienta a execução |
|---|---|---|
| EAP | Qual é o escopo total? | Define entregas e fronteiras do projeto |
| Product Backlog | Qual valor ainda precisa ser entregue? | Mantém histórias priorizadas e critérios de aceitação |
| Roadmap | Em que sequência os resultados serão demonstrados? | Relaciona ondas, sprints, releases e resultados esperados |
| Cronograma | Quais são os marcos e prazos? | Estabelece datas de demonstração e entrega |
| Plano de Custos | Qual é a linha de base econômica? | Permite comparar valor planejado, agregado e custo real |
| Plano de Qualidade | Como comprovar a qualidade do incremento? | Define metas, evidências e resposta a desvios |

O detalhamento está na [EAP](../EAP.md), no
[Roadmap do Produto](roadmap.md), no [Cronograma](cronograma.md), no
[Plano de Custos](plano_de_custos.md) e no [Plano de Qualidade](plano_de_qualidade.md).

### 4.2 Histórias, tarefas e defeitos

Necessidades funcionais são registradas como histórias de usuário, no formato
"Como *perfil*, quero *ação*, para que *benefício*", com critérios de aceitação
escritos como cenários BDD ("Dado que…, quando…, então…"). Trabalho técnico,
gerencial ou documental é registrado como tarefa. Defeitos encontrados durante
verificação ou uso são registrados como relatos de bug.

Só as histórias de usuário recebem pontos de estimativa. Tarefas e defeitos não são
pontuados, para que a *velocity* meça apenas o valor entregue ao usuário.

Os itens são mantidos como issues para preservar autoria, discussão, dependências,
responsabilidade e ligação com Pull Requests. O backlog é repriorizado quando o
cliente altera uma necessidade, um risco se materializa, uma dependência bloqueia
o trabalho ou uma medição indica desvio relevante.

### 4.3 Critérios de entrada e conclusão

Um item está **pronto para entrar em uma sprint** quando possui:

- objetivo ou valor esperado compreensível;
- critérios de aceitação observáveis;
- repositório e responsáveis identificados;
- prioridade, dependências e impedimentos conhecidos;
- referências de produto, arquitetura ou protótipo quando necessárias;
- tamanho suficientemente pequeno para ser verificado dentro da sprint;
- no caso de história de usuário, o rótulo `validada pelo PO`, com o aval do PO e do
  cliente registrado no Discord (ver [seção 5.1](#51-fases-do-semestre-o-planejado-e-o-praticado)).

Um item só é considerado **concluído** quando:

- seus critérios de aceitação foram atendidos;
- a mudança foi submetida por Pull Request vinculado à issue;
- as verificações pertinentes foram executadas e registradas;
- o pipeline aplicável foi aprovado;
- pelo menos outra pessoa revisou a mudança;
- a alteração foi integrada à branch de integração correta;
- documentação e quadro refletem a situação real;
- no caso de história de usuário, o PO aceitou a entrega no teste de aceitação. Até
  esse aceite, a história fica na coluna **Aceitação PO** do Zenhub, mesmo com o PR
  já integrado.

Trabalho iniciado, código existente apenas em branch ou PR ainda não integrado não
é contabilizado como valor concluído.

## 5. Execução em sprints

### 5.1 Fases do semestre: o planejado e o praticado

O [Roadmap do Produto](roadmap.md) previa desenvolvimento desde a Sprint 1, iniciada
em 31/08. Na prática, o semestre teve duas fases, e a avaliação da R1
([Ata 08](../atas-reunioes/Ata-08-EPS-2026-10-02-PO.md)) apontou essa distância entre
o documentado e o praticado.

| Fase | Período | O que aconteceu |
|---|---|---|
| **Preparação** | 31/08 a 24/09 (Sprints 1 e 2) | Descoberta com a *Lean Inception*, visão do produto, identidade visual, protótipo de alta fidelidade no Figma e histórias da primeira release com critérios em BDD. A validação com o PO e o cliente aconteceu em 23/09 ([Ata 07](../atas-reunioes/Ata-07-EPS-2026-09-23-PO.md)), com as últimas respostas no Discord até 24/09. |
| **Desenvolvimento** | A partir de 23/09 | O código das histórias começou depois da validação, em sprints de duas semanas. A R1 foi apresentada em 02/10, e a Release Minor 1 sai em 13/10. |

Na mesma avaliação, o professor observou que requisitos e protótipos foram
detalhados em cascata, todos antes do desenvolvimento, que histórias foram fechadas
sem o aceite do PO e que o quadro do Zenhub não aparecia nas reuniões. Desde então, o
processo praticado é este:

- **Validação semanal das histórias.** A cada semana, a equipe envia ao PO e ao
  cliente, pelo Discord, o link das histórias da próxima leva, com o protótipo
  anexado. A implementação só começa depois do aval, marcado na issue pelo rótulo
  `validada pelo PO`. O ideal é enviar com uma semana de antecedência (Ata 07). Assim,
  cada história é detalhada pouco antes de ser implementada, e não todas no início.
- **Entrega contínua ao PO.** O APK vai para o PO sempre que uma funcionalidade fica
  pronta, sem esperar o fim da sprint, junto com o instrumento de teste de aceitação
  ([Ata 09](../atas-reunioes/Ata-09-EPS-2026-10-05-PO.md)).
- **Aceite antes de fechar.** Uma história integrada fica na coluna Aceitação PO até o
  PO aceitá-la no teste de aceitação. Só então ela vai para Done.
- **Quadro nas reuniões.** O quadro do Zenhub é mostrado na reunião semanal com o PO.

### 5.2 Cadência

O semestre está organizado em oito sprints, em geral com duas semanas, agrupadas
nas releases R1, R2, R3 e release final. Datas, objetivos, dependências e resultados
demonstráveis estão definidos no [Roadmap do Produto](roadmap.md).

Cada sprint é conduzida por uma dupla de liderança, que se alterna a cada duas
semanas, conforme a escala da [Visão Operacional](../equipe/operacional.md). A equipe
se reúne com o PO e o cliente toda segunda-feira, pelo Microsoft Teams.

Cada sprint percorre o seguinte ciclo:

1. **Planejar:** analisar resultados anteriores, confirmar o objetivo e selecionar
   itens prontos conforme prioridade, dependências e capacidade.
2. **Executar e acompanhar:** desenvolver os itens e manter issues, responsáveis,
   impedimentos e PRs atualizados no GitHub e no Zenhub.
3. **Verificar:** executar revisão, build, testes e análises antes da integração.
4. **Validar:** demonstrar o incremento e confrontá-lo com os critérios de
   aceitação e as necessidades do PO e do cliente.
5. **Inspecionar e adaptar:** analisar métricas, riscos, acertos, falhas e
   impedimentos; registrar ações para a sprint seguinte.

### 5.3 Eventos e evidências

| Evento | Participantes principais | Objetivo | Evidência esperada |
|---|---|---|---|
| Planejamento da sprint | Equipe e dupla de liderança | Definir objetivo e selecionar trabalho pronto | Sprint e issues atualizadas no Zenhub |
| Validação das histórias | Equipe, PO e cliente | Conferir critérios de aceitação e protótipo antes da implementação | Aval no Discord e rótulo `validada pelo PO` na issue |
| Alinhamento recorrente | Equipe | Comunicar progresso e impedimentos | Quadro atualizado e responsáveis acionados |
| Revisão técnica | Autor e revisor do PR | Verificar correção, clareza, testes e arquitetura | Comentários, aprovação e checks do PR |
| Reunião semanal com o PO | Equipe, PO e cliente | Demonstrar o incremento com o quadro do Zenhub aberto e decidir os próximos passos | Ata da reunião |
| Teste de aceitação | PO e cliente | Conferir no APK os cenários BDD das histórias entregues | Formulário de aceitação respondido e comentário na issue |
| Retrospectiva | Equipe | Melhorar a forma de trabalho | Ação de melhoria com responsável |

Os encontros com PO e cliente que geram decisões de produto são registrados nas
[atas de reunião](../atas-reunioes/index.md). Conversas que alterem escopo,
prioridade, prazo ou responsabilidade devem ser refletidas na issue ou no artefato
correspondente; a mensagem no canal, isoladamente, não registra a decisão.

### 5.4 Papéis e responsabilidades

| Papel ou grupo | Responsabilidade na metodologia |
|---|---|
| PO (Vinícius de Carvalho Rispoli) e cliente (Arthur Dutra do Bomfim) | Esclarecer necessidades, priorizar valor, validar as histórias antes da implementação e aceitar os incrementos no teste de aceitação |
| Dupla de liderança | Faz o papel que o Scrum atribui ao *Scrum Master*: facilitar a sprint, conduzir as reuniões, acompanhar impedimentos e manter a comunicação com o PO. A dupla se alterna a cada duas semanas |
| Responsáveis pelo item | Implementar, manter a issue atualizada, produzir evidências e responder à revisão |
| Revisor | Conferir mudança, riscos e verificações, solicitando correções quando necessário |
| Produto/UX | Manter coerência entre necessidade, fluxo, protótipo, acessibilidade e backlog |
| Mobile | Implementar e verificar a experiência executada no tablet |
| Dados/IA | Preparar, avaliar e exportar o modelo com rastreabilidade experimental |
| Qualidade/DevOps | Apoiar testes, pipelines, métricas, releases e evidências de qualidade |

A qualidade é compartilhada: a frente de Qualidade/DevOps apoia o processo, mas
autor e revisor continuam responsáveis pela entrega que integram.

## 6. Gestão visual e comunicação

### 6.1 Fluxo de trabalho

O Zenhub, integrado ao GitHub, representa o estado real do trabalho. O quadro segue o
Kanban: cada coluna é uma etapa do fluxo, e quem termina uma etapa puxa o próximo
item. As colunas são:

> Product Backlog → Sprint Backlog → In Progress → Review/QA → Aceitação PO → Done

Itens futuros permanecem no Product Backlog; itens selecionados formam o Sprint
Backlog; itens em execução possuem responsável; mudanças submetidas aguardam revisão
em Review/QA; histórias integradas esperam o aceite do PO em Aceitação PO; somente
itens que satisfazem os critérios de conclusão chegam a Done. A equipe ainda não
definiu limites de WIP para as colunas.

O quadro é usado para tornar prioridade e responsabilidade visíveis, identificar
bloqueios e PRs parados, planejar conforme a capacidade e manter rastreabilidade
entre backlog, issue, PR e release. O quadro está no
[workspace do Zenhub](https://app.zenhub.com/workspaces/unbfcte-unieuromed-6a8c447d652b15002979b829/board).

### 6.2 Canais e registro

| Canal | Uso principal | Registro permanente quando necessário |
|---|---|---|
| WhatsApp | Alinhamento cotidiano e comunicação rápida | Issue, PR ou ata |
| Discord | Alinhamento com PO e discussões síncronas | Issue, decisão de produto ou ata |
| GitHub | Discussão e rastreabilidade técnica | A própria issue, PR ou commit |
| Zenhub | Priorização e acompanhamento | Issue associada |
| Figma | Construção e validação visual | Link no documento ou na história |

Decisões relevantes não permanecem somente em mensagens. Mudanças de requisito,
aceites, riscos, impedimentos e justificativas precisam chegar ao mecanismo de
rastreabilidade adequado.

## 7. Desenvolvimento, integração e qualidade

### 7.1 Fluxo de contribuição

Cada alteração parte de uma issue e segue este fluxo:

1. confirmar escopo, critérios de aceitação e repositório afetado;
2. criar uma branch a partir da branch de integração correta;
3. produzir uma mudança pequena e verificável, com commits semânticos;
4. executar localmente as verificações pertinentes;
5. abrir PR vinculado à issue, explicando como verificar a mudança;
6. obter pipeline aprovado e revisão de pelo menos outra pessoa;
7. corrigir problemas encontrados ou registrar limitações aceitas;
8. integrar a mudança e atualizar issue, documentação e quadro.

No MED-DOCS, as branches partem de `main` e usam `docs/`, `fix/` ou `chore/`,
conforme o [Guia de Contribuição](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-DOCS/blob/main/CONTRIBUTING.md).
No MED-APP e no MED-IA,
as branches de trabalho partem de `develop` e os PRs apontam para `develop`; as
regras específicas de cada repositório prevalecem.

### 7.2 Verificação proporcional à mudança

| Tipo de entrega | Verificação mínima esperada |
|---|---|
| Documentação | Build do MkDocs, links e navegação conferidos, histórico atualizado quando aplicável |
| Aplicativo | Lint e formatação, testes automatizados escritos por quem implementa, cobertura acima do piso do `jest.config.js` e verificação do fluxo alterado no emulador ou no tablet |
| Modelo de IA | Script reexecutável, versão dos dados, parâmetros, semente, divisão e métricas registradas |
| Pipeline | Execução bem-sucedida e evidência do artefato ou métrica produzido |
| Integração APP–IA | Contrato versionado, execução offline e teste no dispositivo-alvo |

Testes automatizados reduzem regressões, mas não substituem a validação com o PO
nem os testes funcionais no tablet. Cobertura elevada também não basta se os
comportamentos críticos não forem exercitados.

### 7.3 Integração contínua e documentação como código

Documentação, aplicativo e projeto de IA são versionados. Os pipelines fornecem
feedback antes da integração e geram evidências compatíveis com cada repositório.
Falha de build, teste ou análise obrigatória impede que o item seja considerado
concluído.

No MED-APP, o pipeline de build roda em todo PR o lint, a verificação de formatação,
os testes com cobertura e a análise do SonarCloud. Cada merge na `develop` ou na
`main` gera uma release com as métricas do SonarCloud anexadas, e o rótulo do PR
define a versão: `MAJOR RELEASE` para as releases R1, R2 e R3, `MINOR RELEASE` para
as releases intermediárias e nenhum rótulo para correções.

Branches, commits, issues, PRs, checks e releases compõem a trilha de auditoria.
Credenciais e dados de pacientes não fazem parte dela e nunca são versionados.

## 8. Monitoramento e tomada de decisão

O dashboard consolida dados de planejamento, entrega e qualidade. As métricas não
são produzidas apenas para exposição: elas devem provocar análise e, quando
necessário, uma ação rastreável.

| Dimensão | Evidência | Pergunta para decisão | Resposta esperada a desvio |
|---|---|---|---|
| Escopo | Backlog, itens adicionados e pontos aceitos | O escopo mudou ou o valor planejado foi entregue? | Repriorizar, negociar corte ou atualizar linha de base |
| Prazo | Velocity, burnup, PV, EV e SPI | O ritmo permite cumprir a release? | Remover impedimento, rever capacidade ou replanejar escopo |
| Custo | BAC, AC, CPI, CV e EAC | O custo permanece coerente com o valor entregue? | Investigar e seguir o controle de mudanças do plano de custos |
| Qualidade | Testes, cobertura, bugs e SonarCloud | O incremento está verificável e sustentável? | Corrigir, aumentar testes ou priorizar dívida técnica |
| Processo | Pipelines, PRs e bloqueios | O fluxo fornece feedback em tempo adequado? | Corrigir pipeline, redistribuir revisão ou reduzir itens |
| Riscos | Probabilidade, impacto e resposta | Algum risco mudou ou se materializou? | Executar resposta, designar responsável e atualizar plano |

Os limites de atenção para CPI e SPI e o processo de alteração da linha de base
estão no [Plano de Custos](plano_de_custos.md). Uma decisão orientada por dados
registra contexto, indicador, interpretação, ação escolhida e responsável.

Dados ausentes ou simulados precisam ser identificados como tal. Uma visualização
não deve induzir a equipe a tratar estimativas como resultado real.

## 9. Inspeção e adaptação da metodologia

Ao final de cada ciclo, a equipe confronta o processo planejado com o ocorrido:

1. identifica resultado, desvio ou impedimento relevante;
2. investiga sua causa, sem limitar a análise ao sintoma;
3. define uma ação pequena e verificável;
4. atribui responsável e prazo;
5. verifica na retrospectiva seguinte se a ação teve o efeito esperado;
6. incorpora ao processo as mudanças que se mostrarem úteis.

Exemplos incluem alterar pareamentos, dividir histórias grandes, antecipar uma
prova técnica, reforçar testes de um fluxo crítico ou mudar a coleta de uma métrica
pouco confiável.

Quando a adaptação modificar uma regra permanente, este documento ou o guia do
repositório é atualizado. Quando afetar produto, prazo, custo ou arquitetura, os
respectivos artefatos também são revisados.

## 10. Origem das práticas e adaptações

Nenhuma prática foi criada pela equipe. A tabela abaixo indica, para cada uma, o método
de onde ela vem, como o MED a adapta e onde fica a evidência. As referências completas
estão na [seção 11](#11-referencias).

| Prática | Origem | Como o MED adapta | Evidência |
|---|---|---|---|
| Visão do produto, personas, jornadas, sequenciador e Canvas MVP | *Lean Inception* (Caroli, 2018) | A oficina, que a *Lean Inception* propõe em uma semana, foi distribuída em reuniões com o PO e o cliente entre agosto e setembro | [Lean Inception](../produto/lean-inception.md) e [Canvas MVP](../produto/canvas-mvp.md) |
| Sprints, Product Backlog, Sprint Backlog e incremento | Scrum (Schwaber; Sutherland, 2020) | Sprints de duas semanas, agrupadas nas releases da disciplina | [Roadmap do Produto](roadmap.md) e Zenhub |
| Papéis do Scrum | Scrum (Schwaber; Sutherland, 2020) | O PO é um professor de fora da equipe, disponível na reunião semanal. O papel de *Scrum Master* fica com a dupla de liderança, que se alterna a cada duas semanas | [Visão Operacional](../equipe/operacional.md) |
| Eventos do Scrum | Scrum (Schwaber; Sutherland, 2020) | A *review* acontece na reunião semanal com o PO, e não só no fim da sprint. Entre as reuniões, o acompanhamento é feito pelo quadro e pelos canais da equipe | [Atas de reunião](../atas-reunioes/index.md) |
| Histórias de usuário | XP (Beck; Andres, 2004) e Cohn (2004) | Formato "Como…, quero…, para que…", com pontos de estimativa só nas histórias | Issues do MED-APP |
| Critérios de aceitação em cenários | BDD (North, 2006) | Cenários "Dado que…, quando…, então…" em cada história, conferidos pelo PO e pelo cliente antes da implementação | Issues com o rótulo `validada pelo PO` |
| Testes de aceitação | XP (Beck; Andres, 2004) | O PO e o cliente testam o APK com um formulário que tem uma pergunta por cenário BDD. A história só fecha depois do aceite | Formulário de aceitação e coluna Aceitação PO |
| Pequenas releases | XP (Beck; Andres, 2004) | Além das releases da disciplina (R1, R2, R3 e final), há releases intermediárias, e o APK vai ao PO a cada funcionalidade concluída | Releases do MED-APP |
| Integração contínua | XP (Beck; Andres, 2004) e Fowler (2006) | Pipeline com lint, formatação, testes e SonarCloud em todo PR, que bloqueia a integração quando falha | Checks dos PRs ([seção 7.3](#73-integracao-continua-e-documentacao-como-codigo)) |
| Testes automatizados | XP (Beck; Andres, 2004) | Quem implementa escreve os testes do próprio código, com piso de cobertura definido no repositório | Relatórios de teste e cobertura no SonarCloud |
| Padrões de código | XP (Beck; Andres, 2004) | ESLint e Prettier no pipeline e *Conventional Commits* em português | `CONTRIBUTING.md` de cada repositório |
| Programação em par | XP (Beck; Andres, 2004) | Adaptada como estratégia de pareamento: quem tem menos experiência numa tecnologia trabalha com quem tem mais, para reduzir lacunas e a dependência de uma só pessoa | [Visão Operacional](../equipe/operacional.md) |
| Revisão por pares | Prática de engenharia de software, feita por *pull request* | Todo PR tem pelo menos um revisor antes da integração | Comentários e aprovações dos PRs |
| Quadro visual e fluxo puxado | Kanban (Anderson, 2010; Valente, 2020) | Colunas do Zenhub descritas na [seção 6.1](#61-fluxo-de-trabalho), com a coluna Aceitação PO. Os limites de WIP ainda não foram definidos | Zenhub |
| Fluxo contínuo de entregas | Kanban (Anderson, 2010) | O APK vai ao PO quando a funcionalidade fica pronta, sem esperar o fim da sprint | [Ata 09](../atas-reunioes/Ata-09-EPS-2026-10-05-PO.md) |
| EAP, cronograma, custos, riscos, qualidade e comunicações | PMBOK (PMI, 2017) | Um artefato para cada área de conhecimento, mantido no repositório de documentação | [EAP](../EAP.md), [Cronograma](cronograma.md), [Plano de Custos](plano_de_custos.md), [Riscos](riscos.md), [Plano de Qualidade](plano_de_qualidade.md) e atas |
| EVM-Ágil | Sulaiman, Barton e Blackburn (2006) | Integra escopo, prazo e custo no dashboard | Indicadores e auditoria do dashboard |
| *Velocity* e *burnup* | Planejamento ágil (Cohn, 2005) | Acompanham o ritmo e a mudança de escopo | Zenhub e dashboard |
| Prototipação | Design de interação | Telas de alta fidelidade no Figma, anexadas às histórias para a validação | Figma e páginas de protótipo |
| Desenvolvimento assistido por IA | Diretrizes de uso de IA da disciplina | O Claude Code segue o arquivo `CLAUDE.md` do MED-APP: prepara o trabalho, mas não faz push, não abre nem aprova PR e não mescla sem a confirmação de uma pessoa | `CLAUDE.md` do MED-APP |

## 11. Referências

ANDERSON, David J. *Kanban: Successful Evolutionary Change for Your Technology
Business*. Sequim: Blue Hole Press, 2010.

BECK, Kent; ANDRES, Cynthia. *Extreme Programming Explained: Embrace Change*. 2. ed.
Boston: Addison-Wesley, 2004.

CAROLI, Paulo. *Lean Inception: como alinhar pessoas e construir o produto certo*.
São Paulo: Editora Caroli, 2018.

COHN, Mike. *Agile Estimating and Planning*. Upper Saddle River: Prentice Hall, 2005.

COHN, Mike. *User Stories Applied: For Agile Software Development*. Boston:
Addison-Wesley, 2004.

FOWLER, Martin. *Continuous Integration*. 2006. Disponível em:
<https://martinfowler.com/articles/continuousIntegration.html>.

NORTH, Dan. Introducing BDD. *Better Software*, mar. 2006. Disponível em:
<https://dannorth.net/introducing-bdd/>.

PROJECT MANAGEMENT INSTITUTE. *Um guia do conhecimento em gerenciamento de projetos
(Guia PMBOK)*. 6. ed. Newtown Square: PMI, 2017.

SCHWABER, Ken; SUTHERLAND, Jeff. *O Guia do Scrum*. 2020. Disponível em:
<https://scrumguides.org/>.

SULAIMAN, Tamara; BARTON, Brent; BLACKBURN, Thomas. AgileEVM: Earned Value
Management in Scrum Projects. In: *Agile Conference*, 2006. IEEE, 2006.

VALENTE, Marco Tulio. *Engenharia de Software Moderna: princípios e práticas para
desenvolvimento de software com produtividade*. 2020. Cap. 2. Disponível em:
<https://engsoftmoderna.info/cap2.html>.

## Histórico de Versões

| Versão | Descrição | Autor(es) | Data | Revisor(es) | Data de Revisão |
|---|---|---|---|---|---|
| 1.0 | Criação do documento de metodologias e técnicas | [Thales Germano](https://github.com/thalesgvl) | 21/09/2026 | | |
| 1.1 | Reestruturação como metodologia integrada, com ciclo, papéis, critérios, qualidade, medição e adaptação | [Daniel Ferreira Nunes](https://github.com/Mach1r0) | 25/09/2026 | | |
| 1.2 | Inclusão do Plano de Qualidade entre os planos integrados | Equipe MED (proposta para revisão) | 26/09/2026 | Pendente | — |
| 2.0 | Origem das práticas (Scrum, XP, Kanban, PMBOK e *Lean Inception*) e adaptações, fases planejada e praticada do semestre, validação semanal das histórias, aceitação pelo PO e colunas reais do Zenhub, conforme a avaliação da R1 | [Thales Germano](https://github.com/thalesgvl) | 12/10/2026 | | |
