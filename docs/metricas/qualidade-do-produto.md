# Qualidade do produto (Q-Rapids)

Esta página apresenta a qualidade interna do produto medida pelo modelo Q-Rapids,
como define o [Plano de Qualidade](../processo/plano_de_qualidade.md) (seção 3), e
compara as releases R1, RM1 e R2. Os valores são do dia **22/10/2026**, com a versão
v1.2.3 do aplicativo. A R2 fecha em 26/10, e a coluna dela será atualizada com a
última versão gerada até lá.

## Como os valores são obtidos

**Tabela 1:** Dados de entrada do cálculo

| Dado | Arquivo em `analytics-raw-data/` | Usado em |
|---|---|---|
| Medidas do SonarCloud por arquivo, gravadas a cada release | `fga-eps-mds-<repositório>-<data>-vX.Y.Z.json` | m1 a m6 |
| Problemas do SonarCloud por branch, abertos e resolvidos | `Sonar_API-Issues-<repositório>.json` | m7 e m8 |
| Branch de destino de cada release | `GitHub_API-Releases-<repositório>.json` | Escolher os problemas da branch que a release mediu |

**Fonte:** [Gabriel Lopes de Amorim](https://github.com/BrzGab), 2026

O cálculo está em [`dashboard/src/qualidade.py`](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-DOCS/blob/main/dashboard/src/qualidade.py)
e segue as fórmulas, os limiares e os pesos das Tabelas 2 e 3 e da seção 3.3 do plano.
Os testes em `dashboard/tests/test_qualidade.py` conferem cada fórmula. Para refazer as
tabelas desta página, a partir da pasta `dashboard/`:

```bash
python3 -m src.qualidade          # tabelas por versão e por release
python3 -m unittest discover tests
```

Cada release é representada pela última versão medida até a data dela: a R1 pela
v1.0.0, de 28/09, a RM1 pela v1.2.0, de 13/10, e a R2, por enquanto, pela v1.2.3, de 22/10.

## Resultados do aplicativo (MED-APP)

**Tabela 2:** Métricas, fatores, características e índice Q por release

| Indicador | R1 (v1.0.0) | RM1 (v1.2.0) | R2 (v1.2.3) |
|---|---:|---:|---:|
| m1 Arquivos não complexos | 1,00 | 1,00 | 1,00 |
| m2 Arquivos comentados | 0,22 | 0,24 | 0,25 |
| m3 Arquivos sem duplicação | 0,89 | 0,98 | 0,98 |
| m4 Sucesso dos testes | não medida | 1,00 | 1,00 |
| m5 Arquivos de teste rápidos | não medida | 0,82 | 0,82 |
| m6 Arquivos com cobertura adequada | 1,00 | 1,00 | 1,00 |
| m7 Arquivos sem problema grave de manutenibilidade | 0,94 | 0,98 | 0,98 |
| m8 Arquivos sem problema de confiabilidade | 0,94 | 0,95 | 0,95 |
| **QC** Qualidade do código | 0,70 Atenção | 0,74 Atenção | 0,74 Atenção |
| **CB** Código bloqueante | 0,94 Adequado | 0,98 Adequado | 0,98 Adequado |
| **T** Testabilidade | 1,00\* Adequado | 0,94 Adequado | 0,94 Adequado |
| **ST** Sucesso dos testes | não medida | 1,00 Adequado | 1,00 Adequado |
| **DP** Defeitos prováveis | 0,94 Adequado | 0,95 Adequado | 0,95 Adequado |
| **M** Manutenibilidade | 0,88\* Adequado | 0,88 Adequado | 0,89 Adequado |
| **C** Confiabilidade | 0,94\* Adequado | 0,98 Adequado | 0,98 Adequado |
| **Q** Índice de qualidade | 0,91\* Adequado | 0,93 Adequado | 0,93 Adequado |

\* Valor parcial: falta pelo menos uma métrica abaixo dele, e o peso dela foi dividido
entre as demais, como manda a seção 3.3 do plano.

**Fonte:** [Gabriel Lopes de Amorim](https://github.com/BrzGab), 2026

### Interpretação

**O produto está na faixa adequada (Q = 0,93), com um fator em atenção.** Nenhum
fator, característica ou índice caiu 0,05 ou mais entre duas versões seguidas, o que
dispensa a análise de queda da seção 3.5.

**Qualidade do código em atenção (QC = 0,74), por causa dos comentários (m2 = 0,25).**
Na v1.2.3, 33 dos 44 arquivos de código ficam fora da faixa de 10% a 30% de linhas de
comentário, e quase todos estão abaixo dela. A complexidade (m1 = 1,00) e a duplicação
(m3 = 0,98) estão adequadas. O plano pede, para essa faixa, a análise da causa e o
registro da decisão. A Tabela 4 do plano orienta comentar as regras de negócio e as
restrições, e não acrescentar comentários óbvios só para subir a métrica.

**Da R1 para a R2, só a duplicação melhorou de fato.** Em m3, o
`register-screen.tsx` deixou de ter duplicação, e só o `login-screen.tsx` segue acima de
5%. Já m7 e m8 subiram porque o código cresceu, de 18 para 44 arquivos, e não porque os
problemas foram resolvidos: o `registration.ts` tem um problema grave de
manutenibilidade e um de confiabilidade desde a R1, e o `cpf-protection.ts` ganhou um
problema de confiabilidade em 08/10. Como as métricas são densidades, o mesmo problema
pesa menos num código maior, e a leitura precisa olhar também a lista de arquivos.

**Três problemas do SonarCloud seguem abertos na `develop`** e explicam m7 e m8
abaixo de 1,00:

**Tabela 3:** Problemas abertos que afetam m7 e m8

| Arquivo | Regra | Impacto | Aberto desde |
|---|---|---|---|
| `src/features/auth/registration.ts` | S3776, complexidade cognitiva | Manutenibilidade alta (m7) | 08/10 |
| `src/features/auth/registration.ts` | S8786, expressão regular lenta | Confiabilidade média (m8) | 26/09 |
| `src/db/cpf-protection.ts` | S7758, `String.fromCharCode` | Confiabilidade baixa (m8) | 08/10 |

**Fonte:** [Gabriel Lopes de Amorim](https://github.com/BrzGab), 2026

**Testes rápidos no limite (m5 = 0,82).** Sete dos 38 arquivos de teste levam 5 s ou
mais. Os mais lentos são os que montam o banco SQLite real: a tela de novo exame
(14,4 s), o cadastro (11,9 s) e o fluxo de cadastro e login (10,3 s).

**Cobertura adequada em todos os arquivos medidos (m6 = 1,00).** O arquivo com menor
cobertura tem 90,3%. Dez arquivos não têm cobertura medida e ficam fora da conta: as
rotas em `src/app/` e os arquivos `.web`, excluídos na configuração do SonarCloud, e
arquivos sem linha executável, como o CSS.

## Resultados do modelo de IA (MED-IA)

**A qualidade interna do MED-IA não está medida na R2.** O único `.json` de release é o
da v0.0.1, de 27/09, com 3 arquivos e sem testes, e a última análise do SonarCloud é
de 17/09, com 19 linhas de código. O código atual da exportação do modelo e os testes
em Python ainda não passam pelo SonarCloud: isso depende da
[IA #13](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-IA/issues/13), em
andamento. Pelo princípio do plano, o valor fica como não medido, e não como zero.

## Limitações da medição

- **Testes da R1.** O SonarCloud só passou a receber o resultado e o tempo dos testes do
  aplicativo na v1.0.2, de 05/10. Por isso m4 e m5 da R1 são não medidas, e T, C, M e Q
  da R1 são parciais. Uma comparação com valor parcial não gera alerta de queda.
- **Data dos problemas.** O SonarCloud registra como criação de um problema a data do
  commit da linha, e não a da análise que o encontrou. Na reconstrução de m7 e m8 de
  versões antigas, um problema pode aparecer alguns dias antes de ter sido apontado.
- **Versão sem dados.** O `.json` da v1.0.1 veio vazio. A versão fica de fora do cálculo.
- **Arquivos de código.** O conjunto A inclui todo arquivo com linha de código, como
  o `global.css`, que não tem comentários e conta contra m2.

## Pontos para as decisões gerenciais da R2

Os resultados apontam três assuntos para a equipe decidir e registrar no dashboard:

1. **Comentários (QC em atenção):** comentar as regras de negócio dos arquivos que
   não têm nenhuma explicação, ou registrar que a faixa de 10% a 30% não se aplica a
   arquivos de estilo e de rota e ajustar o plano.
2. **Problemas abertos (m7 e m8):** corrigir os três problemas da Tabela 3 antes da R2,
   o que levaria m7 e m8 a 1,00, ou registrar a exceção com responsável e prazo.
3. **IA sem medição:** priorizar a IA #13 para que o MED-IA tenha qualidade medida na
   R3.

## Série completa do aplicativo

**Tabela 4:** Indicadores de cada versão do MED-APP

| Versão | Branch | m1 | m2 | m3 | m4 | m5 | m6 | m7 | m8 | QC | CB | T | ST | DP | M | C | Q |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| v0.0.1 | develop | 1,00 | 0,22 | 0,89 | n/m | n/m | 1,00 | 0,94 | 0,89 | 0,70 | 0,94 | 1,00\* | n/m | 0,89 | 0,88\* | 0,89\* | 0,89\* |
| v1.0.0 | main | 1,00 | 0,22 | 0,89 | n/m | n/m | 1,00 | 0,94 | 0,94 | 0,70 | 0,94 | 1,00\* | n/m | 0,94 | 0,88\* | 0,94\* | 0,91\* |
| v1.0.1 | develop | n/m | n/m | n/m | n/m | n/m | n/m | n/m | n/m | n/m | n/m | n/m | n/m | n/m | n/m | n/m | n/m |
| v1.0.2 | develop | 1,00 | 0,17 | 0,89 | 1,00 | 0,78 | 1,00 | 0,94 | 0,94 | 0,69 | 0,94 | 0,93 | 1,00 | 0,94 | 0,85 | 0,97 | 0,91 |
| v1.0.3 | develop | 1,00 | 0,15 | 0,90 | 1,00 | 0,82 | 1,00 | 0,95 | 0,95 | 0,68 | 0,95 | 0,94 | 1,00 | 0,95 | 0,86 | 0,97 | 0,92 |
| v1.0.4 | develop | 1,00 | 0,26 | 0,91 | 1,00 | 0,87 | 1,00 | 0,96 | 0,91 | 0,72 | 0,96 | 0,96 | 1,00 | 0,91 | 0,88 | 0,96 | 0,92 |
| v1.0.5 | develop | 1,00 | 0,25 | 0,96 | 1,00 | 0,88 | 1,00 | 0,96 | 0,92 | 0,74 | 0,96 | 0,96 | 1,00 | 0,92 | 0,88 | 0,96 | 0,92 |
| v1.1.0 | develop | 1,00 | 0,26 | 0,97 | 1,00 | 0,85 | 1,00 | 0,97 | 0,94 | 0,74 | 0,97 | 0,95 | 1,00 | 0,94 | 0,89 | 0,97 | 0,93 |
| v1.1.1 | develop | 1,00 | 0,24 | 0,98 | 1,00 | 0,93 | 1,00 | 0,98 | 0,95 | 0,74 | 0,98 | 0,98 | 1,00 | 0,95 | 0,90 | 0,98 | 0,94 |
| v1.1.2 | develop | 1,00 | 0,24 | 0,98 | 1,00 | 0,93 | 1,00 | 0,98 | 0,95 | 0,74 | 0,98 | 0,98 | 1,00 | 0,95 | 0,90 | 0,98 | 0,94 |
| v1.1.3 | develop | 1,00 | 0,24 | 0,98 | 1,00 | 0,93 | 1,00 | 0,98 | 0,95 | 0,74 | 0,98 | 0,98 | 1,00 | 0,95 | 0,90 | 0,98 | 0,94 |
| v1.1.4 | develop | 1,00 | 0,24 | 0,98 | 1,00 | 0,82 | 1,00 | 0,98 | 0,95 | 0,74 | 0,98 | 0,94 | 1,00 | 0,95 | 0,88 | 0,98 | 0,93 |
| v1.2.0 | main | 1,00 | 0,24 | 0,98 | 1,00 | 0,82 | 1,00 | 0,98 | 0,95 | 0,74 | 0,98 | 0,94 | 1,00 | 0,95 | 0,88 | 0,98 | 0,93 |
| v1.2.1 | develop | 1,00 | 0,24 | 0,98 | 1,00 | 0,83 | 1,00 | 0,98 | 0,95 | 0,74 | 0,98 | 0,94 | 1,00 | 0,95 | 0,89 | 0,98 | 0,93 |
| v1.2.2 | develop | 1,00 | 0,25 | 0,98 | 1,00 | 0,84 | 1,00 | 0,98 | 0,95 | 0,74 | 0,98 | 0,95 | 1,00 | 0,95 | 0,89 | 0,98 | 0,93 |
| v1.2.3 | develop | 1,00 | 0,25 | 0,98 | 1,00 | 0,82 | 1,00 | 0,98 | 0,95 | 0,74 | 0,98 | 0,94 | 1,00 | 0,95 | 0,89 | 0,98 | 0,93 |

n/m: não medida. \* Valor parcial.

**Fonte:** [Gabriel Lopes de Amorim](https://github.com/BrzGab), 2026

## Referências

MARTÍNEZ-FERNÁNDEZ, Silverio et al. A quality model for actionable analytics in rapid
software development. In: *Euromicro Conference on Software Engineering and Advanced
Applications (SEAA)*, 44., 2018, Praga. Anais [...]. IEEE, 2018. p. 370-377.

LETOUZEY, Jean-Louis; COQ, Thierry. The SQALE analysis model: an analysis model
compliant with the representation condition for assessing the quality of software
source code. In: *International Conference on Advances in System Testing and
Validation Lifecycle (VALID)*, 2., 2010, Nice. Anais [...]. IEEE, 2010. p. 43-48.

INTERNATIONAL ORGANIZATION FOR STANDARDIZATION. *ISO/IEC 25010:2011*: Systems and
software engineering — Systems and software Quality Requirements and Evaluation
(SQuaRE) — System and software quality models. Genebra: ISO, 2011.

## Histórico de versão

| Versão | Data | Descrição | Autor | Revisor |
|:------:|------|-----------|-------|---------|
| `1.0` | 22/10/2026 | Cálculo do Q-Rapids por versão e comparação entre R1, RM1 e R2 | [Gabriel Lopes de Amorim](https://github.com/BrzGab) | |
