# 2026.2-UNB-FCTE_UNIEURO_MED-DOCS

Documentação da equipe de **Engenharia de Produto de Software (EPS)** do semestre 2026.2 no projeto **MED**, desenvolvido em parceria com a **UNIEURO**.

O site é publicado via GitHub Pages em:
https://fga-eps-mds.github.io/2026.2-UNB-FCTE_UNIEURO_MED-DOCS/

> A documentação **do produto** fica em repositório próprio, quando aplicável.

## Dashboard Analítico

O painel gerencial e analítico da equipe (Agile EVM, Riscos, Processo/CI-CD e Qualidade de Produto) está publicado em:
https://2026-2-unb-fcte-unieuro-med-docs.streamlit.app

Consome os `.json` versionados em [`analytics-raw-data/`](analytics-raw-data/), atualizados diariamente pela esteira de CI/CD (veja [`dashboard/README.md`](dashboard/README.md) para rodar localmente).

## Estrutura

```
docs/
  index.md                Página inicial da documentação
  produto/                Visão do produto, arquitetura, repositórios
  planejamento/           Metodologia, roadmap, riscos
  sprints/                Registro de cada sprint
  metricas/               Métricas de processo e de produto
  equipe/                 Integrantes, políticas de trabalho, links e acessos
  stylesheets/            CSS customizado (paleta, home estilizada)
mkdocs.yml                Configuração do site (nav, tema, plugins)
requirements.txt     Dependências Python para build da documentação
```

## Rodando localmente

Requer Python 3.10 ou superior.

```bash
python3 -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

pip install -r requirements.txt
mkdocs serve
```

O site fica disponível em http://127.0.0.1:8000.

## Build

```bash
mkdocs build    
```

## Publicação

Todo push na branch `main` dispara o workflow
[`deploy-docs.yml`](.github/workflows/deploy-docs.yml), que faz o build e publica no
GitHub Pages. Não é necessário rodar deploy manualmente.

## Como contribuir

1. Crie uma branch a partir de `main` (`docs/<assunto>`).
2. Edite os arquivos `.md` em `docs/`.
3. Rode `mkdocs serve` para conferir localmente e garantir que não há links quebrados.
4. Abra um Pull Request.


## Licença

MIT License - veja [LICENSE](LICENSE).