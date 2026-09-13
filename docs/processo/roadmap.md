---
title: Roadmap do Produto
---

# Roadmap do Produto — 2026.2

O roadmap distribui as funcionalidades priorizadas no sequenciador ao longo do semestre, associando-as a objetivos, resultados demonstráveis e às datas oficiais da disciplina. As ondas indicam a ordem de valor do produto; elas **não equivalem** às sprints. A **Release 3**, em 30 de novembro, é a entrega do MVP.

<div class="roadmap-visual" markdown>

<iframe
  src="https://miro.com/app/live-embed/uXjVHn_328k=/?focusWidget=3458764683591261415&amp;embedMode=view_only_without_ui&amp;embedId=893512512440"
  title="Roadmap do produto MED no Miro"
  loading="lazy"
  frameborder="0"
  scrolling="no"
  allow="fullscreen; clipboard-read; clipboard-write"
  allowfullscreen>
</iframe>

</div>

## Marcos oficiais

| Data | Marco | Resultado demonstrável |
|---|---|---|
| **10/08** | Início do projeto | Início da Lean Inception e da preparação técnica. |
| **28/09** | **Release 1 — primeiro fluxo funcional** | O profissional entra no aplicativo, inicia uma avaliação, aplica a tarefa do relógio e salva o resultado localmente. |
| **26/10** | **Release 2 — captura e inferência integradas** | Os três testes são executados, os dados necessários são capturados e uma primeira inferência é realizada localmente. |
| **30/11** | **Release 3 — Entrega do MVP** | O fluxo completo roda localmente no tablet, do login do profissional à apresentação do resultado da triagem. |
| **07/12** | **Release final** | MVP revisado com incrementos prioritários de acessibilidade e documentação final. |
| **14/12** | Encerramento do projeto | APK e artefatos da disciplina entregues; resultados e limitações registrados. |

## Planejamento detalhado

As equipes indicadas abaixo representam **frentes de responsabilidade propostas**. A atribuição nominal deve ser ajustada à organização da equipe.

<div class="roadmap-table" markdown>

| Etapa | Período | Release | Onda | Objetivo | Entregas principais | Dependências | Equipes responsáveis | Critério de conclusão | Riscos | Situação esperada do produto ao final |
|---|---|---|---|---|---|---|---|---|---|---|
| **Preparação — Lean Inception e base do projeto** | 10/08–30/08 | — | Pré-ondas | Alinhar visão, escopo, MVP e base técnica. | Visão, personas, jornada, sequenciador, arquitetura, repositórios, ambiente e backlog inicial. | Disponibilidade dos stakeholders; decisões de produto e tecnologia. | Produto/UX; Arquitetura; DevOps. | MVP delimitado, backlog priorizado e ambiente utilizável pela equipe. | Atraso nas decisões; escopo amplo; acesso tardio ao hardware. | Base organizacional e técnica pronta, ainda sem entrega funcional. |
| **Sprint 1 — Acesso e base local** | 31/08–13/09 | R1 | Onda 1 | Construir a base do aplicativo e iniciar a avaliação. | App Android; banco local; cadastro e autenticação; avaliação local; consentimento; protótipo de desenho. | Preparação concluída; arquitetura e backlog disponíveis. | Mobile; Produto/UX; Qualidade. | Profissional autenticado cria uma avaliação, registra consentimento e acessa a área de desenho. | Persistência local instável; experiência inadequada com caneta. | Esqueleto navegável com início do fluxo de avaliação. |
| **Sprint 2 — Primeiro desenho funcional** | 14/09–27/09 | **R1 · 28/09** | Ondas 1–2 | Entregar o primeiro fluxo vertical funcional. | Instrução do relógio; desenho com caneta; captura inicial; confirmar, apagar e repetir; salvamento local. | Autenticação, avaliação, consentimento e área de desenho da Sprint 1. | Mobile; Produto/UX; Qualidade. | Fluxo do relógio concluído e recuperável localmente em demonstração. | Captura imprecisa; falha ao salvar; interação difícil no tablet. | **Primeiro fluxo funcional pronto para a R1.** |
| **Sprint 3 — Captura e recuperação** | 29/09–11/10 | R2 | Onda 2 | Tornar a captura do processo de desenho completa e confiável. | Pausas, apagamentos e velocidade; salvamento automático; recuperação; formato padronizado; testes no tablet. | Aprendizados da R1; fluxo de desenho e persistência local. | Mobile; Dados/IA; Qualidade. | Eventos capturados no formato acordado e avaliação interrompida retomada sem perda relevante. | Perda ou inconsistência de dados; diferenças entre dispositivos. | Captura robusta, padronizada e recuperável. |
| **Sprint 4 — Três testes e IA inicial** | 12/10–25/10 | **R2 · 26/10** | Onda 2 | Integrar processamento local e completar o fluxo dos testes. | Pentágono e cubo; preparação dos desenhos; características iniciais; modelo embarcado; inferência offline. | Captura padronizada da Sprint 3; modelo e formato de entrada disponíveis. | Mobile; Dados/IA; Qualidade. | Três tarefas executam e produzem primeira inferência sem internet no dispositivo-alvo. | Desempenho insuficiente; incompatibilidade do modelo; resultado inconsistente. | **Captura e inferência integradas, prontas para a R2.** |
| **Sprint 5 — Pontuação e resultados** | 27/10–08/11 | R3 | Onda 3 | Construir o fluxo completo de pontuação e resultado. | Escores por tarefa e geral; faixa e incerteza; resultado do profissional; encerramento do paciente sem escore. | Inferência local integrada na R2; regras de pontuação validadas. | Dados/IA; Mobile; Produto/UX. | Escores e incerteza são exibidos ao perfil correto; paciente não visualiza o escore. | Interpretação ambígua; exposição indevida; regras não validadas. | Resultado clínico apresentado com separação adequada de perfis. |
| **Sprint 6 — Integração do MVP** | 09/11–22/11 | R3 | Onda 3 | Integrar e estabilizar todos os componentes do MVP. | Fluxo ponta a ponta; exportação anonimizada; validação offline; testes de integração e E2E; APK candidato. | Fluxos de testes, inferência, pontuação e telas de resultado. | Mobile; Dados/IA; Qualidade/DevOps; Produto/UX. | APK candidato conclui o fluxo inteiro offline e passa pelos testes críticos. | Falhas entre módulos; vazamento de dados; regressões; APK instável. | Versão candidata do MVP integrada e testável. |
| **Sprint 7 — Validação e entrega do MVP** | 23/11–29/11 | **R3 · 30/11** | Onda 3 | Validar e entregar o MVP. | Correções prioritárias; testes no tablet e caneta; demonstração; documentação da R3; APK funcional. | APK candidato da Sprint 6; hardware e stakeholders disponíveis. | Todas as frentes; Qualidade coordena a validação. | Defeitos bloqueadores resolvidos, demonstração aprovada e APK/documentação entregues. | Defeito crítico tardio; indisponibilidade do hardware ou stakeholder. | **MVP completo pronto para a Release 3.** |
| **Sprint 8 — Acessibilidade e incrementos** | 01/12–06/12 | **RF · 07/12** | Ondas 4–5 | Preparar a release final sem comprometer o MVP. | Contraste e fonte; revisão para idosos; vínculo pseudonimizado; explicabilidade se validada; concordância do profissional; correções. | MVP validado na R3; priorização por risco e capacidade. | Produto/UX; Mobile; Dados/IA; Qualidade. | Incrementos prioritários validados sem regressão do fluxo do MVP; documentação atualizada. | Incrementos desestabilizarem o MVP; explicabilidade não validada; pouco tempo. | Release final acessível e estável, com incrementos seguros pós-MVP. |
| **Encerramento — Avaliação e entrega final** | 08/12–14/12 | Pós-RF | — | Avaliar o produto e consolidar os artefatos. | Documentação técnica e de produto; resultados, limitações e trabalhos futuros; APK e artefatos finais. | Release final publicada; evidências e registros das sprints disponíveis. | Todas as frentes; Produto coordena a entrega. | APK final e documentação revisada entregues; retrospectiva e limitações registradas. | Documentação incompleta; perda de evidências; pendências após a RF. | Projeto encerrado com produto e conhecimento transferíveis. |

</div>

## Relação entre ondas, sprints e releases

- O **sequenciador** define ordem e prioridade das funcionalidades.
- O **roadmap** posiciona essas funcionalidades em períodos, objetivos e resultados esperados.
- Uma onda pode atravessar várias sprints, e uma sprint pode encerrar uma onda e iniciar outra.
- As releases são versões demonstráveis; a R3 representa o **MVP**.
- Acessibilidade e demais itens das Ondas 4 e 5 entram como **incrementos pós-MVP**, desde que não comprometam sua estabilidade.

## Histórico de versão

| Data | Versão | Descrição | Autor |
|---|---:|---|---|
| 13/09/2026 | 1.0 | Criação do roadmap a partir do cronograma oficial da disciplina. | Equipe MED |
