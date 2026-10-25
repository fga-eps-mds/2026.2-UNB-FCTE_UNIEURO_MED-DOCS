# Processo e comparação R1 × R2

Esta página apresenta os indicadores de processo, normalizados entre 0 e 1, e a
comparação entre a R1 e a R2 de velocidade, cobertura e defeitos, como pede o
cronograma da disciplina para o DA-R2. Os valores são do dia **22/10/2026**. A R2 fecha
em 26/10, e a Sprint 3 ainda está em andamento.

A qualidade do produto pelo modelo Q-Rapids está em
[Qualidade do produto](qualidade-do-produto.md).

## Indicadores de processo

O [Plano de Qualidade](../processo/plano_de_qualidade.md) define o modelo de qualidade
do produto, mas não o do processo. Os três indicadores abaixo usam dados que a coleta
diária já grava e seguem o mesmo princípio do plano: valor entre 0 e 1, sem dado é
"não medido", e as faixas de leitura são as da Tabela 3 do plano.

**Tabela 1:** Indicadores de processo

| Id | Indicador | Fórmula | Fonte |
|---|---|---|---|
| P1 | Estabilidade do CI | execuções com sucesso / execuções concluídas com sucesso ou falha, no APP e na IA | `GitHub_API-Runs-*.json` |
| P2 | Entrega do comprometido | pontos de história aceitos / pontos planejados, em média por sprint | `zenhub_analytics.json` |
| P3 | Estabilidade do escopo | pontos que já estavam na sprint no início / pontos planejados ao final, em média por sprint | `zenhub_analytics.json` |
| P | Índice de processo | `(P1 + P2 + P3) / 3` | — |

**Fonte:** [Gabriel Lopes de Amorim](https://github.com/BrzGab), 2026

Cada sprint entra na release em que termina, e sprints sem pontos planejados, como as de
preparação, ficam de fora. P2 e P3 são médias por sprint, porque somar os pontos de uma
release contaria duas vezes a história que passa de uma sprint para a outra. Execuções
puladas ou canceladas não entram em P1, porque não dizem se o código está estável.

!!! warning "Proposta para validação"
    Os indicadores e os pesos iguais são uma proposta e ainda precisam ser aprovados pelo
    time e validados com o professor, como os limiares do Q-Rapids.

**Tabela 2:** Indicadores de processo por release

| Release | Sprints | P1 | P2 | P3 | P |
|---|---|---:|---:|---:|---:|
| R1 | Sprint 1 | 0,94 | 0,00 | 1,00 | 0,65 Atenção |
| R2 (em andamento) | Sprints 2 e 3 | 0,97 | 0,00 | 0,77 | 0,58 Crítico |

**Fonte:** [Gabriel Lopes de Amorim](https://github.com/BrzGab), 2026

### Interpretação

**O índice de processo está crítico por causa da entrega (P2 = 0).** Nenhum ponto de
história foi aceito pelos *Product Owners* em nenhuma sprint. Há código entregue e
testado, mas sem aceite a história não conta como concluída. As histórias #6, #46 e #7
estão na coluna Aceitação PO desde a versão 1.2.0, de 13/10.

**O escopo da R2 mudou durante a sprint (P3 = 0,77).** A Sprint 2 manteve o escopo
planejado, mas na Sprint 3 entraram 32 dos 69 pontos com a sprint em andamento: as
histórias #21, #8, #9 e #10, apresentadas aos *Product Owners* em 19/10.

**O CI está estável (P1 = 0,97).** Na R2, 71 de 73 execuções concluídas terminaram com
sucesso no APP e na IA.

## Comparação R1 × R2

**Tabela 3:** Velocidade, cobertura e defeitos por release

| Indicador | R1 | R2 (até 22/10) |
|---|---:|---:|
| Velocidade (pontos de história aceitos por sprint) | 0 | 0 |
| Pontos planejados por sprint | 21,0 | 54,5 |
| Cobertura de testes do APP | 96,0% (v1.0.0) | 97,5% (v1.2.3) |
| Issues de bug abertas na release | 0 | 1 |
| Arquivos do APP com defeito provável no SonarCloud | 1 | 2 |

**Fonte:** [Gabriel Lopes de Amorim](https://github.com/BrzGab), 2026

- **Velocidade.** Zero nas duas releases, pelo mesmo motivo de P2. Os pontos planejados
  por sprint mais que dobraram, o que aumenta o que fica esperando aceite.
- **Cobertura.** Subiu de 96,0% para 97,5%, acima dos 85% que o cronograma pede para a
  R2, com o número de arquivos de código passando de 18 para 44.
- **Defeitos.** A única issue de bug, a
  [APP #52](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/52)
  (*promises* da *splash screen* sem tratamento), foi aberta e corrigida em 05/10. Os
  defeitos prováveis apontados pelo SonarCloud passaram de 1 para 2 arquivos: o
  problema do `registration.ts` continua aberto desde a R1, e o `cpf-protection.ts`
  ganhou um em 08/10.

## Como os valores são obtidos

O cálculo está em
[`dashboard/src/processo.py`](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-DOCS/blob/main/dashboard/src/processo.py),
e os testes em `dashboard/tests/test_processo.py`. Para refazer as tabelas, a partir da
pasta `dashboard/`:

```bash
python3 -m src.processo
python3 -m unittest discover tests
```

A cobertura e os defeitos prováveis da R1 vêm da versão 1.0.0, e os da R2, por enquanto,
da versão 1.2.3, as mesmas usadas no Q-Rapids. As issues de bug vêm do arquivo
`GitHub_API-Bugs-*.json`, descrito em [Coleta de métricas](coleta-de-metricas.md).

## Limitações

- **Sprint 3 em andamento.** P2, P3 e a velocidade da R2 mudam se houver aceite antes de
  26/10.
- **Bugs só com rótulo.** A contagem considera apenas as issues com o rótulo `bug`.
  Defeitos corrigidos direto em PR, sem issue, não aparecem.
- **Pontos da ZenHub.** Os pontos planejados e entregues vêm da sprint do ZenHub no
  momento da coleta, e não de um histórico diário.

## Histórico de versão

| Versão | Data | Descrição | Autor | Revisor |
|:------:|------|-----------|-------|---------|
| `1.0` | 22/10/2026 | Indicadores de processo e comparação R1 × R2 de velocidade, cobertura e defeitos | [Gabriel Lopes de Amorim](https://github.com/BrzGab) | |
