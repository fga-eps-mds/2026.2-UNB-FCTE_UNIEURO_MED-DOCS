# Guia de Contribuição

Este repositório concentra toda a documentação do projeto: atas de reunião, artefatos de planejamento, site do MkDocs e políticas de governança. As diretrizes abaixo se aplicam a qualquer alteração feita aqui.

Este guia trata de processo técnico. As expectativas de comportamento, respeito e inclusão estão no [Código de Conduta](CODE_OF_CONDUCT.md).

## Padrão de Branch

Como este é um repositório exclusivo de documentação, utilizamos um fluxo simplificado. Crie suas branches **sempre a partir da `main`** (não utilizamos `develop` aqui). Use o padrão:

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

- Todo PR deve estar vinculado a uma Issue. Use `Closes #numero` na descrição. O template de PR já traz esse campo.
- Solicite revisão de no mínimo 1 colega antes de fazer o merge.
- PRs de documentação também passam por revisão: verifique se o conteúdo está correto, sem erros de português e com a tabela de histórico de versões atualizada.
- PRs sem Issue vinculada não serão aceitos.

### Como revisar

- Não aprove um Pull Request sem ter lido e compreendido o que está sendo alterado. Aprovação é responsabilidade técnica, não formalidade.
- Mantenha o foco construtivo na revisão. Comente o conteúdo, aponte o problema concreto e, quando possível, sugira o caminho.
- Se não tiver contexto suficiente para avaliar a alteração, diga isso e peça a revisão de quem tem, em vez de aprovar por omissão.

### Revisão, testes e co-autoria

Estas práticas foram adotadas a partir da R3 em todos os repositórios do projeto (DOCS, APP e IA):

- **O revisor não participou da tarefa.** Quem trabalhou na issue não revisa o próprio PR. A revisão fica com integrantes que não participaram do desenvolvimento, para que o código seja lido por quem não o conhece.
- **Os revisores se alternam.** A cada PR, a revisão vai para quem ainda não revisou ou revisou menos, para distribuir as revisões entre toda a equipe em vez de concentrá-las em poucas pessoas.
- **Quem implementa escreve os testes.** Os testes do que foi implementado fazem parte do mesmo PR e são escritos por quem implementou, não por outra pessoa depois. O revisor confere se eles cobrem o que mudou.
- **Trabalho em dupla é registrado com co-autoria.** Quando duas ou mais pessoas trabalham juntas num commit, quem faz o commit acrescenta ao final da mensagem uma linha `Co-authored-by` para cada participante, com o nome e o e-mail usados no GitHub:

```
feat(cadastro): valida CPF no formulário do paciente

Co-authored-by: Nome do Colega <email-do-colega@exemplo.com>
```

O GitHub passa a mostrar o commit no histórico de todos os co-autores, o que deixa o pareamento visível.

## Issues e compromissos

- Cumpra os prazos acordados na sprint e comunique impedimentos assim que eles aparecerem, não no fim do prazo.
- Não feche uma Issue sem a entrega efetiva do que foi combinado nela. Se o escopo mudou, atualize a Issue antes de fechar, explicando o que saiu e por quê.
- Mantenha o quadro fiel ao trabalho real, movendo a Issue conforme ela avança.

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

## Histórico de Versões

| Versão | Descrição | Autor(es) | Data | Revisor(es) | Data de Revisão |
|---|---|---|---|---|---|
| 1.0 | Criação do Guia de Contribuição | [Artur Mendonça Arruda](https://github.com/ArtyMend07) | 03/09/2026 | [Lucas Mendonça Arruda](https://github.com/lucasarruda9) |  |
| 1.1 | Reescrita para contexto do repositório de documentação e adição de Conventional Commits | [Artur Mendonça Arruda](https://github.com/ArtyMend07) | 13/09/2026 | [Lucas Mendonça Arruda](https://github.com/lucasarruda9) |  |
| 1.2 | Recepção das regras de processo que estavam no Código de Conduta, com novas seções de como revisar e de Issues e compromissos | [Artur Mendonça Arruda](https://github.com/ArtyMend07) | 19/09/2026 | [Gabriel Lopes de Amorim](https://github.com/BrzGab) | 20/09/2026 |
| 1.3 | Inclusão das práticas de revisão, testes e co-autoria adotadas na R3 | [Daniel Ferreira Nunes](https://github.com/Mach1r0) | 15/11/2026 |  |  |

