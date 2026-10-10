# Estrutura Analítica do Projeto

## Introdução

A Estrutura Analítica do Projeto (EAP) decompõe o escopo total do MED em
entregas verificáveis. A estrutura parte do projeto completo, separa as
entregas de definição do produto, gestão, engenharia e qualidade e detalha o
produto de software por release e por épico funcional.

A EAP segue a regra dos 100%: os componentes apresentados representam o
escopo planejado do projeto, sem incluir trabalho que não contribua para uma
entrega. As histórias de usuário não são um nível da decomposição; elas são
referenciadas apenas para permitir a rastreabilidade entre os épicos e o
backlog do aplicativo.

## Relação com o processo de desenvolvimento

- **EAP:** delimita o escopo total e organiza as entregas.
- **Sequenciador:** registra a prioridade funcional e o corte do MVP.
- **Backlog:** detalha os épicos em histórias de usuário e critérios de
  aceitação.
- **Roadmap:** distribui as entregas da EAP ao longo das releases.
- **Quadro de trabalho:** acompanha a execução e o aceite de cada história.

Esses artefatos devem ser atualizados em conjunto quando uma mudança de
escopo for aprovada. O detalhamento dos requisitos ocorre de forma evolutiva,
próximo da implementação, para reduzir retrabalho.

## Diagrama da EAP

![Diagrama hierárquico da EAP do projeto MED, com as releases decompostas em épicos funcionais](assets/imagens/eap/estrutura-analitica-projeto.svg)

O diagrama apresenta épicos, e não histórias individuais. Os números das
issues indicados nos épicos servem somente como ligação com o backlog. As
metas futuras não representam funcionalidades concluídas.

## Dicionário da EAP

### 1.1 Definição do produto

| Código | Entrega | Resultado esperado |
|---|---|---|
| **1.1.1** | Visão do produto e MVP | Alinhamento do problema, dos objetivos, das personas, das jornadas e do corte do MVP por meio da Lean Inception. |
| **1.1.2** | Sequenciador | Funcionalidades priorizadas em ondas, com dependências e separação entre MVP e incrementos subsequentes. |
| **1.1.3** | Requisitos e protótipos | Requisitos e protótipos detalhados de forma evolutiva e validados com os POs antes da implementação. |
| **1.1.4** | Identidade visual | Padrões de cores, mensagens, tipografia, ícones, botões e demais componentes visuais. |

### 1.2 Gestão do projeto

| Código | Entrega | Resultado esperado |
|---|---|---|
| **1.2.1** | EAP e backlog | Escopo total decomposto em entregas e backlog estimado e rastreável. |
| **1.2.2** | Roadmap e cronograma | Releases e épicos distribuídos no tempo, com marcos e dependências. |
| **1.2.3** | Custos | Linha de base de custos e acompanhamento do valor realizado por release. |
| **1.2.4** | Riscos | Riscos identificados, analisados, respondidos e monitorados durante o projeto. |
| **1.2.5** | Governança | Fluxo de branches, revisões, releases, contribuições e aceite mantido nos repositórios. |

### 1.3 Engenharia e qualidade

| Código | Entrega | Resultado esperado |
|---|---|---|
| **1.3.1** | Arquitetura e modelagem | Visões arquiteturais, componentes, integração com a IA e modelos conceitual e lógico do banco de dados. |
| **1.3.2** | Qualidade e testes | Modelo de qualidade, métricas, testes unitários, de integração, funcionais, de sistema e de aceitação. |
| **1.3.3** | Integração e entrega contínuas | Pipelines de verificação, coleta de métricas e geração de releases. |
| **1.3.4** | Dashboard e métricas | Indicadores gerenciais, de processo e de produto apresentados de forma rastreável. |

### 1.4 Produto de software

#### 1.4.1 R1 — Interfaces de acesso

A R1 registrou o incremento demonstrado em 28/09. A existência das telas não
representa o aceite integral das histórias de cadastro e login.

| Código | Épico | Escopo | Rastreabilidade |
|---|---|---|---|
| **1.4.1.1** | Acesso do profissional | Interfaces navegáveis de cadastro e login, com validações básicas do formulário. | Avanço parcial das USs [#5](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/5) e [#6](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/6). |

#### 1.4.2 R2 — Acesso local e primeira avaliação

A R2 tem como objetivo estabelecer o acesso funcional e demonstrar o início de
uma avaliação no tablet. O primeiro desenho é um avanço parcial das histórias
que abrangem as três tarefas e somente serão aceitas na R3.

| Código | Épico | Escopo | Rastreabilidade |
|---|---|---|---|
| **1.4.2.1** | Acesso local | Cadastro persistente e autenticação do profissional sem internet. | USs [#5](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/5) e [#6](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/6). |
| **1.4.2.2** | Atendimento e consentimento | Registro do atendimento vinculado ao profissional e apresentação e registro do TCLE antes de qualquer desenho. | USs [#7](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/7) e [#21](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/21). |
| **1.4.2.3** | Fundação da avaliação | Primeiro desenho demonstrado localmente e início da persistência protegida. | Avanço parcial das USs [#8, #9, #10](processo/roadmap.md), [#17, #23 e #25](processo/roadmap.md). |

#### 1.4.3 R3 — MVP integrado

A R3 é o marco planejado para o MVP completo. Cada épico depende de
integração, testes no tablet em modo avião e aceite dos critérios pelo PO.

| Código | Épico | Escopo | Rastreabilidade |
|---|---|---|---|
| **1.4.3.1** | Tarefas e interação | Instruções e execução das três tarefas, com confirmação, correção e avanço entre desenhos. | USs [#8](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/8), [#9](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/9) e [#23](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/23). |
| **1.4.3.2** | Captura e continuidade | Captura do traçado e da imagem confirmada, salvamento do progresso e retomada após interrupção. | USs [#10](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/10) e [#25](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/25). |
| **1.4.3.3** | Inferência e resultados | Encerramento sem escore para o paciente, inferência embarcada e resultados explicáveis acessíveis somente ao profissional. | USs [#11–#14](processo/roadmap.md). |
| **1.4.3.4** | Operação protegida | Fluxo integral sem internet, sem envio de dados clínicos e com dados locais cifrados. | USs [#15–#17](processo/roadmap.md). |
| **1.4.3.5** | Exportação local | Geração de XML sob solicitação do profissional, sem transmissão automática. | US [#22](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/22). |

#### 1.4.4 Release final — Estabilização

| Código | Épico | Escopo | Rastreabilidade |
|---|---|---|---|
| **1.4.4.1** | Correções e testes finais | Estabilização do incremento validado, correção de defeitos e verificação final no tablet. | Defeitos e pendências registrados durante as releases. |
| **1.4.4.2** | Acessibilidade | Configuração de contraste e tamanho da fonte, conforme a capacidade restante e sem regressão do MVP. | US [#24](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/24). |

## Rastreabilidade com o sequenciador

| Elemento do sequenciador | Épico da EAP |
|---|---|
| Cadastrar e logar o profissional de saúde | 1.4.2.1 — Acesso local |
| Aceitar o TCLE | 1.4.2.2 — Atendimento e consentimento |
| Desenhar, confirmar, apagar e refazer | 1.4.3.1 — Tarefas e interação |
| Capturar coordenadas, ordem, tempo e imagem | 1.4.3.2 — Captura e continuidade |
| Salvar dados de progresso offline | 1.4.3.2 — Captura e continuidade |
| Rodar inferência do modelo embarcado | 1.4.3.3 — Inferência e resultados |
| Visualizar instrução e encerramento sem escore | 1.4.3.1 e 1.4.3.3 |
| Exportar XML com os dados pertinentes | 1.4.3.5 — Exportação local |
| Vincular avaliação ao profissional e ao paciente | 1.4.2.2 — Atendimento e consentimento |
| Configurar contraste e tamanho da fonte | 1.4.4.2 — Acessibilidade |
| Extrair características de cada figura | 1.4.3.3 — Inferência e resultados |

O sequenciador define a ordem de valor e as dependências funcionais. O
[roadmap](processo/roadmap.md) define em qual release cada épico será
demonstrado e aceito.

## Histórico de versões

| Versão | Descrição | Autor(es) | Data | Revisor(es) | Data de revisão |
|---|---|---|---|---|---|
| 1.0 | Criação do documento de EAP. | [Lucas Mendonça Arruda](https://github.com/lucasarruda9) | 13/09/2026 | [Artur Mendonça Arruda](https://github.com/Artymend07) | 17/09/2026 |
| 1.1 | Remoção do macro "Gerenciamento do projeto" e reorganização dos pacotes de trabalho. | [Lucas Mendonça Arruda](https://github.com/lucasarruda9) | 17/09/2026 | [Artur Mendonça Arruda](https://github.com/Artymend07) | 19/09/2026 |
| 1.2 | Ajuste das seções e incorporação das métricas e do dashboard ao macro de qualidade. | [Lucas Mendonça Arruda](https://github.com/lucasarruda9) | 22/09/2026 | [Artur Mendonça Arruda](https://github.com/Artymend07) | — |
| 1.3 | Definição dos pacotes de R1, R2 e R3 com vínculo às USs do APP e ao roadmap. | [Daniel Ferreira Nunes](https://github.com/Mach1r0) | 26/09/2026 | — | — |
| 1.4 | Reestruturação da EAP por entregas, releases e épicos funcionais, com alinhamento ao sequenciador, backlog e roadmap após a R1. | [Daniel Ferreira Nunes](https://github.com/Mach1r0) | 10/10/2026 | — | — |
