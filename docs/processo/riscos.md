# Plano de Gestão de Riscos

## Introdução

A gestão de riscos é um componente essencial no desenvolvimento de software, garantindo que os projetos alcancem seus objetivos com sucesso e dentro do prazo previsto. Este plano de gestão de riscos tem como objetivo identificar, analisar, priorizar e mitigar os riscos potenciais que podem surgir ao longo do ciclo de vida do desenvolvimento do software, ressaltando que é um produto novo, sendo implementado do zero.

O contexto do projeto agrava a exposição a certos riscos e reduz outros, sendo fundamental que a equipe esteja ciente desses riscos e tenha estratégias para lidar com eles. A gestão de riscos eficaz não apenas protege o projeto contra possíveis falhas, mas também contribui para a melhoria contínua do processo de desenvolvimento, promovendo uma cultura de proatividade e resiliência.

Este documento fornece uma visão geral das estratégias e processos que serão implementados para assegurar que os riscos sejam gerenciados de maneira eficaz, minimizando impactos negativos e promovendo a entrega do MVP dentro do prazo final e com sua devida qualidade.

### Tipos de risco

Os riscos foram divididos nas seguintes categorias:

- Externo
- Gerencial
- Organizacional
- Técnico

## Definições

### Probabilidade e impacto dos riscos

| Nível | Probabilidade | Porcentagem de certeza |
| :---: | :---: | :---: |
| 1 | Muito baixa | 0% - 19% |
| 2 | Baixa | 20% - 39% |
| 3 | Média | 40% - 59% |
| 4 | Alta | 60% - 79% |
| 5 | Muito alta | 80% - 100% |

### Impacto

| Nível | Impacto |
| :---: | :---: |
| 1 | Muito baixo |
| 2 | Baixo |
| 3 | Médio |
| 4 | Alto |
| 5 | Muito alto |

### Matriz de probabilidade X impacto

| Probabilidade / Impacto | Muito baixo | Baixo | Médio | Alto | Muito alto |
| :---: | :---: | :---: | :---: | :---: | :---: |
| Muito baixa | 1 | 2 | 3 | 4 | 5 |
| Baixa | 2 | 4 | 6 | 8 | 10 |
| Média | 3 | 6 | 9 | 12 | 15 |
| Alta | 4 | 8 | 12 | 16 | 20 |
| Muito alta | 5 | 10 | 15 | 20 | 25 |

### Graus de risco

A severidade de um risco é o produto `probabilidade × impacto`, de 1 a 25. O grau é dado pela tabela abaixo.

| Severidade | Grau |
| :---: | :---: |
| 1 - 5 | Baixo |
| 6 - 12 | Médio |
| 15 - 25 | Elevado |

Nenhum produto de dois níveis de 1 a 5 resulta em 13 ou 14, por isso não há lacuna entre as faixas.

!!! info "Escala única"
    Esta é a única escala de classificação do projeto. O [dashboard gerencial](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-DOCS/tree/main/dashboard), na aba Gestão de Riscos, usa as mesmas faixas e os mesmos rótulos (`FAIXAS_RISCO` em `dashboard/src/config.py`), e um teste automatizado falha se o documento e o dashboard divergirem.

## Levantamento de riscos

### Tabela de Riscos

| Risco | Descrição | Categoria |
| :---: | :---: | :---: |
| R01 | Dificuldade com as tecnologias definidas | Técnico |
| R02 | Saída de algum integrante do projeto | Gerencial |
| R03 | Divergência nos horários disponíveis dos integrantes | Organizacional |
| R04 | Alteração no escopo do projeto | Gerencial |
| R05 | Integrante com problema de saúde | Externo |
| R06 | Indisponibilidade do cliente ou de especialistas para esclarecimento de requisitos e aceite das entregas | Externo |
| R07 | Sobrecarga de membros da equipe, principalmente perto das entregas de release | Gerencial |
| R08 | Falha de equipamento | Externo |
| R09 | Dependência entre atividades | Organizacional |
| R10 | Perda ou corrupção de dados armazenados localmente no dispositivo | Técnico |
| R11 | Resultados insatisfatórios da solução desenvolvida | Técnico |
| R12 | Falta de dados adequados para desenvolvimento e validação | Externo |
| R13 | Dificuldade em treinar um modelo de IA com desempenho adequado | Técnico |
| R14 | Questões de privacidade e proteção de dados sensíveis | Externo |

### Causa e Consequência dos Riscos

| Risco | Causa | Consequência |
| :---: | :---: | :---: |
| R01 | Falta de experiência da equipe com tecnologias como React Native/Expo e modelos de IA embarcados | Atrasos no desenvolvimento e aumento da curva de aprendizado |
| R02 | Desistência, trancamento de disciplina ou imprevisto pessoal de integrante (equipe estudantil) | Redução da capacidade da equipe e sobrecarga dos demais membros |
| R03 | Conflitos de agenda entre integrantes com outras disciplinas e compromissos acadêmicos | Dificuldade de comunicação e atraso na execução das atividades |
| R04 | Mudanças nos requisitos solicitadas pelo cliente (UniEuro) | Retrabalho e impacto no cronograma do projeto |
| R05 | Problemas de saúde de integrantes | Ausência temporária e atraso nas entregas |
| R06 | Falta de disponibilidade do cliente ou de especialistas (ex.: professor/PO da UniEuro) para reuniões, esclarecimentos e validação das entregas | Dificuldade na definição de requisitos, histórias paradas aguardando aceite e atrasos no projeto |
| R07 | Distribuição inadequada de tarefas, especialmente perto das release | Queda na produtividade e risco de burnout |
| R08 | Problemas técnicos em equipamentos (tablets, notebooks) | Interrupção do trabalho e perda de produtividade |
| R09 | Forte dependência entre tarefas de frentes diferentes (ex.: modelo de IA e aplicativo) | Efeito cascata de atrasos no cronograma |
| R10 | Falha na gravação, fechamento do aplicativo durante uma avaliação ou problema no armazenamento local do Tablet | Perda de avaliações já realizadas e necessidade de repetir a coleta |
| R11 | Limitações da solução ou erros na implementação, como desempenho insuficiente do modelo de IA no tablet | Entregas que não atendem aos requisitos esperados |
| R12 | Falta ou baixa qualidade dos dados disponíveis para treinar/validar o modelo | Dificuldade na validação e baixa confiabilidade da solução |
| R13 | Dados insuficientes, modelo mal calibrado ou problema mais difícil do que o previsto | Resultado da avaliação pouco confiável, exigindo retrabalho no modelo |
| R14 | Falta de cuidado no tratamento/armazenamento de dados pessoais de saúde dos usuários | Exposição indevida de dados ou impedimento de uso em ambiente real |

### Prevenção e Solução dos Riscos

| Risco | Prevenção | Solução |
| :---: | :--- | :---: |
| R01 | Capacitação prévia da equipe e escolha adequada de tecnologias | Buscar apoio externo, estudos adicionais ou simplificação da solução |
| R02 | Documentação do projeto e compartilhamento de conhecimento | Redistribuição das tarefas entre os membros restantes |
| R03 | Planejamento de horários e definição de reuniões fixas | Reorganização do cronograma e uso de comunicação assíncrona |
| R04 | Definição clara de requisitos e controle de mudanças | Replanejamento do projeto e priorização de funcionalidades |
| R05 | Distribuição equilibrada de tarefas | Redistribuição das atividades e ajuste no cronograma |
| R06 | Agendamento prévio de reuniões com cliente/especialistas, formulário único de aceite e validação prévia das histórias na reunião semanal | Lembrete pelo canal que o PO usa (WhatsApp) e continuidade do desenvolvimento com base em suposições documentadas até a validação |
| R07 | Planejamento adequado da carga de trabalho | Redistribuição de tarefas e ajuste de prazos |
| R08 | Manutenção preventiva e uso de backup de arquivos | Utilização de equipamentos alternativos (laboratório ou empréstimo), recuperação de dados e redistribuição temporária das tarefas |
| R09 | Planejamento das atividades considerando dependências | Reorganização da ordem das tarefas e ajuste no cronograma |
| R10 | Testes de persistência de dados e rotina de backup/exportação periódica | Recuperação a partir do último backup e revisão do mecanismo de gravação local |
| R11 | Testes contínuos e validações frequentes com o cliente | Correção da solução e ajustes nos requisitos |
| R12 | Busca antecipada por bases de dados adequadas | Utilização de dados alternativos ou adaptação da solução |
| R13 | Validação incremental do modelo com dados de teste desde as primeiras sprints | Ajustar o modelo, buscar mais dados ou simplificar o problema a ser resolvido |
| R14 | Anonimização de dados e boas práticas de segurança desde o início do projeto | Revisão do tratamento de dados e adequação às exigências da LGPD |

## Monitoramento dos Riscos

Os riscos são revisados ao fim de cada sprint, na *sprint review*. A revisão reavalia a probabilidade e o impacto de todos os riscos, registra os que se concretizaram e entra no histórico abaixo. O histórico só contém sprints que já aconteceram: uma sprint ganha coluna depois da sua revisão, nunca antes.

Os dados ficam versionados em `analytics-raw-data/riscos_historico.json`, e a classificação atual em `analytics-raw-data/riscos_analytics.json`. O dashboard lê esses dois arquivos e descarta qualquer revisão com data futura.

<iframe width="700" height="400" src="https://docs.google.com/spreadsheets/d/1ZarJ5KuICboZrPrMZGIZyJAHq8Ju39r4wP2-Lx8_pqc/preview"></iframe>

### Gráfico Impacto X Probabilidade de cada Risco por Sprint

<iframe width="1200" height="700" frameborder="0" scrolling="no" src="https://docs.google.com/spreadsheets/d/e/2PACX-1vTejXRkOfqXWpRfc1pocJMvWkX0TJ5t-oaOfZRiwPMVeY88WhsgXMddbEWA_K1EpaSrunR9_o0qTtCw/pubchart?oid=1663055085&amp;format=interactive"></iframe>

### Gráfico Impacto X Probabilidade Total por Sprint

<iframe width="700" height="400" frameborder="0" scrolling="no" src="https://docs.google.com/spreadsheets/d/e/2PACX-1vTejXRkOfqXWpRfc1pocJMvWkX0TJ5t-oaOfZRiwPMVeY88WhsgXMddbEWA_K1EpaSrunR9_o0qTtCw/pubchart?oid=365709643&format=interactive"></iframe>


### Rotina de revisão a cada sprint

1. Na *sprint review*, reavaliar probabilidade e impacto de cada risco com a escala deste plano.
2. Registrar os riscos que se concretizaram na sprint: data, impacto observado e resposta aplicada.
3. Acrescentar a revisão em `riscos_historico.json` e uma coluna na tabela de histórico abaixo.
4. Atualizar `riscos_analytics.json` com a classificação atual e o histórico de versões deste documento.

### Histórico de revisões por sprint

**Tabela:** Classificação dos riscos nas sprints realizadas

| Risco | Sprint 1 · R1 (até 13/09) | Sprint 2 · R1 (até 27/09) | Sprint 3 · R2 (até 11/10) | Sprint 4 · R2 (até 25/10) | Sprint 5 · R3 (até 08/11) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| R01 | 4 × 4 = 16 (Elevado) | 4 × 4 = 16 (Elevado) | 3 × 4 = 12 (Médio) | 3 × 5 = 15 (Elevado) | 3 × 5 = 15 (Elevado) |
| R02 | 1 × 3 = 3 (Baixo) | 4 × 3 = 12 (Médio) | 4 × 3 = 12 (Médio) | 3 × 3 = 9 (Médio) | 3 × 3 = 9 (Médio) |
| R03 | 4 × 3 = 12 (Médio) | 4 × 3 = 12 (Médio) | 3 × 4 = 12 (Médio) | 3 × 2 = 6 (Médio) | 4 × 2 = 8 (Médio) |
| R04 | 3 × 3 = 9 (Médio) | 3 × 3 = 9 (Médio) | 2 × 3 = 6 (Médio) | 2 × 3 = 6 (Médio) | 3 × 3 = 9 (Médio) |
| R05 | 2 × 2 = 4 (Baixo) | 2 × 2 = 4 (Baixo) | 2 × 3 = 6 (Médio) | 1 × 2 = 2 (Baixo) | 1 × 2 = 2 (Baixo) |
| R06 | 2 × 3 = 6 (Médio) | 2 × 3 = 6 (Médio) | 2 × 2 = 4 (Baixo) | 2 × 3 = 6 (Médio) | 5 × 4 = 20 (Elevado) |
| R07 | 1 × 2 = 2 (Baixo) | 2 × 2 = 4 (Baixo) | 2 × 2 = 4 (Baixo) | 2 × 2 = 4 (Baixo) | 1 × 2 = 2 (Baixo) |
| R08 | 1 × 2 = 2 (Baixo) | 1 × 2 = 2 (Baixo) | 1 × 2 = 2 (Baixo) | 1 × 2 = 2 (Baixo) | 4 × 3 = 12 (Médio) |
| R09 | 1 × 3 = 3 (Baixo) | 1 × 3 = 3 (Baixo) | 2 × 3 = 6 (Médio) | 3 × 4 = 12 (Médio) | 3 × 4 = 12 (Médio) |
| R10 | 3 × 3 = 9 (Médio) | 3 × 3 = 9 (Médio) | 3 × 3 = 9 (Médio) | 2 × 3 = 6 (Médio) | 2 × 3 = 6 (Médio) |
| R11 | 1 × 4 = 4 (Baixo) | 1 × 4 = 4 (Baixo) | 2 × 4 = 8 (Médio) | 4 × 4 = 16 (Elevado) | 5 × 4 = 20 (Elevado) |
| R12 | 2 × 3 = 6 (Médio) | 2 × 3 = 6 (Médio) | 2 × 3 = 6 (Médio) | 2 × 3 = 6 (Médio) | 3 × 3 = 9 (Médio) |
| R13 | 2 × 4 = 8 (Médio) | 2 × 4 = 8 (Médio) | 3 × 4 = 12 (Médio) | 2 × 4 = 8 (Médio) | 2 × 4 = 8 (Médio) |
| R14 | 1 × 3 = 3 (Baixo) | 1 × 3 = 3 (Baixo) | 1 × 3 = 3 (Baixo) | 2 × 4 = 8 (Médio) | 2 × 4 = 8 (Médio) |
| **Total** | **87** | **98** | **102** | **106** | **140** |

Formato: probabilidade × impacto = severidade (grau). A classificação atual, usada na matriz do dashboard, é a da Sprint 5. A probabilidade do R02 sobe de 1 para 4 da Sprint 1 para a Sprint 2 porque o risco se concretizou na Sprint 2.

#### Justificativa das mudanças na Sprint 5

| Risco | Sprint 4 → Sprint 5 | Motivo |
| :---: | :---: | :--- |
| R03 | 6 → 8 | Algumas reuniões da R2 aconteceram sem todos os integrantes. A probabilidade sobe um nível; o impacto se mantém, porque as ausências foram pontuais. |
| R04 | 6 → 9 | Entrou no escopo da R3 o perfil de superusuário, pedido pelo PO na [Ata 11](../atas-reunioes/Ata-11-EPS-2026-10-30-PO.md) e confirmado na [Ata 12](../atas-reunioes/Ata-12-EPS-2026-11-09-PO.md). É uma história nova, mas de tamanho moderado, por isso só a probabilidade sobe. |
| R06 | 6 → 20 | O risco se concretizou: o retorno do PO e do cliente sobre as entregas tem sido mais lento do que o planejado, com o formulário de aceite e histórias enviadas ao Discord ainda pendentes, ausências em reuniões e encaminhamentos combinados, como a avaliação de novos modelos de IA, ainda sem resposta. Ver [Riscos concretizados](#riscos-concretizados). |
| R07 | 4 → 2 | As tarefas foram bem distribuídas entre os integrantes e ninguém ficou sobrecarregado na R2, nem está previsto ficar na R3. |
| R08 | 2 → 12 | Na R2, um integrante teve problema no equipamento e ficou um longo período sem conseguir contribuir. A probabilidade sobe de 1 para 4 e o impacto de 2 para 3, porque a perda de capacidade foi maior do que a prevista. |
| R11 | 16 → 20 | O modelo de IA escolhido erra com frequência nos testes feitos no tablet, e o PO e o cliente avaliam trocá-lo ou reduzir o escopo ao desenho do relógio ([Ata 12](../atas-reunioes/Ata-12-EPS-2026-11-09-PO.md)). |
| R12 | 6 → 9 | O problema da IA está nos dados: as imagens do conjunto atual têm resolução baixa e a equipe busca um novo conjunto com o cliente ([Ata 12](../atas-reunioes/Ata-12-EPS-2026-11-09-PO.md)). O impacto se mantém, porque o desenvolvimento do aplicativo não depende do conjunto. |

Os demais riscos se mantêm: R01 (a dificuldade com as tecnologias continua a mesma), R02 (ninguém saiu da equipe desde a Sprint 2), R05 (ninguém ficou doente, e o risco já está no nível mais baixo de probabilidade), R09 e R10 (não ocorreram; os dados ficam no dispositivo e não há dado crítico a perder durante o desenvolvimento), R13 (o treinamento do modelo não foi o problema, e sim os dados, tratados no R12) e R14 (o aplicativo roda offline e os dados não saem do tablet).

A [planilha de monitoramento](https://docs.google.com/spreadsheets/d/1ZarJ5KuICboZrPrMZGIZyJAHq8Ju39r4wP2-Lx8_pqc/edit?usp=sharing) segue como apoio da equipe e deve conter as mesmas sprints desta tabela.

### Riscos concretizados

#### R02 — Saída de algum integrante do projeto

| Item | Registro |
| :--- | :--- |
| Quando | 24/09/2026, na Sprint 2 (R1), após a *Sprint Review* de 23/09/2026 ([Ata 07](../atas-reunioes/Ata-07-EPS-2026-09-23-PO.md)) |
| O que aconteceu | Marcelo Araújo dos Santos trancou a disciplina ([Ata 08](../atas-reunioes/Ata-08-EPS-2026-10-02-PO.md)) |
| Impacto | A equipe passou de 11 para 10 integrantes. As atividades dele na R1 precisaram ser assumidas pelos demais para fechar a release. A partir da Sprint 3 (R2), são 18 horas a menos por semana, cerca de 9% da capacidade (de 198 para 180 horas semanais), ou 72 horas nas 4 semanas da R2 |
| Resposta aplicada | As atividades que estavam com o integrante foram redistribuídas entre os 10 integrantes restantes, o que permitiu concluir a R1. O [plano de custos](plano_de_custos.md) foi recalculado com 10 integrantes a partir da R2 |

O R02 continua sendo monitorado, porque outra saída ainda pode acontecer até o fim do semestre.

#### R06 — Indisponibilidade do cliente ou de especialistas para esclarecimento de requisitos e aceite das entregas

| Item | Registro |
| :--- | :--- |
| Quando | Sprint 5 (R3). Apontado na reunião de 30/10/2026 ([Ata 11](../atas-reunioes/Ata-11-EPS-2026-10-30-PO.md)) e ainda pendente em 09/11/2026 ([Ata 12](../atas-reunioes/Ata-12-EPS-2026-11-09-PO.md)) |
| O que aconteceu | O formulário único de aceite das histórias da R1 e da R2 ficou sem resposta do PO, e as histórias #10, #23 e #17, enviadas ao Discord, também seguiam sem retorno. O cliente respondeu ao formulário e validou as entregas. Na Ata 11, o professor apontou a falta de retorno como o maior risco do projeto |
| Impacto | Histórias concluídas ficam na coluna de aceitação do ZenHub, a *velocity* da R2 ficou zerada porque só conta pontos com aceite formal, e o planejamento da reta final depende de validações que ainda não chegaram |
| Resposta aplicada | Formulário único de aceite com todas as histórias pendentes e o APK; validação prévia das histórias da R3 na própria reunião semanal; lembrete por WhatsApp, canal que o PO usa. Na Ata 12, ficou combinado que a equipe segue o desenvolvimento quando não houver resposta e ajusta no caminho se o PO ou o cliente pedirem mudança. O PO se comprometeu a responder o formulário até 11/11/2026 |

O R06 continua sendo monitorado até o aceite final da R3.

## Conclusão

A gestão de riscos é essencial no desenvolvimento de software para garantir que possíveis problemas sejam identificados e tratados antes de impactarem significativamente o projeto. Este Plano de Gestão de Riscos fornece uma abordagem sistemática para identificar, analisar e mitigar riscos, minimizando incertezas e maximizando as chances de sucesso. Com a categorização detalhada dos riscos, suas causas e consequências, e a elaboração de estratégias de prevenção e solução, o plano assegura que a equipe esteja preparada para enfrentar desafios e realizar entregas com qualidade e dentro do prazo. A revisão contínua e a participação ativa da equipe são fundamentais para adaptar-se a novos riscos e ajustar estratégias conforme necessário, garantindo uma trajetória segura e eficiente rumo à entrega de um produto final de alta qualidade.

### R1

Na Release 1, o foco da equipe está na construção da base inicial do aplicativo e na validação do primeiro fluxo funcional. Os principais riscos estão relacionados à adaptação da equipe às tecnologias escolhidas, à disponibilidade dos integrantes e à implementação da autenticação.

O risco R02 se concretizou na Sprint 2, com a saída de um integrante em 24/09/2026 (ver [Riscos concretizados](#riscos-concretizados)). As atividades do integrante foram redistribuídas e a R1 foi concluída. A redução da equipe de 11 para 10 integrantes vale a partir da Sprint 3 e exige organização e distribuição equilibrada das atividades restantes. A equipe deve estar atenta à comunicação e ao planejamento para evitar atrasos e garantir que as entregas sejam concluídas com sucesso.

### R3

Na Release 3, os riscos mais altos são o R06 e o R11, ambos de grau Elevado. O R06 se concretizou: o aceite das entregas depende de um retorno do PO e do cliente que tem sido mais lento que o planejado, e a equipe passou a validar as histórias na própria reunião semanal e a seguir o desenvolvimento quando não há resposta. O R11 subiu porque o modelo de IA ainda não tem a precisão esperada e pode ser trocado, o que se reflete também no R12, pela qualidade dos dados. O R08 subiu depois que um integrante ficou um longo período sem equipamento na R2.

## Histórico de versões

| Versão | Descrição | Autor | Data | Revisor | Data de revisão |
|---|---|---|---|---|---|
| 1.0 | Criação da documentação de riscos | [Eduardo Ferreira](https://github.com/eduardoferre) | 27/09/2026 | A definir | — |
| 1.1 | Adição dos gráficos de impacto e probabilidade e conclusão da R1 | [Eduardo Ferreira](https://github.com/eduardoferre) | 27/09/2026 | A definir | — |
| 1.2 | Escala única de classificação com o dashboard, histórico apenas das sprints realizadas, registro do R02 concretizado | [Eduardo Ferreira](https://github.com/eduardoferre) | 25/10/2026 | A definir | — |
| 1.3 | Revisão da Sprint 5 (R3) com justificativa de cada mudança, R06 registrado como risco concretizado e conclusão da R3 | [Daniel Ferreira Nunes](https://github.com/Mach1r0) | 15/11/2026 | A definir | — |
