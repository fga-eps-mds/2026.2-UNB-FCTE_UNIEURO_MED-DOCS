# Coleta de métricas

O dashboard analítico não consulta APIs durante a renderização: ele lê arquivos
`.json` previamente gerados em `analytics/raw-data/`. Quando um arquivo não
existe, a seção correspondente exibe um conjunto de dados de exemplo e sinaliza
isso na tela.

Esta página descreve quais arquivos existem, quem os gera e o que falta.

## Situação atual

**Tabela 1:** Fontes de dados do dashboard

| Arquivo | Alimenta | Origem | Situação |
|---|---|---|---|
| `GitHub_API-Runs-*.json` | Fluxo de CI/CD (processo) | API do GitHub Actions | Automatizado |
| `Sonar_API-Measures-*.json` | Qualidade de produto | API do SonarCloud | Automatizado |
| `zenhub_analytics.json` | Sprints e Agile EVM (projeto) | API do Zenhub | Automatizado — depende do *secret* |
| `riscos_analytics.json` | Matriz de Riscos (projeto) | Plano de Riscos | Pendente — depende da issue #26 |

**Fonte:** [Vitor Carvalho Pereira](https://github.com/vcpVitor), 2026

## Execuções de CI/CD

O workflow [`coleta-metricas.yml`](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-DOCS/blob/main/.github/workflows/coleta-metricas.yml)
consulta a API do GitHub Actions para os três repositórios do projeto e grava um
arquivo por repositório.

Ele roda **diariamente às 06:00** (horário de Brasília) e também sob acionamento
manual, pela aba *Actions*. Não roda em *push* para a `main` de propósito: o job
faz commit de volta no repositório, e um gatilho de push criaria um laço de
execuções.

Usa o `GITHUB_TOKEN` da própria esteira — não requer nenhum segredo adicional.
Se a coleta de um repositório falhar, o arquivo anterior é preservado e o
workflow registra um aviso em vez de falhar por inteiro.

### Formato

```json
{
  "repositorio": "IA",
  "coletado_em": "2026-09-20T19:30:00Z",
  "workflow_runs": [
    {
      "id": 35531017733,
      "name": "Build",
      "head_branch": "docs/resultados-modelo-base",
      "event": "pull_request",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-09-20T19:02:59Z",
      "updated_at": "2026-09-20T19:03:40Z",
      "run_number": 6,
      "html_url": "https://github.com/..."
    }
  ]
}
```

A partir desses campos o dashboard deriva o total de execuções, a taxa de
sucesso e o tempo médio de retorno da esteira.

## Qualidade de produto

O Plano de Ensino é explícito quanto a esta fonte: os dashboards devem consumir
os arquivos `.json` de métricas geradas automaticamente pelos pipelines de CI/CD
a partir do SonarCloud.

O mesmo workflow coleta, para cada projeto analisado, as medidas atuais e a série
histórica: linhas de código, cobertura, testes, *bugs*, vulnerabilidades, *code
smells*, *security hotspots*, densidade de duplicação, dívida técnica, as três
notas de avaliação e o estado do *quality gate*.

A API do SonarCloud é **aberta para projetos públicos** — a coleta não usa token
nem depende de nenhum *secret*.

Apenas **APP** e **IA** são analisados. O repositório de documentação não possui
projeto no SonarCloud, por não conter código de produção.

### Ausência de cobertura

Quando um projeto não tem testes, o SonarCloud **não devolve** a métrica
`coverage` — o que é diferente de devolver zero. A camada de leitura preserva
essa distinção, registrando `None` em vez de `0.0`, para que o dashboard não
apresente "0% de cobertura apurada" onde na verdade não houve apuração alguma.

### Formato

```json
{
  "repositorio": "IA",
  "projeto_sonar": "fga-eps-mds_2026.2-UNB-FCTE_UNIEURO_MED-IA",
  "coletado_em": "2026-09-21T03:00:00Z",
  "medidas": {
    "ncloc": "19",
    "bugs": "0",
    "code_smells": "0",
    "duplicated_lines_density": "0.0",
    "reliability_rating": "1.0",
    "security_rating": "1.0",
    "sqale_index": "0"
  },
  "historico": []
}
```

A função `get_sonar_metrics_data()` do `data_layer.py` converte esse arquivo na
estrutura consumida pelo dashboard, seguindo o mesmo contrato das demais fontes:
devolve uma tupla `(dados, is_mock)`.

## Sprints e Agile EVM

O script [`scripts/coleta_zenhub.py`](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-DOCS/blob/main/scripts/coleta_zenhub.py)
consulta a API GraphQL do Zenhub e grava, para cada sprint, os pontos entregues e
adicionados, o estado, as datas e a contagem de issues.

Diferente das outras duas fontes, esta **exige um token**, lido da variável de
ambiente `ZENHUB_TOKEN`. Ele precisa ser cadastrado como *secret* do repositório,
o que depende de acesso administrativo. Enquanto não estiver cadastrado, o script
avisa e encerra sem erro, preservando o arquivo anterior e deixando as demais
coletas seguirem.

Duas particularidades da API que motivaram decisões no script:

- O campo `scopeChange`, que dá os pontos adicionados e removidos ao longo da
  sprint, **não pode ser consultado para várias sprints de uma vez** — a API
  responde "Batched queries are disabled". Por isso ele é buscado sprint a sprint,
  após a consulta principal.
- Falhas nessa busca individual não interrompem a coleta: a sprint segue com os
  demais dados e os pontos adicionados ficam zerados.

### Estimativas ausentes

O arquivo registra, por sprint, quantas issues estão **sem estimativa** em pontos.
Essa contagem não é consumida pelo dashboard, mas é o dado que explica um
resultado que de outro modo pareceria erro de coleta: quando a maior parte das
issues não tem pontos, a velocity e os índices do Agile EVM ficam próximos de
zero mesmo com trabalho sendo entregue. O que falta, nesse caso, é estimativa —
não entrega.

## O que ainda falta

### Riscos

O arquivo `riscos_analytics.json` é um array de riscos, cada um com `id`,
`titulo`, `categoria`, `probabilidade`, `impacto`, `estrategia` e `acao`. Não é
gerado por API: é a transcrição do Plano de Riscos, que ainda não foi elaborado
(issue #26). Enquanto o plano não existir, não há o que transcrever.

## Histórico de versão

| Versão | Data | Descrição | Autor | Revisor |
|:------:|------|-----------|-------|---------|
| `1.0` | 20/09/2026 | Criação da página e automação da coleta de execuções de CI/CD | [Vitor Carvalho Pereira](https://github.com/vcpVitor) | |
