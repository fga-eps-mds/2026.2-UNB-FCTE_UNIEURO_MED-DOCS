# Dashboard Analítico e Gerencial — `2026.2-UNB-FCTE_UNIEURO_MED`

Dashboard de apoio à tomada de decisão gerencial e técnica da disciplina de **Engenharia de Produto de Software (EPS / MDS)** — Universidade de Brasília (UnB - FGA).

---

## Objetivo e Escopo da Release Atual (DA-R1)

O painel consolida os indicadores gerenciais e de processo exigidos para a primeira entrega:

- **Agile EVM (Earned Value Management)**: BAC, PRP0, PA, PRPn, PPC, PC, RPC, APC, PV, EV, AC, SPI, CPI, SV, CV e EAC (Sulaiman et al., 2006).
- **Velocity**: Histórico por sprint e média de entrega de Story Points.
- **Matriz de Riscos**: Mapa de calor 5x5 (Probabilidade x Impacto) e planos de mitigação.
- **Processo e CI/CD**: Taxa de sucesso de pipelines e tempo médio de feedback.

---

## Tecnologias Utilizadas

- **Linguagem**: Python 3.10+
- **Interface**: [Streamlit](https://streamlit.io/)
- **Visualização de Dados**: [Plotly](https://plotly.com/python/)
- **Manipulação de Dados**: [Pandas](https://pandas.pydata.org/)

---

## Como Executar Localmente

### 1. Pré-requisitos
- Python 3.10 ou superior instalado.
- Gerenciador de pacotes `pip`.

### 2. Passo a Passo

```bash
# 1. Navegue até a pasta do dashboard
cd dashboard

# 2. Crie um ambiente virtual (recomendado)
python3 -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicie o servidor Streamlit
streamlit run dashboard.py
```

O dashboard estará disponível em: `http://localhost:8501`.

---

## Estrutura do Projeto

```text
dashboard/
├── dashboard.py                  # Ponto de entrada do Streamlit
├── requirements.txt              # Dependências do projeto
├── README.md                     # Documentação de execução e arquitetura
├── COMO_INTEGRAR_REPOSITORIOS.md # Guia de CI/CD para os 3 repositórios
├── historico_analises/           # Pareceres técnicos salvos localmente
└── src/
    ├── __init__.py
    ├── config.py                 # Configurações globais e paleta visual
    ├── theme.py                  # Componentes visuais e injeção de CSS
    ├── data_layer.py             # Leitura resiliente de JSONs
    ├── metrics.py                # Modelagem matemática de EVM e Riscos
    └── templates.py              # Utilitários de apresentação
```

---

## Origem dos Dados (`analytics/raw-data/`)

O dashboard lê os arquivos `.json` em `../analytics/raw-data/`:
- `zenhub_analytics.json`: Dados de velocity, issues e sprints.
- `riscos_analytics.json`: Planilha/matriz de riscos da equipe.
- `GitHub_API-Runs-*.json`: Histórico de execuções das GitHub Actions.

> Caso os arquivos ainda não tenham sido extraídos no ambiente local, o dashboard utiliza estruturas iniciais estruturadas para permitir a execução imediata.
