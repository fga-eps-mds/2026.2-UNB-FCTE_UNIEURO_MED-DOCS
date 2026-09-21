---
title: Metodologia
---

# Metodologias e Técnicas

## 1. Introdução

Durante o desenvolvimento do projeto, a equipe utiliza diferentes metodologias,
técnicas e práticas para apoiar a descoberta do produto, o planejamento, o
desenvolvimento, o acompanhamento do projeto e a validação das entregas.

Este documento apresenta as principais abordagens adotadas, descrevendo sua
finalidade, a forma como são aplicadas no contexto do projeto e os artefatos
produzidos ao longo do processo.

O trabalho se organiza em quatro momentos, cada um coberto por uma seção abaixo:

| Momento | Abordagens | Seções |
|---|---|---|
| Descoberta e definição do produto | Lean Inception | [2](#2-lean-inception) |
| Planejamento e execução | Scrum, EAP, backlog e histórias de usuário | [3](#3-scrum) e [4](#4-escopo-e-requisitos) |
| Colaboração e desenvolvimento | Quadro de tarefas, fluxo de Git, revisão de código, prototipação | [5](#5-gestao-do-trabalho-e-colaboracao) a [7](#7-prototipacao) |
| Acompanhamento e qualidade | Documentação como código, CI/CD, Agile EVM, velocity e gestão de riscos | [8](#8-documentacao-como-codigo-e-cicd) e [9](#9-monitoramento-e-metricas) |

## 2. Lean Inception

### 2.1 Visão geral

A Lean Inception é uma abordagem colaborativa utilizada para promover o
alinhamento entre os participantes do projeto acerca do produto a ser
desenvolvido e do seu Produto Mínimo Viável (MVP).

Seu objetivo é construir um entendimento compartilhado entre as partes
envolvidas, permitindo discutir objetivos, usuários, funcionalidades, jornadas e
prioridades antes do início do desenvolvimento.

No projeto, a Lean Inception foi conduzida na etapa inicial de descoberta e definição
do produto, em reuniões com o *Product Owner*, o cliente e o professor, entre
agosto e setembro de 2026. Cada encontro está registrado nas
[atas de reunião](../atas-reunioes/index.md). O conjunto de artefatos gerados é
a [Visão do Produto](../produto/visao.md).

As atividades utilizadas são apresentadas a seguir.

### 2.2 Visão do Produto

A Visão do Produto foi utilizada para alinhar entre equipe e stakeholders qual
produto está sendo desenvolvido, para quem ele se destina, qual problema busca
resolver e qual é o seu principal diferencial.

A atividade produz uma declaração concisa que sintetiza o propósito do produto e
serve como referência para as demais decisões tomadas durante o projeto.

**Aplicação no projeto:** o produto é um aplicativo Android que roda localmente, sem
internet, no tablet do hospital, com modelo de IA embarcado, para triagem
cognitiva de pessoas idosas por meio de tarefas de desenho.

#### Finalidade

- Alinhar o entendimento da equipe sobre o produto;
- Identificar o público-alvo;
- Explicitar o problema ou necessidade atendida;
- Registrar os principais benefícios esperados;
- Apoiar decisões posteriores sobre funcionalidades e escopo.

#### Artefato resultante

- [Declaração da Visão do Produto](../produto/lean-inception.md#1-declaracao-da-visao-do-produto).

### 2.3 O Produto É / Não É / Faz / Não Faz

A técnica "É / Não É / Faz / Não Faz" foi utilizada para esclarecer os limites do
produto.

Ela auxilia a equipe a construir um entendimento compartilhado sobre o que o
produto representa, quais funções fazem parte de sua proposta e, principalmente,
quais elementos estão fora do escopo inicialmente definido.

A atividade é organizada em quatro perspectivas:

| Perspectiva | Objetivo |
|-------------|----------|
| É | Características que definem o produto |
| Não é | Características que não representam o produto |
| Faz | Funções e comportamentos esperados |
| Não faz | Funções explicitamente fora do escopo |

**Aplicação no projeto:** a técnica deixou explícito, por exemplo, que o produto é uma
ferramenta de apoio à decisão e não um diagnóstico, e que não envia dados a
servidor externo.

#### Finalidade

- Reduzir ambiguidades;
- Estabelecer limites iniciais de escopo;
- Alinhar expectativas entre equipe e stakeholders;
- Evitar interpretações diferentes sobre o produto.

#### Artefato resultante

- [Quadro É / Não É / Faz / Não Faz](../produto/lean-inception.md#2-e-nao-e-faz-nao-faz).

### 2.4 Objetivos de Negócio

Os objetivos de negócio foram levantados e agrupados em conjuntos afins
(*clusters*), para deixar claro que resultados o produto precisa alcançar para
ser considerado bem-sucedido.

**Aplicação no projeto:** os objetivos foram organizados em torno da qualidade da IA
e do escore, da experiência do paciente idoso, da experiência do profissional de
saúde e da qualidade dos dados coletados.

#### Finalidade

- Explicitar o valor esperado do produto;
- Dar critério para priorizar funcionalidades;
- Servir de base para as hipóteses e métricas do Canvas MVP.

#### Artefato resultante

- [Objetivos de Negócio](../produto/lean-inception.md#3-objetivos-de-negocio).

### 2.5 Personas

As personas foram utilizadas para representar grupos relevantes de usuários do
produto.

A definição das personas permite que decisões relacionadas às funcionalidades,
experiência e prioridades do produto sejam tomadas considerando as necessidades,
objetivos e dificuldades dos usuários.

**Aplicação no projeto:** foram definidas duas personas, o paciente idoso (Seu José)
e o profissional da saúde (Dr. Marcelo).

#### Finalidade

- Identificar os principais usuários do produto;
- Entender necessidades e objetivos;
- Apoiar a definição das funcionalidades;
- Orientar decisões de experiência do usuário.

#### Artefato resultante

- [Personas do projeto](../produto/lean-inception.md#4-personas).

### 2.6 Jornadas dos Usuários

As jornadas dos usuários descrevem sequências de interação entre as personas e o
produto para alcançar determinados objetivos.

Elas permitem visualizar o produto sob a perspectiva do usuário e verificar como
as funcionalidades propostas participam de situações reais de utilização.

**Aplicação no projeto:** foram mapeadas três jornadas: o paciente realizando a
triagem, o profissional aplicando o teste na rotina e o profissional usando o
aplicativo pela primeira vez.

#### Finalidade

- Compreender como o usuário interage com o produto;
- Identificar funcionalidades necessárias em cada etapa;
- Encontrar lacunas ou problemas na experiência;
- Apoiar a priorização das funcionalidades.

#### Artefato resultante

- [Jornadas dos usuários](../produto/lean-inception.md#5-jornadas-de-usuario).

### 2.7 Brainstorming de Funcionalidades

Após o alinhamento sobre produto, objetivos e usuários, a equipe realiza o
levantamento das funcionalidades que podem compor o produto.

O brainstorming permite que diferentes participantes contribuam com ideias, sem
uma filtragem prematura das possibilidades. Depois, as funcionalidades são
agrupadas e avaliadas.

#### Finalidade

- Identificar possíveis funcionalidades;
- Explorar diferentes soluções para as necessidades dos usuários;
- Criar uma base inicial para priorização;
- Apoiar a definição do MVP.

#### Artefato resultante

- [Lista de funcionalidades por cluster](../produto/funcionalidades.md#atividade-6-brainstorming-de-funcionalidades).

### 2.8 Revisão Técnica, de Negócio e de UX

Cada funcionalidade levantada é avaliada sob três perspectivas: o esforço
técnico, o valor para o negócio e o impacto na experiência do usuário.

O resultado dessa avaliação alimenta diretamente o sequenciador.

#### Finalidade

- Estimar de forma comparável o esforço e o valor de cada funcionalidade;
- Evidenciar riscos técnicos e de experiência antes do desenvolvimento;
- Apoiar decisões de priorização com critérios explícitos.

#### Artefato resultante

- [Revisão técnica, de negócio e de UX](../produto/funcionalidades.md#atividade-7-revisao-tecnica-de-negocio-e-de-ux).

### 2.9 Sequenciador de Funcionalidades

O sequenciador é utilizado para organizar as funcionalidades de forma
incremental.

Seu objetivo é auxiliar a equipe a decidir quais funcionalidades devem aparecer
primeiro e quais podem ser desenvolvidas posteriormente. A técnica também
auxilia na identificação do conjunto mínimo de funcionalidades necessário para
compor o MVP.

**Aplicação no projeto:** o sequenciador define as ondas de entrega. As ondas
indicam a ordem de valor do produto e servem de base para o
[Roadmap do Produto](roadmap.md), mas **não equivalem** às sprints.

#### Finalidade

- Organizar a evolução incremental do produto;
- Apoiar o planejamento das entregas;
- Priorizar funcionalidades;
- Identificar o MVP.

#### Artefato resultante

- [Sequenciador de funcionalidades](../produto/sequenciador.md).

### 2.10 Produto Mínimo Viável — MVP

O MVP corresponde ao menor conjunto de funcionalidades capaz de entregar valor
suficiente para permitir validação e aprendizado sobre o produto.

Na Lean Inception, o MVP não deve ser entendido apenas como uma versão com poucas
funcionalidades, mas como uma entrega capaz de testar hipóteses e gerar
aprendizado para orientar as próximas evoluções do produto.

**Aplicação no projeto:** o MVP é o fluxo completo rodando localmente no tablet, do
login do profissional à apresentação do resultado da triagem, com os três testes
de desenho. Ele é entregue na Release 3 (30/11), conforme o
[Roadmap](roadmap.md#marcos-oficiais).

#### Finalidade

- Entregar valor de maneira antecipada;
- Validar hipóteses;
- Obter feedback;
- Reduzir o risco de desenvolver funcionalidades sem valor;
- Orientar a evolução incremental do produto.

### 2.11 Canvas MVP

O Canvas MVP consolida as principais decisões obtidas durante a Lean Inception.

Ele reúne em um único artefato informações sobre o MVP planejado e serve como
síntese da estratégia definida pela equipe: proposta, usuários, jornadas,
funcionalidades, hipóteses a validar, métricas de validação, custo e cronograma.

#### Finalidade

- Consolidar as decisões tomadas durante a Lean Inception;
- Registrar a estratégia do MVP;
- Criar uma referência compartilhada para equipe e stakeholders;
- Apoiar o planejamento das próximas etapas do projeto.

#### Artefato resultante

- [Canvas MVP](../produto/canvas-mvp.md).

## 3. Scrum

### 3.1 Visão geral

A execução do projeto segue o Scrum, framework ágil que organiza o trabalho em
ciclos curtos (*sprints*), cada um entregando um incremento do produto. A
abordagem é adequada ao projeto porque o produto é novo, as hipóteses precisam ser
validadas com o cliente e o escopo evolui a partir do aprendizado.

### 3.2 Aplicação no projeto

- **Sprints:** o semestre está dividido em oito sprints, em geral de duas
  semanas, cada uma com objetivo, entregas e critério de conclusão definidos no
  [Roadmap do Produto](roadmap.md#planejamento-detalhado).
- **Releases:** as sprints se agrupam em releases demonstráveis (R1 em 28/09,
  R2 em 26/10, R3 em 30/11 e release final em 07/12). Ao fim de cada release, a
  equipe apresenta o incremento ao cliente.
- **Papéis:** o *Product Owner* representa o cliente e valida escopo e
  prioridades; a equipe de desenvolvimento é organizada em frentes de
  responsabilidade (por exemplo, Mobile, Dados/IA, Produto/UX, Qualidade e
  DevOps). Os integrantes estão listados na página da [Equipe](../equipe/equipe.md).
- **Eventos:** dailies para alinhamento rápido, reuniões de review com o
  *Product Owner* para validar o que foi entregue e retrospectivas para registrar
  aprendizados e limitações.
- **Artefatos:** Product Backlog priorizado, backlog da sprint e o incremento
  demonstrável de cada sprint.

#### Finalidade

- Entregar valor de forma incremental e frequente;
- Obter feedback do *Product Owner* e do cliente a cada ciclo;
- Adaptar o plano à medida que o produto é descoberto;
- Dar previsibilidade ao acompanhamento do semestre.

## 4. Escopo e requisitos

### 4.1 Estrutura Analítica do Projeto (EAP)

A EAP decompõe o escopo total do projeto em partes menores, organizadas
hierarquicamente até chegar aos pacotes de trabalho. No projeto, ela funciona como
norte estratégico do escopo macro e se integra ao Scrum: os pacotes de trabalho
são desdobrados no Product Backlog em épicos e histórias de usuário, e o
progresso do escopo é atualizado à medida que as histórias são validadas.

#### Artefato resultante

- Estrutura Analítica do Projeto (EAP).

### 4.2 Product Backlog e Histórias de Usuário

Os requisitos do produto são registrados como histórias de usuário, no formato
"Como *perfil*, quero *ação*, para que *benefício*", acompanhadas de critérios de
aceitação. As histórias são organizadas em blocos por tema (por exemplo, acesso e
cadastro do médico, termo de consentimento) e priorizadas a partir do
sequenciador.

Cada história é registrada como *issue* no GitHub, por meio de um modelo que
exige:

- contexto e problema;
- critérios de aceitação objetivos, observáveis e testáveis;
- regras de negócio;
- referências e protótipos;
- prioridade sugerida;
- **definição de pronta**, isto é, a história expressa valor claro e seus
  critérios podem ser testados.

#### Finalidade

- Manter os requisitos centrados no valor para o usuário;
- Tornar o aceite verificável;
- Rastrear cada entrega até a necessidade que a originou.

#### Artefato resultante

- Product Backlog (histórias de usuário do MVP).

## 5. Gestão do trabalho e colaboração

### 5.1 Quadro de tarefas

O acompanhamento das sprints é feito em um quadro no Zenhub integrado ao GitHub
([abrir board](https://app.zenhub.com/workspaces/unbfcte-unieuromed-6a8c447d652b15002979b829/board)).
Cada item do trabalho é uma *issue*, criada a partir de um dos modelos do
repositório:

| Modelo | Uso |
|---|---|
| História (*user story*) | Funcionalidade proposta a partir da necessidade de uma pessoa usuária |
| Tarefa (*task*) | Atividade técnica, operacional ou de documentação |
| Relatório de bug | Defeito encontrado no produto |

As tarefas seguem a estrutura Objetivo, Contexto, Atividades, Critérios de
conclusão, Dependências e impedimentos e Prioridade sugerida, e são agrupadas em
épicos (por exemplo, "Planejamento do Projeto").

### 5.2 Comunicação

| Canal | Uso |
|---|---|
| Discord | Alinhamento com o *Product Owner* e reuniões de review |
| WhatsApp | Comunicação diária da equipe e organização das dailies |
| GitHub | Discussão técnica em issues e pull requests |

### 5.3 Atas de reunião

As reuniões com o *Product Owner* e com o cliente são registradas em atas,
seguindo um modelo padronizado, com pontos discutidos, decisões tomadas e
presença. As atas dão rastreabilidade às decisões de negócio.

Consulte as [atas de reunião](../atas-reunioes/index.md).

## 6. Práticas de desenvolvimento

O fluxo de contribuição segue o
[Guia de Contribuição](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-DOCS/blob/main/CONTRIBUTING.md)
do repositório.

- **Branches:** cada mudança é feita em uma branch própria, nomeada por tipo:
  `feature/nome-da-funcionalidade`, `bugfix/nome-do-erro` ou
  `docs/nome-do-documento`.
- **Commits:** mensagens claras e em português, com prefixo que indica o tipo da
  alteração (`docs:`, `feat:`, `fix:`).
- **Pull requests:** todo PR usa o modelo do repositório, que pede descrição,
  tipo de alteração, issue relacionada (`Closes #NN`), como testar, evidências e
  um checklist de conferência.
- **Revisão de código:** o autor solicita a revisão de pelo menos uma pessoa da
  equipe e deve ser capaz de explicar cada linha do que submeteu.
- **Vínculo com as issues:** o PR fecha a issue correspondente, mantendo o quadro
  do Zenhub atualizado.

#### Finalidade

- Manter o histórico do projeto organizado e rastreável;
- Compartilhar conhecimento e reduzir defeitos por meio da revisão por pares;
- Garantir que nenhuma alteração entre sem que ao menos outra pessoa a tenha
  lido.

## 7. Prototipação

Os protótipos de interface e a identidade visual do produto são construídos no
Figma. A prototipação permite validar fluxos e telas com o *Product Owner* e com
o cliente antes da implementação, reduzindo retrabalho. Os protótipos são
referenciados nas histórias de usuário e servem de insumo para a equipe de
desenvolvimento.

Como o público inclui pessoas idosas com pouca familiaridade com tecnologia, a
prototipação considera aspectos de acessibilidade, como contraste e tamanho de
fonte.

## 8. Documentação como código e CI/CD

### 8.1 Documentação como código

Esta documentação é escrita em Markdown, versionada no mesmo repositório e
publicada como site com [MkDocs](https://www.mkdocs.org/) e o tema Material. Isso
permite tratar a documentação com as mesmas práticas do código: branches, pull
requests e revisão.

### 8.2 Integração e entrega contínuas

O repositório possui um fluxo do GitHub Actions que constrói o site a cada pull
request e o publica no GitHub Pages a cada alteração na branch principal. Para o
produto, o escopo da Release 1 prevê pipeline de CI/CD configurado, com testes
automatizados e cobertura mínima definida no plano da disciplina.

#### Finalidade

- Detectar erros de build antes de integrar a mudança;
- Manter a documentação sempre publicada e atualizada;
- Reduzir trabalho manual de publicação.

## 9. Monitoramento e métricas

O acompanhamento do projeto é apoiado por um dashboard gerencial próprio, feito
em Python com Streamlit, Plotly e Pandas, que consolida indicadores de prazo,
custo, qualidade e processo.

### 9.1 Agile EVM

O Agile EVM (*Earned Value Management* adaptado ao contexto ágil) compara o que
foi planejado com o que foi efetivamente entregue, em pontos de história.

| Indicador | O que mostra |
|---|---|
| PV (valor planejado) e EV (valor agregado) | Progresso planejado e progresso real |
| SPI (índice de desempenho de prazo) | Se a equipe está adiantada ou atrasada |
| CPI (índice de desempenho de custo) | Se o custo está acima ou abaixo do orçamento |
| SV, CV | Variações de prazo e de custo |
| EAC | Estimativa de custo no término |

### 9.2 Velocity e burnup

A *velocity* registra os pontos de história entregues por sprint e sua média,
apoiando o planejamento das sprints seguintes. O gráfico de burnup compara o
trabalho planejado, o realizado e a trajetória ideal.

### 9.3 Gestão de riscos

Os riscos são avaliados em uma matriz de probabilidade × impacto (5 × 5), com
planos de mitigação. Cada etapa do roadmap também lista seus principais riscos.

### 9.4 Métricas de processo e CI/CD

O dashboard acompanha ainda a taxa de sucesso dos pipelines e o tempo médio de
feedback, para avaliar a saúde do processo de entrega.

#### Finalidade

- Apoiar decisões gerenciais com dados;
- Antecipar desvios de prazo e custo;
- Comparar o planejado com o realizado a cada release.

## 10. Resumo da aplicação

| Metodologia/Técnica | Objetivo | Artefato |
|---------------------|----------|----------|
| Lean Inception | Alinhar equipe e stakeholders acerca do MVP | Conjunto de artefatos da Inception |
| Visão do Produto | Estabelecer propósito e direção do produto | [Visão do Produto](../produto/visao.md) |
| É / Não É / Faz / Não Faz | Delimitar entendimento e escopo | [Quadro de definição do produto](../produto/lean-inception.md#2-e-nao-e-faz-nao-faz) |
| Objetivos de Negócio | Explicitar o valor esperado | [Objetivos de Negócio](../produto/lean-inception.md#3-objetivos-de-negocio) |
| Personas | Representar grupos de usuários | [Personas](../produto/lean-inception.md#4-personas) |
| Jornadas | Representar interações do usuário | [Jornadas dos usuários](../produto/lean-inception.md#5-jornadas-de-usuario) |
| Brainstorming de funcionalidades | Identificar soluções e funcionalidades | [Funcionalidades](../produto/funcionalidades.md) |
| Revisão técnica, de negócio e de UX | Comparar esforço, valor e experiência | [Revisão](../produto/funcionalidades.md#atividade-7-revisao-tecnica-de-negocio-e-de-ux) |
| Sequenciador | Organizar funcionalidades de forma incremental | [Sequenciador](../produto/sequenciador.md) |
| MVP e Canvas MVP | Definir e consolidar a primeira entrega validável | [Canvas MVP](../produto/canvas-mvp.md) |
| Scrum | Entregar valor em ciclos curtos com feedback | [Roadmap do Produto](roadmap.md) |
| EAP | Decompor o escopo em pacotes de trabalho | EAP |
| Histórias de usuário | Registrar requisitos com critérios de aceitação | Product Backlog e issues no GitHub |
| Quadro de tarefas (Zenhub) | Acompanhar o andamento das sprints | Board do Zenhub |
| Atas de reunião | Registrar decisões com o PO e o cliente | [Atas de reunião](../atas-reunioes/index.md) |
| Fluxo de Git e revisão de código | Integrar mudanças com rastreabilidade e qualidade | Branches, commits e pull requests |
| Prototipação | Validar telas e fluxos antes da implementação | Protótipos no Figma |
| Documentação como código e CI/CD | Manter documentação e entrega automatizadas | Este site e o fluxo do GitHub Actions |
| Agile EVM, velocity e riscos | Monitorar prazo, custo, entrega e riscos | Dashboard gerencial |

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
