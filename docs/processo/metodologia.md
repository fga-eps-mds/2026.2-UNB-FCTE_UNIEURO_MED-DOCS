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

O detalhamento está na [EAP](../EAP.md), no
[Roadmap do Produto](roadmap.md), no [Cronograma](cronograma.md) e no
[Plano de Custos](plano_de_custos.md).

### 4.2 Histórias, tarefas e defeitos

Necessidades funcionais são registradas como histórias de usuário, no formato
"Como *perfil*, quero *ação*, para que *benefício*". Trabalho técnico, gerencial ou
documental é registrado como tarefa. Defeitos encontrados durante verificação ou
uso são registrados como relatos de bug.

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
- tamanho suficientemente pequeno para ser verificado dentro da sprint.

Um item só é considerado **concluído** quando:

- seus critérios de aceitação foram atendidos;
- a mudança foi submetida por Pull Request vinculado à issue;
- as verificações pertinentes foram executadas e registradas;
- o pipeline aplicável foi aprovado;
- pelo menos outra pessoa revisou a mudança;
- a alteração foi integrada à branch de integração correta;
- documentação e quadro refletem a situação real;
- quando aplicável, o PO ou cliente validou o comportamento entregue.

Trabalho iniciado, código existente apenas em branch ou PR ainda não integrado não
é contabilizado como valor concluído.

## 5. Execução em sprints

### 5.1 Cadência

O semestre está organizado em oito sprints, em geral com duas semanas, agrupadas
nas releases R1, R2, R3 e release final. Datas, objetivos, dependências e resultados
demonstráveis estão definidos no [Roadmap do Produto](roadmap.md).

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

### 5.2 Eventos e evidências

| Evento | Participantes principais | Objetivo | Evidência esperada |
|---|---|---|---|
| Planejamento da sprint | Equipe e liderança do período | Definir objetivo e selecionar trabalho pronto | Sprint e issues atualizadas no Zenhub |
| Alinhamento recorrente | Equipe | Comunicar progresso e impedimentos | Quadro atualizado e responsáveis acionados |
| Revisão técnica | Autor e revisor do PR | Verificar correção, clareza, testes e arquitetura | Comentários, aprovação e checks do PR |
| Review | Equipe, PO e/ou cliente | Demonstrar valor e obter aceite ou ajustes | Feedback, decisão e pendências registrados |
| Retrospectiva | Equipe | Melhorar a forma de trabalho | Ação de melhoria com responsável |

Os encontros com PO e cliente que geram decisões de produto são registrados nas
[atas de reunião](../atas-reunioes/index.md). Conversas que alterem escopo,
prioridade, prazo ou responsabilidade devem ser refletidas na issue ou no artefato
correspondente; a mensagem no canal, isoladamente, não registra a decisão.

### 5.3 Papéis e responsabilidades

| Papel ou grupo | Responsabilidade na metodologia |
|---|---|
| PO e cliente | Esclarecer necessidades, priorizar valor e validar incrementos |
| Liderança do período | Facilitar a sprint, acompanhar impedimentos e manter comunicação com o PO |
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

O Zenhub, integrado ao GitHub, representa o estado real do trabalho. Itens futuros
permanecem no backlog; itens selecionados formam o backlog da sprint; itens em
execução possuem responsável; mudanças submetidas aguardam revisão; somente itens
que satisfazem os critérios de conclusão chegam ao estado final.

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
| Aplicativo | Lint/build, testes automatizados relacionados e verificação do fluxo alterado |
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

## 10. Métodos e técnicas de apoio

Esta tabela mostra onde cada elemento contribui para o ciclo, em vez de apresentar
definições isoladas.

| Método ou técnica | Papel no ciclo | Evidência |
|---|---|---|
| Lean Inception | Alinhar problema, pessoas, funcionalidades, hipóteses e MVP | Visão do Produto e Canvas MVP |
| EAP | Delimitar e decompor o escopo | Estrutura Analítica do Projeto |
| Histórias de usuário | Transformar necessidades em valor verificável | Product Backlog e issues |
| Scrum adaptado | Organizar planejamento, entrega, validação e melhoria | Sprints, incrementos, reviews e retrospectivas |
| Gestão visual | Tornar fluxo, prioridade e bloqueios visíveis | Zenhub e histórico das issues |
| Prototipação | Antecipar validação de telas e acessibilidade | Figma e referências nas histórias |
| Revisão por pares e CI | Fornecer feedback antes da integração | PR, aprovação e checks |
| EVM-Ágil | Integrar escopo, prazo e custo | Indicadores e auditoria do dashboard |
| Velocity e burnup | Analisar ritmo e mudança de escopo | Zenhub e dashboard |
| Gestão de riscos | Antecipar eventos incertos e acompanhar respostas | Registro e matriz de riscos |
| SonarCloud e testes | Acompanhar qualidade e regressões | Métricas e resultados dos testes |
| Atas e decisões | Preservar contexto, autoria e justificativa | Atas, issues e histórico documental |

## 11. Referências

CAROLI, Paulo. *Lean Inception: como alinhar pessoas e construir o produto certo*.

COHN, Mike. *User Stories Applied: For Agile Software Development*. Boston:
Addison-Wesley, 2004.

SCHWABER, Ken; SUTHERLAND, Jeff. *O Guia do Scrum*. 2020. Disponível em:
<https://scrumguides.org/>.

SULAIMAN, Tamara; BARTON, Brent; BLACKBURN, Thomas. AgileEVM: Earned Value
Management in Scrum Projects. In: *Agile Conference*, 2006. IEEE, 2006.

## Histórico de Versões

| Versão | Descrição | Autor(es) | Data | Revisor(es) | Data de Revisão |
|---|---|---|---|---|---|
| 1.0 | Criação do documento de metodologias e técnicas | [Thales Germano](https://github.com/thalesgvl) | 21/09/2026 | | |
| 1.1 | Reestruturação como metodologia integrada, com ciclo, papéis, critérios, qualidade, medição e adaptação | [Daniel Ferreira Nunes](https://github.com/Mach1r0) | 25/09/2026 | | |
