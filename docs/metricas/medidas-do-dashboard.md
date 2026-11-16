# Medidas do dashboard

Esta página explica cada medida que o dashboard mostra: de onde vem, como é calculada, em que
unidade, o que ela não diz e uma frase para explicá-la ao cliente. Qualquer integrante deve
conseguir apresentar qualquer número do painel a partir dela. Os números do momento estão em
[Qualidade do produto](qualidade-do-produto.md), em [Processo e comparação R1 × R2](processo-e-comparativo.md)
e no próprio dashboard; as fontes dos dados, em [Coleta de métricas](coleta-de-metricas.md).

Duas regras valem para todas as medidas:

- **Sem dado, "não medida".** Uma medida sem dado aparece como `N/A` ou `n/m`, nunca como zero.
- **Cite o modo.** Os pontos entregues têm dois modos, escolhidos na barra lateral: somente as
  histórias **aceitas** (fechadas depois do aceite do PO) ou também as que estão em **Aceitação PO**
  (código entregue, aceite pendente). Ao apresentar um número de entrega, diga o modo.

## Agile EVM (projeto)

O Agile EVM compara, em reais, o que estava planejado com o que foi entregue. É calculado por
release, porque é a release que tem orçamento e escopo próprios. A origem é Sulaiman, Barton e
Blackburn (2006), e o cálculo está em `dashboard/src/metrics.py`.

**Tabela 1:** Medidas do Agile EVM

| Medida | Origem e fórmula | Unidade | Limitação | Para o cliente |
|---|---|---|---|---|
| BAC | Orçamento da release, da seção 5 do [Plano de Custos](../processo/plano_de_custos.md) | R$ | Só muda com mudança formal do plano | "É o orçamento previsto para esta release." |
| PRP | ZenHub: pontos das histórias cotadas nas sprints que terminam na release (a primeira em que têm estimativa), cada uma contada uma vez, na release de cotação | pontos de história | Só é confiável se todas as histórias estiverem estimadas; issue sem estimativa vale 0 | "É o tamanho do que prometemos entregar nesta release." |
| RPC | ZenHub: pontos entregues nessas sprints, conforme o modo | pontos de história | Depende do aceite do PO; no modo "aceitas", espera de aceite zera o valor | "É o tanto do que prometemos que já está pronto." |
| PPC | Dias decorridos da release ÷ dias da release | 0 a 1 | Mede só calendário, não esforço | "É quanto do prazo já passou." |
| APC | RPC ÷ PRP, limitado a 1 | 0 a 1 | Herda os limites do PRP e do RPC | "É quanto do escopo já está entregue." |
| PV | PPC × BAC | R$ | É linear no tempo; não considera que o trabalho não é uniforme | "É o valor que já deveria estar entregue neste ponto do prazo." |
| EV | APC × BAC | R$ | Mede o que foi produzido, não o que foi gasto | "É o valor do que já foi entregue." |
| AC | PPC × BAC (estimado) | R$ | Não há custo real apurado, então AC = PV | "Ainda estimamos o custo pelo plano, porque não medimos o gasto real." |
| SPI | EV ÷ PV | índice | Com AC estimado, é igual ao CPI. Abaixo de 1 é menos entrega que o planejado | "1 é o planejado; abaixo disso, entregamos menos do que o prazo pede." |
| CPI | EV ÷ AC | índice | Repete o SPI enquanto o AC for estimado | "Compara o valor entregue com o custo; hoje repete o SPI." |
| SV e CV | EV − PV e EV − AC | R$ | Mesmos limites do SPI e do CPI | "É a diferença, em reais, entre o entregue e o planejado." |
| ETC e EAC | (BAC − EV) ÷ CPI e AC + ETC | R$ | Sem custo real, é uma projeção a partir de estimativas | "É a projeção do custo restante e do custo final se o ritmo continuar." |

**Fonte:** [Cláudio Henrique dos Santos Carvalho](https://github.com/claudiohsc), 2026

As faixas do SPI e do CPI seguem a seção 6 do Plano de Custos: **Adequado** a partir de 0,90,
**Atenção** de 0,80 a 0,89 e **Crítico** abaixo de 0,80. As barras partem do zero e a linha de
referência é 1,0. Um índice zero com histórias em Aceitação PO aparece como "aguardando aceite",
porque indica espera do aceite do PO, e não necessariamente atraso do time.

O **gráfico de custo** soma as releases e mostra PV, AC e EV acumulados do projeto. Como o AC é
estimado, a linha dele repete a do PV.

## Pontos, velocity e aceite

**Tabela 2:** Medidas de pontos entregues

| Medida | Origem e fórmula | Unidade | Limitação | Para o cliente |
|---|---|---|---|---|
| Pontos aceitos | ZenHub: `delivered_story_points`, as histórias fechadas | pontos de história | Só conta depois do aceite do PO | "São as histórias que o PO já validou." |
| Em Aceitação PO | ZenHub: histórias abertas na coluna Aceitação PO, com estimativa, contadas uma vez | pontos de história | Retrato do momento da coleta; se o PO devolve a história, o número cai | "É o que já entregamos e aguarda a validação do PO." |
| Aceite depois do fim da sprint | História fechada que esperou o PO volta para a sprint em que foi cotada (a primeira com estimativa) | pontos de história | Depende do estado e da data de fechamento da issue, que a coleta passou a gravar. Se o ZenHub tira a história da sprint aberta depois do aceite, os pontos entram na sprint de origem sem sair de outra. Supõe que a equipe entregou a história na sprint em que a cotou, e o painel não separa a que ficou mais de uma sprint em andamento | "A espera pelo aceite não conta contra a sprint que fez a entrega." |
| Velocity | Pontos entregues por sprint fechada; a média é a das sprints fechadas | pontos por sprint | Sprint com poucos pontos pode refletir histórias maiores ou trabalho sem pontos | "É quanto a equipe entrega, em média, a cada duas semanas." |
| Burnup e burndown | Pontos acumulados da release contra o PRP e contra o ritmo ideal | pontos de história | Se o PRP muda, as curvas se ajustam | "Mostram o quanto falta e se o ritmo basta para terminar no prazo." |

**Fonte:** [Cláudio Henrique dos Santos Carvalho](https://github.com/claudiohsc), 2026

A seção **Aceitas × entregues, lado a lado** da aba de EVM mostra os dois modos juntos, com o
escopo aceito, o escopo entregue e o prazo decorrido. Se só o escopo entregue acompanha o prazo, o
atraso nos índices vem da espera do aceite, e não do desenvolvimento.

## Processo e CI/CD

**Tabela 3:** Medidas de processo

| Medida | Origem e fórmula | Unidade | Limitação | Para o cliente |
|---|---|---|---|---|
| P1, estabilidade do CI | GitHub Actions: execuções com sucesso ÷ execuções com sucesso ou falha, em APP e IA | 0 a 1 | Execuções puladas ou canceladas ficam de fora | "Mostra com que frequência a verificação automática do código passa." |
| P2, escopo concluído | É o APC da release (RPC ÷ PRP), igual ao da aba de EVM | 0 a 1 | Segue o modo de pontos entregues | "É a parte do escopo da release que já está concluída." |
| P3, estabilidade do PRP | ZenHub: PRP no início ÷ PRP no fim da sprint, em média por sprint | 0 a 1 | Cai quando entram histórias com a sprint em andamento | "Mostra o quanto o plano da sprint mudou depois que ela começou." |
| P, índice de processo | (P1 + P2 + P3) ÷ 3 | 0 a 1 | Proposta da equipe, com pesos iguais, ainda em validação | "Resume em um número a saúde do nosso processo." |
| Taxa de sucesso e tempo mediano do pipeline | GitHub Actions: execuções concluídas; a mediana da duração | % e minutos | A mediana evita que execuções atípicas distorçam o valor | "Mostra se a verificação automática é estável e rápida." |

**Fonte:** [Cláudio Henrique dos Santos Carvalho](https://github.com/claudiohsc), 2026

As faixas de leitura dos índices de 0 a 1 são as do Plano de Qualidade: **Adequado** a partir de
0,80, **Atenção** de 0,60 a 0,79 e **Crítico** abaixo de 0,60.

## Qualidade do produto (Q-Rapids)

A qualidade interna segue o modelo Q-Rapids do [Plano de Qualidade](../processo/plano_de_qualidade.md)
(seção 3), calculado em `dashboard/src/qualidade.py` sobre as medidas do SonarCloud por arquivo. As
métricas m1 a m8 são **densidades**: arquivos que cumprem o limiar ÷ arquivos medidos. Os detalhes de
cada resultado estão em [Qualidade do produto](qualidade-do-produto.md).

**Tabela 4:** Métricas, fatores e características

| Medida | Origem e fórmula | Unidade | Limitação | Para o cliente |
|---|---|---|---|---|
| m1, arquivos não complexos | Complexidade por função abaixo de 10 | 0 a 1 | Só arquivos com função | "Quanto do código é simples de entender." |
| m2, arquivos comentados | Comentários entre 10% e 30% das linhas | 0 a 1 | Comentário em quantidade certa não garante comentário útil | "Quanto do código está explicado." |
| m3, arquivos sem duplicação | Duplicação abaixo de 5% | 0 a 1 | Código duplicado em arquivos diferentes pode passar | "Quanto do código evita repetição desnecessária." |
| m4, sucesso dos testes | Testes que passam ÷ testes executados | 0 a 1 | Não medida se o SonarCloud não recebe o resultado | "Quantos dos testes automáticos passam." |
| m5, testes rápidos | Arquivos de teste que levam menos de 5 s | 0 a 1 | Testes lentos podem ser necessários, como os que usam o banco real | "Quanto da verificação automática roda rápido." |
| m6, cobertura adequada | Arquivos com cobertura de 75% ou mais | 0 a 1 | Arquivos sem cobertura medida ficam de fora | "Quanto do código é exercitado pelos testes." |
| m7, sem problema grave de manutenibilidade | Arquivos sem problema de impacto alto ou bloqueante | 0 a 1 | É uma densidade: o mesmo problema pesa menos num código maior | "Quanto do código está livre de problemas graves de manutenção." |
| m8, sem problema de confiabilidade | Arquivos sem problema de confiabilidade | 0 a 1 | Idem | "Quanto do código está livre de erros prováveis." |
| Fatores QC, CB, T, ST e DP | Média ponderada: QC = m1, m2, m3; CB = m7; T = m5 (peso 1) e m6 (peso 2); ST = m4; DP = m8 | 0 a 1 | Falta de uma métrica divide o peso entre as demais e marca o valor como parcial (`*`) | "Agrupam as métricas em temas." |
| Características M e C | M = média de QC, CB e T; C = média de ST e DP | 0 a 1 | Cobrem manutenibilidade e confiabilidade, não toda a ISO/IEC 25010 | "Dizem se o código é fácil de manter e se é confiável." |
| Q, índice de qualidade | Média de M e C | 0 a 1 | Só vale pelas características que cobre | "Resume em um número a qualidade interna do código." |
| Indicadores do SonarCloud | Linhas de código, cobertura, duplicação, bugs, vulnerabilidades, code smells, security hotspots e notas A a E | contagens, % e letras | A nota reflete o pior problema não corrigido, não uma média | "É a leitura direta da ferramenta de análise do código." |

**Fonte:** [Cláudio Henrique dos Santos Carvalho](https://github.com/claudiohsc), 2026

## Qualidade por característica (SonarCloud)

A aba de Qualidade de Produto abre com as quatro características do Plano de Qualidade, na release escolhida, e as medidas do SonarCloud ficam num bloco de detalhe.

**Tabela 5:** Medidas de qualidade por característica

| Medida | Origem e fórmula | Unidade | Limitação | Para o cliente |
|---|---|---|---|---|
| Segurança | Nota de segurança do SonarCloud (A a E), pelas vulnerabilidades abertas, no último ponto do histórico até o fim da release | nota | Hotspots revisados e as evidências E4 a E6 do plano ainda não são coletados | "Diz se o código tem brechas de segurança conhecidas." |
| Confiabilidade | Nota de confiabilidade do SonarCloud, pela gravidade do pior bug aberto | nota | A nota reflete o pior problema, não uma média | "Diz se o código tem erros prováveis." |
| Manutenibilidade | Nota SQALE do SonarCloud, pela razão entre o débito técnico e o tamanho do código | nota | Débito técnico é estimativa da ferramenta | "Diz se o código é fácil de evoluir." |
| Testabilidade | Cobertura global de testes do SonarCloud, com o total de testes ao lado | % | O SonarCloud não separa os testes por nível (unitário, integração e funcional) e cobertura não garante que o comportamento esteja certo | "Diz quanto do código os testes automáticos exercitam." |
| Faixa | Nota A é Adequado, B é Atenção e C a E é Crítico; cobertura de 90% ou mais é Adequado, de 80% a 89,9% é Atenção e abaixo de 80% é Crítico | faixa | Os limites vêm do Plano de Qualidade e aguardam a validação do professor | "Diz se a característica está dentro da meta." |
| Sentido da mudança | Compara o valor da release com o da anterior: melhorou, piorou ou manteve (variação menor que 0,5 nota ou ponto de cobertura é ruído) | texto | Sem valor numa das releases, aparece "sem comparação", e na primeira, "primeira medição" | "Diz se a qualidade subiu ou caiu desde a release passada." |

**Fonte:** [Cláudio Henrique dos Santos Carvalho](https://github.com/claudiohsc), 2026

## Gestão de riscos

**Tabela 6:** Medidas de risco

| Medida | Origem e fórmula | Unidade | Limitação | Para o cliente |
|---|---|---|---|---|
| Severidade do risco | [Plano de Gestão de Riscos](../processo/riscos.md): probabilidade (1 a 5) × impacto (1 a 5) | 1 a 25 | Os valores são julgamento da equipe, transcritos a cada sprint review | "Mostra o quanto cada risco merece atenção." |
| Grau do risco | Baixo de 1 a 5, Médio de 6 a 12, Elevado de 15 a 25 | faixa | Nenhum produto dá 13 ou 14, por isso a faixa Elevado começa em 15 | "Classifica o risco em baixo, médio ou elevado." |

**Fonte:** [Cláudio Henrique dos Santos Carvalho](https://github.com/claudiohsc), 2026

## O que o dashboard ainda não mede

- **Segurança por inteiro.** A característica já aparece pela nota do SonarCloud, mas os hotspots
  revisados e as evidências E4 a E6 do plano ainda não são coletados. O Q-Rapids continua só com
  manutenibilidade e confiabilidade.
- **Testabilidade por nível.** O SonarCloud informa a cobertura e o total de testes, sem separar
  unitário, integração e funcional.
- **Throughput e lead time.** Dependem das datas de movimentação das issues entre colunas do ZenHub.
- **Custo real.** Enquanto não houver custo real apurado, o AC é estimado e o CPI repete o SPI.

## Histórico de versão

| Versão | Data | Descrição | Autor | Revisor |
|:------:|------|-----------|-------|---------|
| `1.0` | 11/11/2026 | Criação da página com origem, fórmula, unidade, limitação e frase para o cliente de cada medida | [Cláudio Henrique dos Santos Carvalho](https://github.com/claudiohsc) | |
| `1.1` | 15/11/2026 | Inclusão das medidas de qualidade por característica e dos limites que ainda restam | [Cláudio Henrique dos Santos Carvalho](https://github.com/claudiohsc) | |
| `1.2` | 16/11/2026 | O aceite tardio conta na sprint em que a história foi cotada, e não na última sprint encerrada em que aparece | [Cláudio Henrique dos Santos Carvalho](https://github.com/claudiohsc) | |
| `1.3` | 16/11/2026 | O PRP de cada release passa a contar só as histórias cotadas nela, e não as que vieram de releases anteriores | [Cláudio Henrique dos Santos Carvalho](https://github.com/claudiohsc) | |
| `1.4` | 17/11/2026 | O aceite tardio conta na sprint de origem mesmo quando o ZenHub tira a história da sprint em que ela fechou | [Cláudio Henrique dos Santos Carvalho](https://github.com/claudiohsc) | |
