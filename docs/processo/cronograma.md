# Cronograma Projeto UnB FCTE/UNIEURO


Este documento apresenta o cronograma de desenvolvimento do projeto, seguindo os prazos previamente estabelecidos no [plano de ensino](https://github.com/fga-eps-mds/A-Disciplina-MDS-EPS/blob/master/PlanosDeEnsino/EPS_Plano_de_Ensino.md) da disciplina de Engenharia de Produto de Software (EPS) do semestre 2026.2.

## Marcos do projeto

| Data | Marco | Resultado demonstrável |
|---|---|---|
| **10/08** | Início do projeto | Início da Lean Inception e da preparação técnica. |
| **28/09** | **Release 1 — primeiro fluxo funcional** | O profissional entra no aplicativo, inicia uma avaliação, aplica a tarefa do relógio e salva o resultado localmente. |
| **26/10** | **Release 2 — captura e inferência integradas** | Os três testes são executados, os dados necessários são capturados e uma primeira inferência é realizada localmente. |
| **30/11** | **Release 3 — Entrega do MVP** | O fluxo completo roda localmente no tablet, do login do profissional à apresentação do resultado da triagem. |
| **07/12** | **Release final** | MVP revisado com incrementos prioritários de acessibilidade e documentação final. |
| **14/12** | Encerramento do projeto | APK e artefatos da disciplina entregues; resultados e limitações registrados. |

## Releases do Projeto

O projeto seguirá os seguintes prazos de entrega, com releases planejadas para homologação e demonstração do produto ao cliente.

### RELEASE MAJOR R1 · 28/09/2026  

> **Data-limite de registro nos repositórios.** Release implantada em ambiente de homologação. Apresentações: 20 min por time · Reunião de 2h · Gravação no Teams.

***Escopo da release***:

* **Projeto-Produto:** Visão do Produto/Canvas MVP validado, backlog priorizado com protótipos de alta fidelidade no Figma, pipeline CI/CD configurado com cobertura de testes unitários $\ge 85\%$.
* **Dashboard Gerencial (DA-R1):** Construído em Streamlit consumindo o `.json` do SonarCloud (métricas de velocity, burndown, EVM-Ágil, etc.). Submeter URL e PR no Aprender 3.
* **Memorando de decisão:** MD-R1 entregue com $\ge 2$ ciclos registrados no `MD_Template.md` antes das 06h00 do dia **29/09/2026**.

---

### RELEASE MAJOR R2 · 26/10/2026

> **Data-limite de registro nos repositórios.** Incremento funcional implantado em homologação. Apresentações: 20 min por time · Reunião de 2h · Gravação no Teams.

***Escopo da release***:

* **Projeto-Produto:** Incremento funcional em homologação, histórias aceitas pelo cliente, pipeline evoluído com testes de integração ($\ge 85\%$ de cobertura) e `.json` atualizado automaticamente.
* **Dashboard Gerencial (DA-R2):** Evolução com métricas de processo e qualidade, comparativo R1 $\times$ R2 e $\ge 3$ decisões gerenciais documentadas. Submeter URL e PR no Aprender 3.
* **Memorando de decisão:** MD-R2 entregue com log de autoavaliação de IA e $\ge 5$ ciclos acumulados no `MD_Template.md` antes das 06h00 do dia **27/10/2026**.

---

### RELEASE MAJOR R3 · 30/11/2026

> **Data-limite de registro nos repositórios.** Produto em produção/homologação e MVP validado com os clientes. Apresentações: 20 min por time · Reunião de 2h · Gravação no Teams. Foco: Planejado x Realizado.

***Escopo da release***:

* **Projeto-Produto:** Produto implantado, cobertura de testes $\ge 90\%$ (unitários, integração, sistema e GUI), manual de instalação e Relatório de Encerramento com a seção *"Como usamos IA neste semestre"*.
* **Dashboard Gerencial (DA-R3):** Forma final com o **Canvas Analytics**, análise completa de planejado $\times$ realizado (custo, tempo, escopo e qualidade), $\ge 5$ decisões gerenciais e retrospectiva crítica de IA. Submeter URL e PR no Aprender 3.
* **Memorando de decisão:** MD-R3 completo ($\ge 8$ ciclos) e início das defesas orais.

---

### RELEASE MAJOR FINAL (RF) · 07/12/2026

> **Semana de encerramento, consolidação e defesa.**

***Escopo da release***:

* Execução e documentação final dos testes de aceitação com o cliente.
* Finalização do Relatório de Encerramento.
* Continuação e conclusão das defesas orais individuais (justificativa de decisões gerenciais).
* Submissão final do MD-R3 e registro das evidências (seção 5.) antes das 06h00 do dia **08/12/2026**.

### RELEASES MINOR

Haverão 3 Releases Minor, com entregas incrementais de funcionalidades, para validação do produto e acompanhamento do progresso do projeto. As entregas deverão ser feitas no Aprender 3.

| Release | Data |
|---|---|
| **RM1** | 13/10/2026 |
| **RM2** | 09/11/2026 |
| **RM3** | 07/12/2026 |


## Entregas dos Dashboards Analíticos (DA-R1, DA-R2 e DA-R3)

| Dashboard | Data-limite |  Objetivo |
|-----------|-------|---------|
| **DA-R1** | 28/09 | Consolidar os primeiros indicadores técnicos e gerenciais. Ex: velocity, burndown, EVM-Ágil e matriz de riscos.   |
| **DA-R2** | 26/10 | Evoluir DA-R1 e incorpora o _Dashboard_ com as métricas de qualidade de produto normalizadas, ponderadas, agregadas e interpretadas pelo time. |
| **DA-R3** | 30/11 | Evoluir DA-R2 e alcança sua forma final com o Canvas Analytics, apresentando síntese visual do desempenho do produto e do projeto ao longo de todo o semestre, incluindo a análise planejado × realizado e uma retrospectiva crítica sobre o uso de IA generativa no projeto. |
---

## Histórico de versões

| Versão | Descrição | Autor(es) | Data | Revisor(es) | Data de Revisão |
|---|---|---|---|---|---|
| 1.0 | Criação do documento: Cronograma | [Henrique Galdino Couto](https://github.com/hgaldino05) | 12/09/2026 | [Daniel Ferreira Nunes](https://github.com/Mach1r0) | |
| 1.1 | Inclusão das releases minor no cronograma | [Henrique Galdino Couto](https://github.com/hgaldino05) | 19/09/2026 | [Daniel Ferreira Nunes](https://github.com/Mach1r0) | |

