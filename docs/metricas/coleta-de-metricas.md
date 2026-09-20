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
| `GitHub_API-Runs-*.json` | Fluxo de CI/CD | API do GitHub Actions | Automatizado |
| `zenhub_analytics.json` | Sprints e Agile EVM | API do Zenhub | Pendente — falta *secret* |
| `riscos_analytics.json` | Matriz de Riscos | Plano de Riscos | Pendente — depende da issue #26 |

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

## O que ainda falta

### Zenhub

O arquivo `zenhub_analytics.json` alimenta a velocidade das sprints e o Agile
EVM. A API do Zenhub exige um token pessoal, que precisa ser cadastrado como
*secret* do repositório — algo que depende de quem tem acesso administrativo à
organização.

A estrutura esperada pelo `data_layer.py` é um objeto com a chave
`sprints_velocity`, mapeando o nome de cada sprint para seus pontos entregues,
pontos adicionados, estado e datas de início e fim.

### Riscos

O arquivo `riscos_analytics.json` é um array de riscos, cada um com `id`,
`titulo`, `categoria`, `probabilidade`, `impacto`, `estrategia` e `acao`. Não é
gerado por API: é a transcrição do Plano de Riscos, que ainda não foi elaborado
(issue #26). Enquanto o plano não existir, não há o que transcrever.

## Histórico de versão

| Versão | Data | Descrição | Autor | Revisor |
|:------:|------|-----------|-------|---------|
| `1.0` | 20/09/2026 | Criação da página e automação da coleta de execuções de CI/CD | [Vitor Carvalho Pereira](https://github.com/vcpVitor) | |
