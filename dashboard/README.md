# Dashboard Analítico e Gerencial — `2026.2-UNB-FCTE_UNIEURO_MED`

Dashboard de apoio à tomada de decisão gerencial e técnica da disciplina de **Engenharia de Produto de Software (EPS / MDS)** — Universidade de Brasília (UnB - FGA).

---

## Objetivo e Escopo da Release Atual (DA-R1)

O painel consolida os indicadores gerenciais e de processo exigidos para a primeira entrega:

- **Agile EVM (Earned Value Management) por release**: BAC, PRP, RPC, PPC, APC, PV, EV, AC, SPI, CPI, SV, CV e EAC (Sulaiman et al., 2006), calculados para cada release já iniciada (R1, R2, R3 e release final aparecem a partir da data de início). Não há parâmetros de simulação: o painel reflete os dados reais.
- **Velocity**: histórico de pontos entregues por sprint fechada.
- **Burnup e Burndown de pontos**: progresso da release selecionada contra o escopo planejado (PRP) e contra o ritmo ideal.
- **Matriz de Riscos**: Mapa de calor 5x5 (Probabilidade x Impacto) e planos de mitigação.
- **Processo e CI/CD**: Taxa de sucesso de pipelines e tempo mediano de execução (a mediana evita que execuções atípicas distorçam o indicador).
- **Qualidade de Produto**: Métricas do SonarCloud (cobertura, bugs, vulnerabilidades, code smells, security hotspots, ratings) por repositório de código (APP/IA).

---

## Agile EVM por release: fórmulas, unidades e hipóteses

Origem: Sulaiman, Barton e Blackburn (2006), *AgileEVM - Earned Value Management in Scrum Projects*. Cálculo em `src/metrics.py` (`compute_release_evm`).

| Indicador | Fórmula | Unidade |
|---|---|---|
| BAC | orçamento da release (`RELEASES` em `src/config.py`) | R$ |
| PRP | soma dos pontos (`total_points`) das sprints que terminam na release | pontos de história |
| RPC | soma dos pontos entregues (`delivered_sp`) nessas sprints | pontos de história |
| PPC | dias decorridos da release ÷ dias da release | 0 a 1 |
| APC | RPC ÷ PRP | 0 a 1 |
| PV | PPC × BAC | R$ |
| EV | APC × BAC | R$ |
| AC | PPC × BAC (estimado) | R$ |
| SPI e CPI | EV ÷ PV e EV ÷ AC | índice |
| SV e CV | EV − PV e EV − AC | R$ |
| ETC e EAC | (BAC − EV) ÷ CPI e AC + ETC | R$ |

Hipóteses e limites:

- **BAC provisório:** os valores de `RELEASES` vêm da seção 5 do Plano de Custos v1.3 e serão atualizados quando o plano for revisado. É o único lugar a alterar.
- **Sprint e release:** cada sprint é atribuída à release em que termina (data de término em horário de Brasília). Sprints depois da release final ficam de fora.
- **PRP depende da estimativa:** só é confiável se todas as histórias estiverem estimadas no ZenHub. Se o ZenHub pontuar tarefas em vez de histórias, o PRP sai inflado. O painel não conta issues sem estimativa, porque nem toda issue é uma história de usuário.
- **Possível dupla contagem:** issues que passam de uma sprint para a seguinte podem ser contadas nas duas.
- **AC estimado:** não há custo real apurado. Por isso o CPI coincide com o SPI até que o custo real seja registrado.

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

## Origem dos Dados (`analytics-raw-data/`)

O dashboard lê os arquivos `.json` em `../analytics-raw-data/`:
- `zenhub_analytics.json`: Dados de sprints (pontos planejados e entregues por sprint).
- `riscos_analytics.json`: Planilha/matriz de riscos da equipe.
- `GitHub_API-Runs-*.json`: Histórico de execuções das GitHub Actions.
- `Sonar_API-Measures-*.json`: Métricas de qualidade de produto do SonarCloud (APP/IA).

> Caso os arquivos ainda não tenham sido extraídos no ambiente local, o dashboard utiliza estruturas iniciais estruturadas para permitir a execução imediata.
