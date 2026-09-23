# AGENTS.md

## Escopo

Estas instruções se aplicam a todo o repositório `2026.2-UNB-FCTE_UNIEURO_MED-DOCS`.

Este repositório concentra a documentação do projeto MED, o site MkDocs e o dashboard gerencial. Antes de alterar qualquer arquivo, consulte também:

- `CONTRIBUTING.md`, para fluxo de branches, commits e Pull Requests;
- `mkdocs.yml`, para navegação e configuração do site;
- `README.md`, para execução local;
- `dashboard/README.md`, quando a tarefa envolver o dashboard.

Em caso de conflito, as instruções mais específicas do arquivo ou diretório alterado prevalecem.

## Contexto do ecossistema

O projeto está dividido em três repositórios irmãos:

| Repositório | Responsabilidade | Branch de integração |
|---|---|---|
| `2026.2-UNB-FCTE_UNIEURO_MED-DOCS` | Documentação, governança, MkDocs e dashboard | `main` |
| `2026.2-UNB-FCTE_UNIEURO_MED-APP` | Aplicativo Android utilizado no tablet | `develop` |
| `2026.2-UNB-FCTE_UNIEURO_MED-IA` | Treino, avaliação e exportação do modelo de IA | `develop` |

Não altere os repositórios irmãos quando a solicitação estiver limitada ao `MED-DOCS`. Consulte-os apenas para manter consistência técnica ou quando o usuário os incluir explicitamente no escopo.

O aplicativo e o modelo devem funcionar **100% offline**. A documentação não pode propor serviços remotos, telemetria ou envio de dados clínicos sem uma decisão formal do projeto.

## Estrutura principal

- `docs/`: páginas publicadas no MkDocs.
- `docs/produto/`: visão, identidade e artefatos do produto.
- `docs/processo/`: roadmap, cronograma e processo de desenvolvimento.
- `docs/atas-reunioes/`: atas e índice das reuniões.
- `docs/equipe/`: informações da equipe.
- `docs/stylesheets/`: customizações visuais do site.
- `docs/assets/`: imagens e demais arquivos usados pelas páginas.
- `dashboard/`: aplicação Streamlit e seus módulos.
- `mkdocs.yml`: navegação, tema e extensões do site.

## Regras para documentação

- Escreva em português brasileiro, com linguagem objetiva e termos consistentes com os documentos existentes.
- Preserve alterações do usuário e evite reformatações sem relação com a tarefa.
- Ao adicionar uma página publicada, inclua-a na seção correta de `nav` em `mkdocs.yml`.
- Use links relativos para arquivos internos e confirme que o destino existe.
- Armazene imagens em `docs/assets/imagens/<assunto>/`, com nomes descritivos em minúsculas e separados por hífen.
- Adicione texto alternativo útil a imagens e título descritivo a `iframe`, quando seu uso for adequado.
- Não incorpore por `iframe` conteúdo protegido por senha; forneça somente o link de acesso.
- Nunca versione senhas, tokens, chaves, dados pessoais ou dados clínicos. Não copie credenciais recebidas na conversa para arquivos do projeto.
- Atualize o histórico de versões do documento quando o padrão já existir na página.
- Não edite diretamente o diretório gerado `site/`.

## Regras para o dashboard

- Mantenha `dashboard/dashboard.py` como ponto de entrada do Streamlit.
- Separe configuração, acesso a dados, cálculos e apresentação nos módulos existentes em `dashboard/src/`.
- Não misture dados reais de pacientes com dados gerenciais do projeto.
- Preserve o comportamento resiliente quando os arquivos analíticos ainda não estiverem disponíveis.
- Ao alterar fórmulas ou indicadores, documente a origem, as unidades e as hipóteses utilizadas.

## Validação

Para alterações no site, execute a partir da raiz:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mkdocs build
```

Para visualizar o site durante a edição:

```bash
mkdocs serve
```

Para alterações no dashboard:

```bash
python3 -m venv dashboard/venv
source dashboard/venv/bin/activate
pip install -r dashboard/requirements.txt
streamlit run dashboard/dashboard.py
```

Execute somente as validações relevantes para os arquivos alterados. Se uma dependência não estiver disponível, registre claramente no resultado o que não pôde ser validado.

## Git e Pull Requests

- Neste repositório, crie branches a partir de `main`; não use `develop`.
- Use os prefixos `docs/`, `fix/` ou `chore/`, conforme `CONTRIBUTING.md`.
- Siga Conventional Commits, com descrição curta em português, por exemplo: `docs(arquitetura): adiciona diagrama de contêineres`.
- Não faça push direto em `main`.
- Todo Pull Request deve apontar para `main`, estar vinculado a uma Issue e receber pelo menos uma revisão.
- No `MED-APP` e no `MED-IA`, branches de trabalho partem de `develop` e Pull Requests apontam para `develop`.
- Antes de concluir, revise `git diff`, confirme que não há credenciais e liste as validações executadas.

## Restrições entre aplicativo e IA

Quando um documento descrever integração entre os repositórios, preserve estas invariantes:

- nenhum dado de atendimento, imagem, traçado ou escore sai do dispositivo;
- o paciente não recebe o escore na tela final;
- o modelo precisa ter caminho viável de exportação e execução embarcada;
- resultados de experimentos devem registrar versão dos dados, parâmetros e métricas;
- dados brutos de pacientes e identificações nunca são versionados.
