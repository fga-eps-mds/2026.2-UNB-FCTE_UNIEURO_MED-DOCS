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
- **Q-Rapids e R1 × R2 (DA-R2)**: índice de qualidade do produto (Q) com métricas, fatores e características por release, indicadores de processo (P1 a P3 e P) e a comparação de velocidade, cobertura e defeitos entre as releases.

---

## Agile EVM por release: fórmulas, unidades e hipóteses

Origem: Sulaiman, Barton e Blackburn (2006), *AgileEVM - Earned Value Management in Scrum Projects*. Cálculo em `src/metrics.py` (`compute_release_evm`).

| Indicador | Fórmula | Unidade |
|---|---|---|
| BAC | orçamento da release (`RELEASES` em `src/config.py`) | R$ |
| PRP | pontos das histórias distintas das sprints que terminam na release | pontos de história |
| RPC | pontos entregues nessas sprints: os aceitos (`delivered_sp`) e, conforme o modo, os que estão em Aceitação PO | pontos de história |
| PPC | dias decorridos da release ÷ dias da release | 0 a 1 |
| APC | RPC ÷ PRP | 0 a 1 |
| PV | PPC × BAC | R$ |
| EV | APC × BAC | R$ |
| AC | PPC × BAC (estimado) | R$ |
| SPI e CPI | EV ÷ PV e EV ÷ AC | índice |
| SV e CV | EV − PV e EV − AC | R$ |
| ETC e EAC | (BAC − EV) ÷ CPI e AC + ETC | R$ |

Hipóteses e limites:

- **BAC por release:** os valores de `RELEASES` vêm da seção 5 do Plano de Custos v2.0 (R$ 62.746,77, R$ 12.595,73, R$ 15.744,66 e R$ 3.148,93, somando R$ 94.236,09). Devem ser atualizados junto com o plano, e este é o único lugar a alterar.
- **Sprint e release:** cada sprint é atribuída à release em que termina (data de término em horário de Brasília). Sprints depois da release final ficam de fora.
- **PRP depende da estimativa:** só é confiável se todas as histórias estiverem estimadas no ZenHub. Se o ZenHub pontuar tarefas em vez de histórias, o PRP sai inflado. O painel não conta issues sem estimativa, porque nem toda issue é uma história de usuário.
- **Histórias contadas uma vez:** uma história que passa de uma sprint para a seguinte aparece nas duas no ZenHub. O PRP conta cada uma só uma vez, com a estimativa da última sprint em que aparece. Para isso a coleta (`scripts/coleta_zenhub.py`) guarda, por sprint, o id, o número e a estimativa de cada issue (`issues` em `zenhub_analytics.json`). Se o ZenHub recusar esses campos ou o detalhe estiver incompleto, o painel soma o `total_points` das sprints e avisa que o PRP é aproximado.
- **Aceite do PO:** uma história só é fechada depois do aceite do PO (Ata 08), e o ZenHub só conta como entregue a história fechada. No modo "somente aceitas", enquanto o PO não aceita, o RPC, o EV, o SPI e o CPI ficam em zero, o que indica espera de aceite e não necessariamente atraso do time. Veja a seção seguinte.
- **AC estimado:** não há custo real apurado. Por isso o CPI coincide com o SPI até que o custo real seja registrado.

---

## Pontos entregues: aceitos e em Aceitação PO

A equipe decidiu medir também o que já foi entregue e aguarda o aceite: o código está pronto, o APK segue para o PO e para o cliente, e a história fica aberta na coluna **Aceitação PO** do ZenHub até o aceite. O painel guarda as duas partes e a barra lateral ("Pontos entregues") escolhe o que conta:

| Modo | O que entra nos pontos entregues |
|---|---|
| Somente histórias aceitas (fechadas) | só os pontos das histórias fechadas (`delivered_story_points` do ZenHub) |
| Aceitas + em Aceitação PO (padrão) | os aceitos e os pontos das histórias da coluna Aceitação PO |

A escolha vale para tudo que envolve pontos entregues: RPC, APC, EV, SPI e CPI do EVM, o burnup e o burndown, a velocity e, na aba Q-Rapids, o P2 (entrega do comprometido) e a velocidade da comparação entre releases. O PRP, o P3 e o BAC não mudam. Os dois valores aparecem sempre separados nos cartões e na tabela de auditoria (`RPC aceito`, `Em aceitação` e `RPC considerado`), e a lista das histórias em aceitação fica na aba de EVM.

Regras e hipóteses:

- **Origem.** `scripts/coleta_zenhub.py` grava, para cada issue de cada sprint, o id, o número, a estimativa e a coluna atual (`coluna`). A coluna é lida de duas formas: perguntando a cada issue onde ela está e, se o ZenHub recusar, perguntando ao workspace quais issues cada coluna guarda e juntando pelo id. O JSON traz `colunas_coletadas` e `colunas_fonte` (`issue` ou `workspace`), e é por esse sinal que o painel distingue "Aceitação PO vazia" de "coluna nunca coletada". A regra de quais colunas contam está em `COLUNAS_ACEITACAO` (`src/config.py`), e a leitura em `src/aceitacao.py`. A comparação ignora acento, caixa e espaços.
- **Contada uma vez.** Uma história que passa de uma sprint para a seguinte aparece nas duas, e conta na última sprint em que aparece, com a estimativa de lá. História sem estimativa vale 0 ponto.
- **Retrato do momento.** A coluna é lida na hora da coleta. Quando o PO aceita, a história fecha e passa a contar como aceita; se ele a devolve, ela sai dos pontos entregues. Por isso o valor do modo "entregues" pode cair.
- **Sem a coluna coletada.** Se o ZenHub recusar as duas formas, a coleta volta às consultas anteriores, imprime no log os campos que a API realmente tem (`Esquema: campos de Issue: ...`) e o painel avisa que a coluna não foi coletada: os dois modos mostram o mesmo valor, sem inventar dado. Como alternativa, o arquivo `analytics-raw-data/aceitacao_po_manual.json`, no formato `{"issues": [7, 8]}`, com os números das issues que estão na coluna, é usado somente nessa situação. Ele precisa ser mantido à mão e não deve listar histórias já fechadas, que contariam duas vezes.
- **Leitura.** O modo "entregues" mostra trabalho entregue, mas ainda não validado. Ao apresentar um número, cite o modo.

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
    ├── aceitacao.py              # Histórias em Aceitação PO e os pontos entregues por modo
    ├── qualidade.py              # Q-Rapids: métricas m1 a m8, fatores, características e índice Q
    ├── processo.py               # Indicadores de processo e comparação R1 × R2
    └── templates.py              # Utilitários de apresentação, incluindo as tabelas da aba Q-Rapids
└── tests/
    ├── test_qualidade.py         # Testes das fórmulas do Plano de Qualidade
    ├── test_processo.py          # Testes dos indicadores de processo
    ├── test_aceitacao.py         # Testes das histórias em Aceitação PO
    ├── test_aceitacao_dados.py   # Testes da leitura dos dados e do processo nos dois modos
    ├── test_metrics_modo.py      # Testes do EVM nos dois modos de pontos entregues
    ├── test_data_layer_qrapids.py  # Testes da leitura resiliente dos dados da aba Q-Rapids
    └── test_templates_qrapids.py   # Testes das tabelas e dos formatos da aba Q-Rapids
```

Os módulos `qualidade.py` e `processo.py` não dependem do Streamlit:

- `qualidade.avaliar_repositorio("APP")` devolve, para cada versão, as métricas com os
  arquivos fora do limiar e a agregação, e `qualidade.por_marco()` escolhe a versão de
  cada release;
- `processo.indicadores_por_release()` devolve os indicadores de processo P1 a P3 e o
  índice P de cada release, e `processo.comparativo()` devolve a velocidade, a
  cobertura e os defeitos de cada release, a comparação R1 × R2 que o cronograma pede
  para o DA-R2.

### Aba "Q-Rapids e R1 × R2"

A aba tem três seções: **Qualidade do Produto**, **Processo** e **Comparação entre Releases**. O fluxo respeita a separação entre camadas:

1. `data_layer.get_qrapids_data()` lê `analytics-raw-data/` e chama `qualidade.py` e `processo.py`. Cada cálculo é protegido: se um `.json` estiver malformado, só aquela parte volta vazia e o restante da aba continua.
2. `templates.py` monta as tabelas, formata os índices e escolhe a cor pela faixa do Plano de Qualidade.
3. `dashboard.py` (`render_qrapids_tab`) só apresenta.

Decisões de leitura:

- **Sem dados de exemplo.** Diferente das outras abas, esta não usa dado simulado, porque um índice inventado seria lido como resultado real. Sem os arquivos, a aba avisa que ainda não há coleta.
- **Não medido não é zero.** Métrica sem dado aparece como `n/m`, e o gráfico por versão interrompe a linha em vez de cair a zero. Valor parcial leva um asterisco.
- **Marcos sem versão.** Se um repositório não tem versão nova medida para uma release que já passou ou está em curso (hoje, a IA na RM1 e na R2), a aba avisa quais marcos ficaram sem medição.
- **Causa de cada nota.** A seção "De onde vem cada nota" lista os arquivos fora do limiar de cada métrica, para a análise de causa que o plano pede.
- **Validação pendente.** Os limiares, os pesos e os indicadores de processo são proposta do time e aguardam o professor. Para mudar um limiar, altere a constante em `qualidade.py` e a aba acompanha.

Para conferir os valores e rodar os testes, a partir desta pasta:

```bash
python3 -m src.qualidade
python3 -m src.processo
python3 -m unittest discover tests
```

---

## Origem dos Dados (`analytics-raw-data/`)

O dashboard lê os arquivos `.json` em `../analytics-raw-data/`:
- `zenhub_analytics.json`: Dados de sprints (pontos planejados e entregues por sprint, e por issue o id, o número, a estimativa e a coluna).
- `aceitacao_po_manual.json` (opcional): números das issues em Aceitação PO, usado só quando a coleta não trouxe a coluna.
- `riscos_analytics.json`: Planilha/matriz de riscos da equipe.
- `GitHub_API-Runs-*.json`: Histórico de execuções das GitHub Actions.
- `Sonar_API-Measures-*.json`: Métricas de qualidade de produto do SonarCloud (APP/IA).

> Caso os arquivos ainda não tenham sido extraídos no ambiente local, o dashboard utiliza estruturas iniciais estruturadas para permitir a execução imediata.
