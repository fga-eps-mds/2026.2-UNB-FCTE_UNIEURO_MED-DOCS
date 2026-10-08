# Visão do Produto — Canvas MVP

Esta página faz parte da Visão do Produto do MED e registra a Atividade 10 da Lean Inception. O Canvas MVP consolida em um único quadro a proposta do produto mínimo viável, as personas, as jornadas, as funcionalidades, as hipóteses a validar, as métricas de validação e o custo estimado. Ela fecha a sequência iniciada em [Lean Inception](lean-inception.md) e detalhada em [Funcionalidades](funcionalidades.md) e [Sequenciador](sequenciador.md). A leitura condensada de tudo está em [Visão do Produto](visao.md).

## 1. Proposta do MVP

Aplicativo Android local no tablet. Aplica o teste. O modelo embarcado gera o resultado. Mostra o desenho e o resultado ao profissional de saúde. Testa se a IA classifica como o especialista.

## 2. Segmentos de clientes e usuários

- **Seu José**, paciente idoso, faz o teste.
- **Profissional de saúde**, aplica o teste e lê o resultado.
- Escala inicial de validação: 1 ambulatório, com 1 ou 2 profissionais.

## 3. Jornadas

- **J1** — Seu José faz a triagem, ou seja, os desenhos.
- **J2** — O profissional de saúde aplica e interpreta.
- **J3** — Primeiro uso, sem login e sem modo demonstração.

O detalhamento passo a passo das três jornadas está em [Lean Inception](lean-inception.md).

## 4. Funcionalidades do MVP

| Grupo | Funcionalidades referenciadas no quadro |
|---|---|
| Teste de desenho | F1, F2, F3, F6, F7 |
| Captura de imagem e traçado | F10, F11 |
| Armazenamento local | F24 |
| Inferência e resultado | F15, F16 |
| Resultado ao profissional | F18, F8 |
| Registro e conformidade | F22, F26, F27 |

Esta numeração vem do próprio quadro e não corresponde à lista consolidada em [Funcionalidades](funcionalidades.md). As duas precisam ser unificadas para que o escopo do MVP seja rastreável.

## 5. Hipóteses a validar

- **H1** — O resultado concorda com o especialista.
- **H2** — O idoso desenha sozinho.
- **H3** — Cabe no tempo da consulta.
- **H4** — O modelo tem significado clínico.
- **H5** — O profissional confia no que vê.

## 6. Métricas para validar as hipóteses

Cada hipótese tem pelo menos uma métrica que a equipe consegue medir até o fim do semestre, com o próprio aplicativo, com o repositório de IA ou nos testes com o *Product Owner* e o cliente. As metas marcadas como proposta ainda precisam do aceite do *Product Owner*.

| Hipótese | Métrica | Como medir | Quando | Meta |
|---|---|---|---|---|
| H1 — O resultado concorda com o especialista | AUC e F1-score do modelo no conjunto de teste, com o MoCA como referência | Avaliação do modelo no repositório de IA ([IA #4](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-IA/issues/4)) | R2 e R3 | Linha de base: AUC de 0,765 no [modelo base](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-IA/blob/docs/resultados-modelo-base/docs/resultados-modelo-base.md). Proposta: AUC de pelo menos 0,80, perto do 0,838 do artigo |
| H1 — O resultado concorda com o especialista | Mesma classe entre o modelo original e o modelo exportado no tablet | Conjunto de conferência rodado nos dois ([IA #6](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-IA/issues/6)) | R3 | Todos os casos com a mesma classe |
| H2 — O idoso desenha sozinho | Percentual de tarefas concluídas sem ajuda | Sessões de teste de usabilidade com voluntários de 60 anos ou mais, sem dado de saúde | R3 | Proposta: pelo menos 80% das tarefas |
| H2 — O idoso desenha sozinho | Apagamentos e desistências por sessão | Registro automático do aplicativo ([Ata 06](../atas-reunioes/Ata-06-EPS-2026-09-15-PO.md)) nas mesmas sessões | R3 | Valor registrado por sessão, para comparar entre as releases |
| H3 — Cabe no tempo da consulta | Tempo do fluxo completo, do início da avaliação ao resultado | Tempo registrado pelo aplicativo, sem exibir ao paciente ([Ata 07](../atas-reunioes/Ata-07-EPS-2026-09-23-PO.md)), nas sessões de usabilidade e no teste de aceitação | R3 e RF | Proposta: até 10 minutos |
| H3 — Cabe no tempo da consulta | Tempo da inferência no tablet do parceiro | Medição no aparelho com o modelo exportado ([IA #6](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-IA/issues/6), [APP #12](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/12)) | R3 | Limite combinado com o parceiro na IA #6 |
| H4 — O modelo tem significado clínico | AUC por faixa de escolaridade no conjunto de teste | Relatório por faixa no repositório de IA ([IA #5](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-IA/issues/5)) | R3 | Relatório publicado e limites de uso revisados pelo parceiro |
| H5 — O profissional confia no que vê | Aceite das histórias do resultado e nota de confiança de 1 a 5 | Instrumento de teste de aceitação do *Product Owner* e do cliente ([APP #13](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/13), [APP #14](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/14)) | R3 e RF | Proposta: histórias aceitas e nota de pelo menos 4 |

### 6.1 Métricas que dependem do uso real

Estas métricas estavam no quadro original. Elas só podem ser medidas com o aplicativo em uso no ambulatório, depois do semestre, e ficam registradas para a continuidade do projeto.

| Métrica | Por que fica para depois |
|---|---|
| Concordância do modelo com dois especialistas | Precisa de pacientes reais avaliados pelo aplicativo e por dois especialistas |
| Concordância entre os próprios especialistas | Precisa da mesma coleta com dois especialistas |
| Desempenho em desenhos nunca vistos, coletados no ambulatório | O conjunto de dados atual é público e já foi usado no treino e no teste |
| Percentual de aplicações em que o profissional olhou o desenho | Só tem sentido em consultas reais, não em teste de aceitação |
| Número de instruções reformuladas | Depende do protocolo aplicado por profissionais no dia a dia |

## 7. Custo e cronograma

### 7.1 Custo

O custo vem do [Plano de Custos](../processo/plano_de_custos.md), que soma pessoas, computadores, energia e internet. O produto não tem custo de servidor, licença ou hospedagem, porque roda 100% offline, e usa um tablet Android comum, sem custo se a instituição já tiver o aparelho.

| Período | Semanas | Custo planejado | Acumulado |
|---|---:|---:|---:|
| R1 — 10/08 a 28/09 | 7 | R$ 25.294,46 | R$ 25.294,46 |
| R2 — 29/09 a 26/10 | 4 | R$ 13.139,98 | R$ 38.434,44 |
| R3 — 27/10 a 30/11 | 5 | R$ 16.424,97 | R$ 54.859,41 |
| Release final — 01/12 a 07/12 | 1 | R$ 3.285,00 | R$ 58.144,41 |
| **Total** | **17** | **R$ 58.144,41** | |

O Plano de Custos está sendo recalculado pelo valor da hora, com o orçamento por release ([DOCS #75](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-DOCS/issues/75)). Quando ele mudar, esta tabela acompanha.

### 7.2 Cronograma

As datas vêm do [Cronograma](../processo/cronograma.md), e o recorte de cada release, do [Roadmap](../processo/roadmap.md). As métricas da seção 6 são medidas nas releases indicadas na tabela delas.

| Data | Release | Objetivo |
|---|---|---|
| 28/09 | R1 | Telas de cadastro e login |
| 13/10 | Release minor 1 | Conta do profissional completa e tela inicial |
| 26/10 | R2 | Cadastro e login offline, atendimento e TCLE registrados e primeiro desenho no tablet |
| 09/11 | Release minor 2 | Incremento das três tarefas e da captura |
| 30/11 | R3 — MVP | Três tarefas, captura, inferência e resultado no tablet, e exportação do XML |
| 07/12 | Release final | Correções, acessibilidade e teste de aceitação final com o cliente |
| 14/12 | Encerramento | APK, documentação e resultados das métricas |

## Histórico de Versões

| Versão | Descrição | Autor(es) | Data | Revisor(es) | Data de Revisão |
|---|---|---|---|---|---|
| 1.0 | Criação da página com o registro da Atividade 10 da Lean Inception, transcrita do quadro de Visão do Produto | [Artur Mendonça Arruda](https://github.com/ArtyMend07) | 18/09/2026 | [Lucas Mendonça Arruda](https://github.com/lucasarruda9) | 19/09/2026 |
