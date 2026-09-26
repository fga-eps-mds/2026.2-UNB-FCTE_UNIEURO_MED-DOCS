# Plano de Gerenciamento de Custos

## 1. Objetivo

Este plano estabelece como os custos do projeto MED serão estimados, consolidados,
monitorados e revisados durante o semestre 2026.2. A linha de base representa o
**custo econômico estimado** do projeto acadêmico: ela inclui o investimento público
na formação dos estudantes e o uso proporcional de recursos já disponíveis, mesmo
quando não há desembolso direto da equipe.

O documento apoia o acompanhamento por EVM-Ágil e deve permanecer alinhado ao
[cronograma](../processo/cronograma.md), ao
[roadmap](../processo/roadmap.md), ao [Canvas MVP](../produto/canvas-mvp.md) e aos
dados apresentados no Dashboard Gerencial e Analítico.

!!! note "Natureza da estimativa"
    Os valores não constituem prestação de contas da UnB, da UNIEURO ou do cliente.
    São uma estimativa acadêmica para planejamento e controle do projeto.

## 2. Premissas da linha de base

| Premissa | Valor adotado |
|---|---:|
| Período do projeto | 17 semanas |
| Equipe de EPS | 11 integrantes |
| Créditos anuais de referência | 40 créditos |
| Créditos da disciplina | 4 créditos |
| Dotação atualizada da UnB em 2026 | R$ 2.700.943.579,00 |
| Estudantes regulares de graduação | 39.190 |
| Estudantes regulares de mestrado | 6.805 |
| Estudantes regulares de doutorado | 4.848 |
| Total oficial de estudantes utilizado | 50.843 |
| Orçamento anual aproximado por estudante | R$ 53.123,21 |
| Orçamento proporcional da disciplina por estudante | R$ 5.312,32 |
| Orçamento semanal médio por estudante | R$ 312,49 |
| Computadores de uso geral | 11 unidades já disponíveis |
| Vida útil contábil dos computadores | 5 anos (depreciação de 20% ao ano) |
| Uso extraclasse considerado | 14 horas por semana e por integrante |
| Tablet Android | Disponibilizado pelo parceiro; desembolso previsto de R$ 0,00 |
| Servidor, hospedagem e licenças | R$ 0,00, pois o produto opera offline e utiliza planos educacionais/gratuitos |

A adoção do custo do estudante UnB como referência de mão de obra foi registrada na
[Ata 04, de 11/09/2026](../atas-reunioes/Ata-04-EPS-2026-09-11-PO.md#orientacoes-do-professor-sobre-o-canvas-mvp).
A decisão de manter o produto offline, sem servidor, licença ou hospedagem, está
registrada no [Canvas MVP](../produto/canvas-mvp.md#7-custo-e-cronograma).

A dotação atualizada foi consultada no
[Painel Gestão UnB](https://app.powerbi.com/view?r=eyJrIjoiZWNjNzkzZWQtNTJkMi00YmZhLThkOTgtNzgzNmE2MWMzZjdmIiwidCI6ImVjMzU5YmExLTYzMGItNGQyYi1iODMzLWM4ZTZkNDhmODA1OSJ9),
com fechamento contábil em 20/09/2026. A quantidade de estudantes utiliza o total
oficial mais recente disponível na tabela 2.18 do
[Anuário Estatístico 2025 da UnB](https://repositoriodpo.unb.br/anuarios/anuario-estatistico-2025/):
50.843 alunos regulares no segundo semestre de 2024, sendo 39.190 da graduação,
6.805 do mestrado e 4.848 do doutorado. A tabela apresenta separadamente 232
residentes médicos, mas não os incorpora ao total geral. Os 5.252 estudantes de
especialização também não integram esse total consolidado.

!!! warning "Orçamento por estudante, não custo contábil individual"
    O valor de R$ 53.123,21 é obtido pela divisão da dotação atualizada da
    Universidade pelo total oficial de 50.843 estudantes. Ele deve ser interpretado
    como **orçamento médio aproximado por estudante**, pois o orçamento total
    também financia pós-graduação, pesquisa, extensão, pessoal, aposentadorias,
    infraestrutura, hospitais e outros serviços da UnB.

Para uma análise restrita à graduação, a divisão pelos 39.190 graduandos produziria
R$ 68.919,20 por ano. Este plano utiliza os **50.843 estudantes** porque esse é o
“Total Geral” consolidado pela própria UnB na tabela 2.18.

## 3. Método de estimativa

### 3.1 Pessoas

O valor do trabalho não utiliza salário de mercado. Seguindo a orientação acadêmica,
adota-se como aproximação o orçamento médio da UnB por estudante alocado à
disciplina:

**Orçamento por estudante/ano:**
`R$ 2.700.943.579,00 ÷ 50.843 = R$ 53.123,21`.

**Orçamento proporcional da disciplina por estudante:**
`R$ 53.123,21 ÷ 40 créditos × 4 créditos = R$ 5.312,32`.

Para 11 integrantes, o custo estimado de pessoas durante o semestre é:

**Custo econômico de pessoas:**
`11 × (R$ 2.700.943.579,00 ÷ 50.843 ÷ 40 × 4) = R$ 58.435,54`.

Os totais usam os valores não arredondados; os valores unitários exibidos são
arredondados para duas casas decimais.

O valor semanal médio de pessoas é de **R$ 3.437,38**.

### 3.2 Computadores

Cada integrante utiliza um computador de uso geral já disponível. Para tornar o uso
do equipamento visível no custo econômico do projeto, considera-se um equipamento de
referência de R$ 3.500,00, com vida útil de cinco anos. A depreciação estimada é de
R$ 13,61 por equipamento por semana.

**Custo dos computadores:** `11 × R$ 13,61 × 17 = R$ 2.545,07`.

Não foi incluída uma estação dedicada de IA. Caso a equipe contrate GPU em nuvem ou
adquira equipamento específico, o valor deverá entrar pelo processo de mudança deste
plano.

### 3.3 Energia elétrica

Considera-se consumo médio de 0,56 kWh por computador a cada semana de trabalho
extraclasse e custo semanal aproximado de R$ 0,46 por integrante:

**Custo de energia:** `11 × R$ 0,46 × 17 = R$ 86,02`.

### 3.4 Internet

Para um plano residencial de referência de R$ 100,00 mensais, rateado pelas horas de
uso, estima-se R$ 1,94 por integrante por semana:

**Custo de internet:** `11 × R$ 1,94 × 17 = R$ 362,78`.

### 3.5 Produto e serviços

| Recurso | Estratégia | Custo direto previsto |
|---|---|---:|
| Tablet Android e caneta | Equipamento fornecido pelo parceiro | R$ 0,00 |
| GitHub e GitHub Actions | Repositórios públicos/plano acadêmico | R$ 0,00 |
| GitHub Pages | Hospedagem da documentação | R$ 0,00 |
| ZenHub | Plano educacional | R$ 0,00 |
| Figma | Plano educacional | R$ 0,00 |
| SonarCloud | Análise dos repositórios públicos | R$ 0,00 |
| Streamlit | Hospedagem no plano gratuito ou execução local | R$ 0,00 |
| Servidor de aplicação | Não necessário; aplicação 100% offline | R$ 0,00 |
| Licenças de software | Tecnologias abertas ou planos acadêmicos | R$ 0,00 |

O custo zero indica ausência de desembolso previsto, não ausência de risco. Mudanças
de franquia, indisponibilidade de planos gratuitos ou necessidade de infraestrutura
adicional devem ser registradas como solicitação de mudança.

## 4. Linha de base de custos

A memória de cálculo também está disponível em formato aberto na
[planilha CSV versionada](../assets/dados/plano_de_custos.csv), que pode ser importada
no LibreOffice Calc, Microsoft Excel ou Google Planilhas.

| Categoria | Custo semanal médio | Quantidade de semanas | Custo total |
|---|---:|---:|---:|
| Pessoas | R$ 3.437,38 | 17 | R$ 58.435,54 |
| Depreciação dos computadores | R$ 149,71 | 17 | R$ 2.545,07 |
| Energia elétrica | R$ 5,06 | 17 | R$ 86,02 |
| Internet | R$ 21,34 | 17 | R$ 362,78 |
| Serviços, licenças e hospedagem | R$ 0,00 | 17 | R$ 0,00 |
| **Linha de base (BAC)** | **R$ 3.613,49** | **17** | **R$ 61.429,41** |

Foi definida uma **reserva gerencial de 5%**, separada da linha de base, para eventos
não previstos que sejam formalmente aprovados:

| Componente orçamentário | Valor |
|---|---:|
| Linha de base de custos (BAC) | R$ 61.429,41 |
| Reserva gerencial (5%) | R$ 3.071,47 |
| **Orçamento total autorizado** | **R$ 64.500,88** |

A reserva não integra o BAC enquanto não houver mudança aprovada. Assim, os índices
de EVM são calculados inicialmente sobre **R$ 61.429,41**.

## 5. Distribuição planejada por release

A distribuição temporal segue os marcos do cronograma. Os valores correspondem ao
custo semanal médio multiplicado pelas semanas de cada período.

| Período | Semanas consideradas | Custo planejado | Acumulado planejado |
|---|---:|---:|---:|
| R1 — 10/08 a 28/09 | 7 | R$ 25.294,46 | R$ 25.294,46 |
| R2 — 29/09 a 26/10 | 4 | R$ 14.453,98 | R$ 39.748,44 |
| R3 — 27/10 a 30/11 | 5 | R$ 18.067,47 | R$ 57.815,91 |
| Release final — 01/12 a 07/12 | 1 | R$ 3.613,50 | R$ 61.429,41 |
| **Total** | **17** | **R$ 61.429,41** | **R$ 61.429,41** |

O centavo residual do último período compensa o arredondamento dos valores semanais.

## 6. Monitoramento por EVM-Ágil

O acompanhamento combina custo, tempo e escopo. A unidade de progresso é composta
por pontos de história concluídos e aceitos na sprint, evitando contabilizar trabalho
iniciado como valor entregue.

| Sigla | Indicador | Cálculo/uso |
|---|---|---|
| BAC | Orçamento no término | Linha de base aprovada: R$ 61.429,41 |
| PV | Valor planejado | BAC × percentual de escopo planejado até a data |
| EV | Valor agregado | BAC × percentual de pontos aceitos até a data |
| AC | Custo real | Custo das semanas decorridas, ajustado por mudanças reais |
| SV | Variação de prazo | EV − PV |
| CV | Variação de custo | EV − AC |
| SPI | Índice de desempenho de prazo | EV ÷ PV |
| CPI | Índice de desempenho de custo | EV ÷ AC |
| EAC | Estimativa no término | BAC ÷ CPI, quando CPI > 0 |

### Limites para tomada de decisão

| Estado | CPI/SPI | Ação esperada |
|---|---:|---|
| Adequado | ≥ 0,90 | Manter o plano e acompanhar semanalmente |
| Atenção | 0,80 a 0,89 | Investigar causa e registrar ação corretiva |
| Crítico | < 0,80 | Replanejar escopo, capacidade ou prazo e submeter mudança |

Os valores de PV, EV, AC, CPI, SPI e EAC devem ser atualizados ao término de cada
sprint e consumidos pelo Dashboard Gerencial. O custo semanal configurado no
dashboard deve permanecer sincronizado com esta linha de base.

## 7. Controle e aprovação de mudanças

Uma revisão da linha de base é necessária quando ocorrer pelo menos uma das situações:

- entrada ou saída de integrante;
- alteração do número de semanas do projeto;
- aquisição ou aluguel de tablet, computador ou GPU;
- contratação de infraestrutura, licença ou serviço pago;
- variação acumulada superior a 5% da linha de base;
- mudança de escopo que altere materialmente a capacidade planejada.

O processo de controle é:

1. registrar a necessidade e sua causa em uma issue;
2. calcular o impacto no BAC, na reserva e nas releases;
3. discutir a mudança com a equipe e responsáveis pelo projeto;
4. aprovar ou rejeitar a mudança com evidência rastreável;
5. atualizar este documento, os dados do EVM e o dashboard;
6. registrar a alteração no histórico de versões.

### Registro de ajustes estruturais

| Data | Mudança | Impacto | Novo BAC | Evidência | Responsável |
|---|---|---:|---:|---|---|
| 21/09/2026 | Criação da linha de base inicial | — | R$ 61.284,29 | Versão 1.0 deste documento | Daniel Ferreira Nunes |
| 22/09/2026 | Atualização da fonte de pessoas para o orçamento da UnB em 2026 | + R$ 17.520,70 | R$ 78.804,99 | Painel Gestão UnB e Anuário Estatístico 2025 | Daniel Ferreira Nunes |
| 22/09/2026 | Adoção do total oficial de 50.843 estudantes como denominador | - R$ 17.375,58 | R$ 61.429,41 | Tabela 2.18 do Anuário Estatístico 2025 | Daniel Ferreira Nunes |

## 8. Responsabilidades e frequência

| Atividade | Responsável | Frequência |
|---|---|---|
| Manter premissas e linha de base | Responsável pelo Plano de Custos | Sob demanda |
| Atualizar PV, EV, AC, CPI, SPI e EAC | Frente de gestão/dashboard | Ao fim de cada sprint |
| Validar pontos concluídos | Liderança da sprint e responsáveis pelas histórias | Ao fim de cada sprint |
| Analisar desvios e propor resposta | Equipe | Sprint Review |
| Aprovar alteração da linha de base | Equipe e responsável pelo projeto | Sob demanda |

## 9. Referências

1. UNIVERSIDADE DE BRASÍLIA. [Painel Gestão UnB](https://app.powerbi.com/view?r=eyJrIjoiZWNjNzkzZWQtNTJkMi00YmZhLThkOTgtNzgzNmE2MWMzZjdmIiwidCI6ImVjMzU5YmExLTYzMGItNGQyYi1iODMzLWM4ZTZkNDhmODA1OSJ9). Dotação atualizada de 2026, com fechamento contábil em 20 set. 2026. Acesso em: 22 set. 2026.
2. UNIVERSIDADE DE BRASÍLIA. [Painel Gestão UnB: uma nova ferramenta de transparência e eficiência para a gestão universitária](https://daf.unb.br/destaques/238-painel-de-gestao-projeta-unb-como-modelo-de-transparencia-publica). Decanato de Administração. Acesso em: 22 set. 2026.
3. UNIVERSIDADE DE BRASÍLIA. [Anuário Estatístico 2025 — Repositório DPO](https://repositoriodpo.unb.br/anuarios/anuario-estatistico-2025/). Diretoria de Avaliação e Informações Gerenciais, Decanato de Planejamento, Orçamento e Avaliação Institucional. Acesso em: 22 set. 2026.
4. UNIVERSIDADE DE BRASÍLIA. [Anuário Estatístico 2025 — ano-base 2024: tabela 2.18](https://anuariounb2025.netlify.app/geral#alunos-regulares-na-graduacao-e-na-pos-graduacao-stricto-sensu-2020-a-2024-2o-semestre). Acesso em: 22 set. 2026.
5. RECEITA FEDERAL DO BRASIL. [Taxas de depreciação de bens](https://normasinternet2.receita.fazenda.gov.br/#/consulta/externa/81268/visao/vigente). Acesso em: 21 set. 2026.
6. NEOENERGIA BRASÍLIA. [Composição tarifária](https://www.neoenergia.com/web/brasilia/sua-casa/composicao-tarifaria). Acesso em: 21 set. 2026.
7. PROJECT MANAGEMENT INSTITUTE. *A Guide to the Project Management Body of Knowledge (PMBOK Guide)*. 7. ed. Newtown Square: PMI, 2021.

## Histórico de versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) | Data de revisão |
|---|---|---|---|---|---|
| 1.0 | 21/09/2026 | Criação do plano, linha de base, distribuição por release e controle por EVM-Ágil | [Daniel Ferreira Nunes](https://github.com/Mach1r0) | — | — |
| 1.1 | 22/09/2026 | Atualização do orçamento por estudante com dados do Painel Gestão UnB e recálculo da linha de base | [Daniel Ferreira Nunes](https://github.com/Mach1r0) | — | — |
| 1.2 | 22/09/2026 | Inclusão do Repositório DPO e adoção do total oficial de 50.843 estudantes da tabela 2.18 | [Daniel Ferreira Nunes](https://github.com/Mach1r0) | — | — |
