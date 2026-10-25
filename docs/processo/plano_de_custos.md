# Plano de Gerenciamento de Custos

## 1. Objetivo

Este plano estima o custo do projeto MED no semestre 2026.2 e o define **por release**: o orçamento de cada release (BAC) é o seu próprio custo. Ele serve de base para o monitoramento por EVM-Ágil no Dashboard Gerencial e Analítico e deve permanecer alinhado ao [cronograma](../processo/cronograma.md), ao [roadmap](../processo/roadmap.md) e ao [Canvas MVP](../produto/canvas-mvp.md).

!!! note "Natureza da estimativa"
    Os valores são uma estimativa acadêmica de planejamento e controle. Não constituem prestação de contas da UnB, da UNIEURO ou do cliente.

## 2. Premissas

| Premissa | Valor adotado |
|---|---|
| Período do projeto | 17 semanas, de 10/08 a 07/12/2026 |
| Equipe de EPS | 11 integrantes na R1 e 10 a partir da R2 |
| Esforço por integrante na disciplina | 18 horas por semana: 4 de aula (dois encontros por semana) e 14 de trabalho extraclasse (2 horas por dia, de segunda a domingo) |
| Carga anual de um estudante | 40 créditos: 20 por semestre, ou 5 disciplinas de 4 créditos |
| Custo anual médio por estudante da UnB | R$ 53.123,21 |
| Custo da disciplina por estudante | R$ 5.312,32 (4 créditos), nas 17 semanas do semestre |
| Valor da hora do estudante | R$ 17,36 (seção 3) |
| Computador | R$ 3.500,00 por unidade, pelo valor de compra, um por integrante |
| Energia elétrica | 40 W por computador nas horas extraclasse, a R$ 0,82 por kWh |
| Internet | R$ 100,00 por mês, rateados por hora de mês (720 h), nas horas extraclasse |
| Tablet Android | Disponibilizado pelo parceiro, fora do custo da equipe |
| Servidor, hospedagem e licenças | R$ 0,00: o produto opera offline e usa planos educacionais ou gratuitos |

O custo anual médio por estudante é a dotação atualizada da UnB em 2026 (R$ 2.700.943.579,00) dividida pelos 50.843 estudantes regulares, conforme as referências 1 e 3. As horas de aula acontecem na rede e nas instalações da Universidade, por isso energia e internet consideram só as horas extraclasse, feitas em casa. Os valores do computador, da energia e da internet são estimativas de referência, a substituir pelos valores reais levantados com a equipe. O tablet e a decisão de manter o produto offline estão registrados no [Canvas MVP](../produto/canvas-mvp.md#7-custo-e-cronograma).

!!! info "Saída de integrante"
    Marcelo Araújo dos Santos trancou a disciplina após a Sprint Review de 23/09/2026 (Ata 07). A R1 permanece calculada com 11 integrantes e, a partir da R2, com 10.

## 3. Valor da hora do estudante

O valor do trabalho não usa salário de mercado. Seguindo a orientação registrada na [Ata 04](../atas-reunioes/Ata-04-EPS-2026-09-11-PO.md#orientacoes-do-professor-sobre-o-canvas-mvp), adota-se o custo médio da UnB por estudante, que é dividido pelos créditos até chegar à hora da disciplina.

1. **Custo por crédito.** `R$ 53.123,21 ÷ 40 créditos por ano = R$ 1.328,08 por crédito`. A média de 40 créditos anuais corresponde a 5 disciplinas de 4 créditos por semestre.
2. **Custo da disciplina por estudante.** `4 créditos × R$ 1.328,08 = R$ 5.312,32`, distribuídos nas 17 semanas do semestre, ou R$ 312,49 por semana.
3. **Horas do estudante na disciplina.** `18 horas por semana × 17 semanas = 306 horas`.
4. **Valor da hora.** `R$ 5.312,32 ÷ 306 horas = R$ 17,36 por hora`.

O custo anual cobre todas as disciplinas do estudante. O que se divide pelas horas do projeto é só a parte que cabe a esta disciplina, 4 dos 40 créditos anuais. Por isso o custo de pessoas de cada integrante é o da disciplina, R$ 5.312,32 em 17 semanas.

## 4. Horas do projeto

As horas de cada release são `integrantes × 18 horas × semanas`. As horas extraclasse (`integrantes × 14 horas × semanas`) servem de base para energia e internet.

| Release | Período | Semanas | Integrantes | Horas do projeto | Horas extraclasse |
|---|---|---:|---:|---:|---:|
| R1 | 10/08 a 28/09 | 7 | 11 | 1.386 | 1.078 |
| R2 | 29/09 a 26/10 | 4 | 10 | 720 | 560 |
| R3 | 27/10 a 30/11 | 5 | 10 | 900 | 700 |
| Release final | 01/12 a 07/12 | 1 | 10 | 180 | 140 |
| **Total** | | **17** | | **3.186** | **2.478** |

## 5. Custo e BAC por release

O custo de pessoas é `horas do projeto × valor da hora`. Os computadores entram pelo valor de compra, uma única vez, na R1, que é quando passam a ser usados: 11 unidades, pois a integrante que saiu usou o seu computador na R1. Energia e internet são calculadas por integrante e por semana (R$ 0,46 e R$ 1,94).

| Release | Pessoas | Computadores | Energia | Internet | **BAC da release** |
|---|---:|---:|---:|---:|---:|
| R1 | R$ 24.061,69 | R$ 38.500,00 | R$ 35,36 | R$ 149,72 | **R$ 62.746,77** |
| R2 | R$ 12.499,58 | R$ 0,00 | R$ 18,37 | R$ 77,78 | **R$ 12.595,73** |
| R3 | R$ 15.624,47 | R$ 0,00 | R$ 22,96 | R$ 97,22 | **R$ 15.744,66** |
| Release final | R$ 3.124,89 | R$ 0,00 | R$ 4,59 | R$ 19,44 | **R$ 3.148,93** |
| **Custo do projeto** | R$ 55.310,64 | R$ 38.500,00 | R$ 81,28 | R$ 344,17 | **R$ 94.236,09** |

Os valores usam o valor da hora sem arredondar. O custo do projeto é a soma dos BAC das releases; ele não é um BAC. A R1 concentra 67% do custo porque inclui a compra dos computadores à vista.

Há uma **reserva gerencial de 5%** sobre o custo do projeto, de R$ 4.711,80, separada dos BAC. Ela só entra em um BAC por mudança aprovada (seção 7). O orçamento total autorizado é de R$ 98.947,89.

Esta memória de cálculo também está em [CSV versionado](../assets/dados/plano_de_custos.csv).

## 6. Monitoramento por EVM-Ágil

O EVM-Ágil é calculado **por release**, com o BAC da seção 5 e os pontos das histórias de usuário (nunca de tarefas). O dashboard aplica estas mesmas definições.

| Sigla | Indicador | Cálculo |
|---|---|---|
| BAC | Orçamento da release | Valor da seção 5 |
| PRP | Pontos planejados da release | Pontos das histórias estimadas da release |
| RPC | Pontos entregues | Pontos das histórias concluídas e aceitas |
| PPC | Prazo decorrido | Dias decorridos ÷ dias da release |
| APC | Escopo concluído | RPC ÷ PRP |
| PV | Valor planejado | PPC × BAC |
| EV | Valor agregado | APC × BAC |
| AC | Custo real | Custo incorrido até a data |
| SV e CV | Variações de prazo e de custo | EV − PV e EV − AC |
| SPI e CPI | Índices de prazo e de custo | EV ÷ PV e EV ÷ AC |
| EAC | Estimativa no término | AC + (BAC − EV) ÷ CPI |

Limites para a tomada de decisão:

| Estado | CPI e SPI | Ação esperada |
|---|---:|---|
| Adequado | ≥ 0,90 | Manter o plano e acompanhar semanalmente |
| Atenção | 0,80 a 0,89 | Investigar a causa e registrar a ação corretiva |
| Crítico | < 0,80 | Replanejar escopo, capacidade ou prazo e submeter mudança |

Limites desta medição: o PRP só é confiável com o backlog da release inteiramente estimado; e, enquanto não houver custo real apurado, o AC é estimado pela linha de base (PPC × BAC), o que faz o CPI coincidir com o SPI. Os índices são atualizados ao fim de cada sprint, e o BAC usado no dashboard deve ser sempre o da seção 5.

## 7. Controle e aprovação de mudanças

Uma revisão do custo é necessária quando ocorrer pelo menos uma destas situações:

- entrada ou saída de integrante;
- alteração do número de semanas ou da carga semanal de horas;
- aquisição de computador, tablet ou GPU, ou contratação de serviço pago;
- variação acumulada superior a 5% do custo de uma release;
- mudança de escopo que altere materialmente a capacidade planejada.

O processo de controle é:

1. registrar a necessidade e a causa em uma issue;
2. calcular o impacto no BAC das releases e na reserva;
3. discutir a mudança com a equipe e os responsáveis pelo projeto;
4. aprovar ou rejeitar com evidência rastreável;
5. atualizar este documento, os dados do EVM e o dashboard;
6. registrar a alteração no histórico de versões.

### Registro de ajustes estruturais

| Data | Mudança | Impacto | Custo do projeto | Evidência | Responsável |
|---|---|---:|---:|---|---|
| 21/09/2026 | Criação da linha de base inicial | n/a | R$ 61.284,29 | Versão 1.0 deste documento | Daniel Ferreira Nunes |
| 22/09/2026 | Atualização da fonte de pessoas para o orçamento da UnB em 2026 | + R$ 17.520,70 | R$ 78.804,99 | Painel Gestão UnB e Anuário Estatístico 2025 | Daniel Ferreira Nunes |
| 22/09/2026 | Adoção do total oficial de 50.843 estudantes como denominador | − R$ 17.375,58 | R$ 61.429,41 | Tabela 2.18 do Anuário Estatístico 2025 | Daniel Ferreira Nunes |
| 26/09/2026 | Saída de integrante a partir da R2 (10 semanas com 10 integrantes) | − R$ 3.285,00 | R$ 58.144,41 | Trancamento da disciplina; última participação na Ata 07 | Daniel Ferreira Nunes |
| 12/10/2026 | Recálculo pelo valor da hora (custo por crédito e 18 h semanais na disciplina), BAC por release e computador pelo valor de compra | + R$ 36.091,68 | R$ 94.236,09 | Avaliação da R1 (Ata 08) e issue #75 | Cláudio Henrique dos Santos Carvalho |

## 8. Responsabilidades e frequência

| Atividade | Responsável | Frequência |
|---|---|---|
| Manter premissas e custo por release | Responsável pelo Plano de Custos | Sob demanda |
| Atualizar PV, EV, AC, CPI, SPI e EAC | Frente de gestão e dashboard | Ao fim de cada sprint |
| Validar pontos concluídos | Liderança da sprint e responsáveis pelas histórias | Ao fim de cada sprint |
| Analisar desvios e propor resposta | Equipe | Sprint Review |
| Aprovar alteração do custo | Equipe e responsável pelo projeto | Sob demanda |

## 9. Referências

1. UNIVERSIDADE DE BRASÍLIA. [Painel Gestão UnB](https://app.powerbi.com/view?r=eyJrIjoiZWNjNzkzZWQtNTJkMi00YmZhLThkOTgtNzgzNmE2MWMzZjdmIiwidCI6ImVjMzU5YmExLTYzMGItNGQyYi1iODMzLWM4ZTZkNDhmODA1OSJ9). Dotação atualizada de 2026, com fechamento contábil em 20 set. 2026. Acesso em: 22 set. 2026.
2. UNIVERSIDADE DE BRASÍLIA. [Painel Gestão UnB: uma nova ferramenta de transparência e eficiência para a gestão universitária](https://daf.unb.br/destaques/238-painel-de-gestao-projeta-unb-como-modelo-de-transparencia-publica). Decanato de Administração. Acesso em: 22 set. 2026.
3. UNIVERSIDADE DE BRASÍLIA. [Anuário Estatístico 2025, ano-base 2024: tabela 2.18](https://anuariounb2025.netlify.app/geral#alunos-regulares-na-graduacao-e-na-pos-graduacao-stricto-sensu-2020-a-2024-2o-semestre). Total de 50.843 estudantes regulares. Acesso em: 22 set. 2026.
4. NEOENERGIA BRASÍLIA. [Composição tarifária](https://www.neoenergia.com/web/brasilia/sua-casa/composicao-tarifaria). Acesso em: 21 set. 2026.
5. SULAIMAN, T.; BARTON, B.; BLACKBURN, T. AgileEVM: Earned Value Management in Scrum Projects. In: AGILE 2006 CONFERENCE, 2006.
6. PROJECT MANAGEMENT INSTITUTE. *A Guide to the Project Management Body of Knowledge (PMBOK Guide)*. 7. ed. Newtown Square: PMI, 2021.

## Histórico de versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) | Data de revisão |
|---|---|---|---|---|---|
| 1.0 | 21/09/2026 | Criação do plano, linha de base, distribuição por release e controle por EVM-Ágil | [Daniel Ferreira Nunes](https://github.com/Mach1r0) | n/a | n/a |
| 1.1 | 22/09/2026 | Atualização do orçamento por estudante com dados do Painel Gestão UnB e recálculo da linha de base | [Daniel Ferreira Nunes](https://github.com/Mach1r0) | n/a | n/a |
| 1.2 | 22/09/2026 | Inclusão do Repositório DPO e adoção do total oficial de 50.843 estudantes da tabela 2.18 | [Daniel Ferreira Nunes](https://github.com/Mach1r0) | n/a | n/a |
| 1.3 | 26/09/2026 | Recálculo da linha de base após o trancamento de um integrante: 11 integrantes na R1 e 10 a partir da R2 | [Daniel Ferreira Nunes](https://github.com/Mach1r0) | n/a | n/a |
| 2.0 | 12/10/2026 | Refeito pelo valor da hora do estudante e pelas horas do projeto, com BAC por release, computadores pelo valor de compra e texto enxugado, conforme a avaliação da R1 | [Cláudio Henrique dos Santos Carvalho](https://github.com/claudiohsc) | n/a | n/a |
