# Coleta de métricas

O dashboard analítico não consulta APIs durante a renderização: ele lê arquivos
`.json` previamente gerados em `analytics-raw-data/`. Quando um arquivo não
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
| `fga-eps-mds-<repositório>-<data>-vX.Y.Z.json` | Métricas de cada versão do produto | Pipeline de release de APP e IA | Em revisão — ver [Métricas por versão](#metricas-por-versao-do-produto) |
| `Sonar_API-Issues-*.json` | Q-Rapids, métricas m7 e m8 | API do SonarCloud | Automatizado — ver [Problemas do SonarCloud](#problemas-do-sonarcloud-e-branches-das-releases) |
| `GitHub_API-Releases-*.json` | Q-Rapids, branch medida por release | API do GitHub | Automatizado |
| `GitHub_API-Bugs-*.json` | Comparação de defeitos entre releases | API do GitHub | Automatizado |

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
Antes de publicar, o job incorpora o que tiver chegado à `main` enquanto ele rodava
(`git pull --rebase`), porque os pipelines de APP e IA também gravam nesta pasta.
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
histórica. A lista começa pelas 12 métricas definidas pelo professor no Discord da
disciplina em 14/09 — `files`, `functions`, `complexity`, `comment_lines_density`,
`duplicated_lines_density`, `coverage`, `ncloc`, `tests`, `test_errors`,
`test_failures`, `test_execution_time` e `security_rating` — e acrescenta as que
alimentam os indicadores de confiabilidade e manutenibilidade do dashboard: *bugs*,
vulnerabilidades, *code smells*, *security hotspots*, dívida técnica, as notas de
avaliação e o estado do *quality gate*.

Métricas que dependem de código ou de testes, como `functions` e `tests`, só
aparecem no arquivo depois que o repositório passa a tê-los: o SonarCloud não as
devolve enquanto não há o que medir.

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

## Métricas por versão do produto

O professor definiu, no Discord da disciplina em 14/09, um segundo requisito para o
SonarCloud, independente do dashboard:

- a chamada à API do SonarCloud é feita no pipeline **de cada repositório de
  código**, quando um PR é fechado;
- o `.json` gerado para cada versão do produto (releases *major* e *minor*) vai para
  a pasta `analytics-raw-data/` deste repositório;
- o nome segue o formato `fga-eps-mds-<repositório>-<MM-DD-YYYY-HH-MM-SS>-vX.Y.Z`;
- cada release *major* publica, como *asset* no GitHub, o código-fonte e os testes
  compactados, com a *tag* da release.

Por isso a pasta se chama `analytics-raw-data/` e reúne todos os arquivos de
métricas, os do dashboard e os de cada versão.

O pipeline que gera esses arquivos está em revisão em
[APP #26](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/pull/26) e
[IA #11](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-IA/pull/11). A cada PR
fechado com merge, ele gera a release, com a versão definida pelos rótulos `MAJOR
RELEASE`, `MINOR RELEASE` ou `NOT RELEASE` do PR, e anexa a ela o `.json` com as métricas.

Deste lado, a coleta diária copia para a pasta o `.json` de cada release de APP e IA
que ainda não estiver aqui. Com isso, nenhum dos repositórios precisa de *secret* de
escrita em outro.

## Problemas do SonarCloud e branches das releases

O `.json` de cada release traz as medidas por arquivo, mas não os problemas apontados
pelo SonarCloud, que as métricas m7 e m8 do
[Plano de Qualidade](../processo/plano_de_qualidade.md) precisam. O script
[`scripts/coleta_qualidade.py`](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-DOCS/blob/main/scripts/coleta_qualidade.py),
chamado pela coleta diária, grava três arquivos por repositório de código:

- `Sonar_API-Issues-<repositório>.json`: todos os problemas da `main` e da `develop`,
  abertos e resolvidos, com o arquivo, a regra, os impactos e as datas de criação e de
  fechamento. As datas permitem saber o que estava aberto no momento de cada release.
- `GitHub_API-Releases-<repositório>.json`: a *tag*, o commit e a branch de destino de
  cada release. O pipeline de release roda nos merges para a `main` e para a `develop`,
  e cada `.json` mede a branch de destino; os problemas são lidos da mesma branch.
- `GitHub_API-Bugs-<repositório>.json`: as issues com o rótulo `bug`, com as datas de
  abertura e de fechamento, para a comparação de defeitos entre as releases.

A release guarda só o commit de merge, e a branch vem do PR desse commit. O cálculo e os
resultados estão em [Qualidade do produto](qualidade-do-produto.md) e em
[Processo e comparação R1 × R2](processo-e-comparativo.md).

## Sprints e Agile EVM

O script [`scripts/coleta_zenhub.py`](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-DOCS/blob/main/scripts/coleta_zenhub.py)
consulta a API GraphQL do Zenhub e grava, para cada sprint, os pontos entregues e
adicionados, o estado, as datas e a contagem de issues. Por issue, grava também o
identificador, o número, a estimativa e a coluna em que ela está.

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

### Histórias em Aceitação PO

Uma história só é fechada depois do aceite do *Product Owner* e do cliente, e os
pontos entregues de uma sprint no Zenhub só contam as histórias fechadas. Enquanto o
aceite não acontece, a história fica aberta na coluna **Aceitação PO**, com o código
entregue. Por isso a coleta grava a **coluna** de cada issue, e o dashboard soma os
pontos das histórias que estão em Aceitação PO, separados dos pontos aceitos. A barra
lateral do dashboard escolhe se esses pontos entram nos pontos entregues.

Particularidades:

- A coluna é lida no momento da coleta. Quando o PO aceita uma história, ela fecha e
  passa a contar como aceita; se ele a devolve, ela sai da coluna.
- A API do Zenhub não pôde ser conferida com o token durante o desenvolvimento. Se ela
  recusar o campo da coluna, a coleta tenta as consultas anteriores (com número e id e,
  por fim, a original) e o painel avisa que a coluna não foi coletada, em vez de
  mostrar zero como se fosse medido.
- Nesse caso, o arquivo opcional `analytics-raw-data/aceitacao_po_manual.json`, no
  formato `{"issues": [7, 8]}`, com os números das issues em Aceitação PO, é usado
  como alternativa.

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
| `1.1` | 21/09/2026 | Coleta do SonarCloud e do Zenhub | [Vitor Carvalho Pereira](https://github.com/vcpVitor) | |
| `1.2` | 24/09/2026 | Pasta renomeada para `analytics-raw-data/`, métricas exigidas pelo professor e seção de métricas por versão do produto | [Vitor Carvalho Pereira](https://github.com/vcpVitor) | |
| `1.3` | 22/10/2026 | Coleta dos problemas do SonarCloud e das branches das releases, para o Q-Rapids | [Gabriel Lopes de Amorim](https://github.com/BrzGab) | |
| `1.4` | 24/10/2026 | Coleta da coluna de cada issue do Zenhub, para os pontos em Aceitação PO | [Cláudio Henrique dos Santos Carvalho](https://github.com/claudiohsc) | |
