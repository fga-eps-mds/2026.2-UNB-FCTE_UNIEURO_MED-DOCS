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

## 7. Custo e cronograma

- 34 dias de dupla, equivalentes a 11 ou 12 semanas.
- Tablet Android, com custo zero caso o hospital já disponha do equipamento.
- Sem servidor, sem licença e sem hospedagem, consequência direta da decisão de operar 100% offline.

O detalhamento e a validação desses números são tratados no Plano de Custos, pacote 1.1.5 da EAP.

## Histórico de Versões

| Versão | Descrição | Autor(es) | Data | Revisor(es) | Data de Revisão |
|---|---|---|---|---|---|
| 1.0 | Criação da página com o registro da Atividade 10 da Lean Inception, transcrita do quadro de Visão do Produto | [Artur Mendonça Arruda](https://github.com/ArtyMend07) | 18/09/2026 | [Lucas Mendonça Arruda](https://github.com/lucasarruda9) | 19/09/2026 |
