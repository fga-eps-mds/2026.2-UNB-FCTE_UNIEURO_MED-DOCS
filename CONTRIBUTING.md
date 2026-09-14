# Guia de Contribuição

Este repositório concentra toda a documentação do projeto: atas de reunião, artefatos de planejamento, site do MkDocs e políticas de governança. As diretrizes abaixo se aplicam a qualquer alteração feita aqui.

## Padrão de Branch

Como este é um repositório exclusivo de documentação, utilizamos um fluxo simplificado (Trunk-Based). Crie suas branches **sempre a partir da `main`** (não utilizamos `develop` aqui). Use o padrão:

- `docs/nome-do-documento`
- `fix/nome-da-correcao`
- `chore/nome-da-tarefa`

Push direto na `main` não é permitido. Qualquer alteração, mesmo pequena, passa por Pull Request.

## Padrão de Commits

Este repositório adota o padrão [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/). O formato obrigatório é:

```
<tipo>(escopo opcional): descrição curta em português
```

Tipos mais usados neste repositório:

| Tipo | Quando usar |
|------|-------------|
| `docs` | Criação ou atualização de qualquer documento |
| `fix` | Correção de erro em documento já existente |
| `chore` | Configuração de pipeline, MkDocs, dependências |

Exemplos:

```
docs(visao): atualiza escopo do produto após reunião com o PO
fix(contributing): corrige tabela de histórico de versões
chore(mkdocs): adiciona nova página ao menu de navegação
```

## Pull Requests

- Todo PR deve estar vinculado a uma Issue. Use `Closes #numero` na descrição (no Template de PR tem).
- Solicite revisão de no mínimo 1 colega antes de fazer o merge.
- PRs de documentação também precisam de revisão, e verificação se o conteúdo está correto, sem erros de português e com a tabela de histórico de versões atualizada.
- PRs sem Issue vinculada não serão aceitos.

## Verificando o site localmente

Antes de abrir o PR com alterações no MkDocs, confirme que o site compila sem erros:

```bash
pip install -r requirements.txt
mkdocs build
```

Se quiser visualizar no navegador:

```bash
mkdocs serve
```

| Versão | Descrição | Autor(es) | Data | Revisor(es) | Data de Revisão |
|---|---|---|---|---|---|
| 1.0 | Criação do Guia de Contribuição | [Artur Mendonça Arruda](https://github.com/ArtyMend07) | 03/09/2026 | [Lucas Mendonça Arruda](https://github.com/lucasarruda9) |  |
| 1.1 | Reescrita para contexto do repositório de documentação e adição de Conventional Commits | [Artur Mendonça Arruda](https://github.com/ArtyMend07) | 13/09/2026 | [Lucas Mendonça Arruda](https://github.com/lucasarruda9) |  |

