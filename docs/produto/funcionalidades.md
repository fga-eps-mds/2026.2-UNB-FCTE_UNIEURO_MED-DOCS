# Visão do Produto — Funcionalidades

Esta página faz parte da Visão do Produto do MED e registra as Atividades 6 e 7 da Lean Inception, o brainstorming de funcionalidades e a revisão técnica, de negócio e de UX. Ela dá continuidade ao que foi levantado em [Lean Inception](lean-inception.md), onde estão a declaração de visão, os objetivos de negócio, as personas e as jornadas, e alimenta o [Sequenciador](sequenciador.md) e o [Canvas MVP](canvas-mvp.md). A leitura condensada de tudo está em [Visão do Produto](visao.md).

## Atividade 6 — Brainstorming de Funcionalidades

A pergunta que orientou a atividade foi: o usuário está tentando fazer uma coisa, então o produto deve ter uma funcionalidade para isso, que funcionalidade é essa? As funcionalidades levantadas na ideação foram depois agrupadas em cinco clusters.

### Cluster 1 — Aplicação do teste

- Visualizar tela de instrução simples por tarefa
- Desenhar com a caneta na área de desenho
- Tarefa do relógio
- Tarefa do pentágono com figura de referência
- Tarefa do cubo com figura de referência
- Confirmar desenho e avançar tarefa
- Apagar traço e refazer
- Tela de encerramento sem escore
- Fonte grande e alto contraste

### Cluster 2 — Captura do traçado

- Salvar imagem final do desenho
- Capturar coordenadas, ordem, tempo e contexto do traçado
- Registrar pausas, apagamentos e velocidade
- Registrar se foi dedo ou caneta e qual tablet

### Cluster 3 — Pontuação e resultado

- Extrair características de cada figura
- Rodar inferência do modelo embarcado
- Escore por tarefa e escore geral
- Faixa de desempenho com margem de incerteza
- Visualizar tela de resultado com desenho ao lado do escore
- Destacar características que puxaram o escore
- Registrar concordância ou discordância do profissional de saúde

### Cluster 4 — Acesso e registro

- Cadastro e login do profissional de saúde
- Vincular avaliação ao profissional e ao paciente pseudonimizado
- Listar avaliações anteriores do profissional

### Cluster 5 — Base e conformidade

- Armazenar localmente no tablet
- Exportar dados anonimizados para a base de pesquisa
- Visualizar tela de consentimento (TCLE)
- Avisar que não é diagnóstico

### Sem cluster

- Modo demonstração para o profissional treinar

## Atividade 7 — Revisão Técnica, de Negócio e de UX

Cada funcionalidade foi revisada em três dimensões, em escala de 1 a 3. Esforço técnico é representado no quadro pela marcação `E`, valor de negócio por `$` e valor de UX por `<3`. Além das marcações, a cor de cada post-it registra o nível de confiança da equipe no entendimento da funcionalidade: verde para alta, amarelo para média e vermelho para baixa. A cor é o que o [Sequenciador](sequenciador.md) usa nas regras de composição das ondas. A tabela abaixo transcreve as marcações e as cores do quadro.

| Funcionalidade | Confiança | Esforço | Valor de negócio | Valor de UX |
|---|:---|:---:|:---:|:---:|
| Visualizar tela de instrução simples por tarefa | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#93E396;border:1px solid rgba(0,0,0,.15)"></span> Alta | 2 | 2 | 3 |
| Desenhar com a caneta na área de desenho | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#FFEA79;border:1px solid rgba(0,0,0,.15)"></span> Média | 2 | 3 | 3 |
| Tarefa do relógio | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#93E396;border:1px solid rgba(0,0,0,.15)"></span> Alta | 1 | 3 | 2 |
| Tarefa do pentágono com referência | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#93E396;border:1px solid rgba(0,0,0,.15)"></span> Alta | 1 | 3 | 2 |
| Tarefa do cubo com referência | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#93E396;border:1px solid rgba(0,0,0,.15)"></span> Alta | 1 | 3 | 2 |
| Confirmar desenho e avançar | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#93E396;border:1px solid rgba(0,0,0,.15)"></span> Alta | 1 | 2 | 3 |
| Apagar traço e refazer | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#93E396;border:1px solid rgba(0,0,0,.15)"></span> Alta | 1 | 2 | 3 |
| Visualizar encerramento do teste sem escore visualizável | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#93E396;border:1px solid rgba(0,0,0,.15)"></span> Alta | 1 | 3 | 3 |
| Fonte grande e alto contraste | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#93E396;border:1px solid rgba(0,0,0,.15)"></span> Alta | 2 | 2 | 3 |
| Exportar imagens finais dos desenhos | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#93E396;border:1px solid rgba(0,0,0,.15)"></span> Alta | 1 | 2 | 1 |
| Capturar coordenadas, ordem e tempo do traçado | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#93E396;border:1px solid rgba(0,0,0,.15)"></span> Alta | 2 | 3 | 1 |
| Pausas, apagamentos e velocidade | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#FFEA79;border:1px solid rgba(0,0,0,.15)"></span> Média | 2 | 2 | 1 |
| Extrair características de cada figura | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#FFBDAE;border:1px solid rgba(0,0,0,.15)"></span> Baixa | 3 | 2 | 1 |
| Rodar inferência do modelo embarcado | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#FFBDAE;border:1px solid rgba(0,0,0,.15)"></span> Baixa | 3 | 3 | 2 |
| Escore por tarefas individuais e tarefa geral | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#FFEA79;border:1px solid rgba(0,0,0,.15)"></span> Média | 2 | 3 | 3 |
| Faixa de desempenho com incerteza | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#FFEA79;border:1px solid rgba(0,0,0,.15)"></span> Média | 2 | 3 | 2 |
| Resultado com desenhos ao lado do escore | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#FFEA79;border:1px solid rgba(0,0,0,.15)"></span> Média | 2 | 3 | 3 |
| Destacar características que puxaram o escore | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#93E396;border:1px solid rgba(0,0,0,.15)"></span> Alta | 2 | 2 | 3 |
| Registrar concordância ou discordância | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#93E396;border:1px solid rgba(0,0,0,.15)"></span> Alta | 1 | 2 | 3 |
| Cadastrar e logar o profissional de saúde | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#93E396;border:1px solid rgba(0,0,0,.15)"></span> Alta | 1 | 3 | 3 |
| Vincular avaliação ao profissional e paciente pseudonimizado | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#93E396;border:1px solid rgba(0,0,0,.15)"></span> Alta | 2 | 3 | 2 |
| Listar avaliações anteriores | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#93E396;border:1px solid rgba(0,0,0,.15)"></span> Alta | 2 | 1 | 3 |
| Armazenamento local persistente | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#93E396;border:1px solid rgba(0,0,0,.15)"></span> Alta | 2 | 3 | 1 |
| Exportar dados anonimizados | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#FFEA79;border:1px solid rgba(0,0,0,.15)"></span> Média | 2 | 3 | 1 |
| Tela de consentimento (TCLE) | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#FFEA79;border:1px solid rgba(0,0,0,.15)"></span> Média | 1 | 3 | 2 |
| Aviso de que não é diagnóstico | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#93E396;border:1px solid rgba(0,0,0,.15)"></span> Alta | 1 | 1 | 2 |
| Modo demonstração | <span style="display:inline-block;width:0.9em;height:0.9em;border-radius:2px;vertical-align:middle;background:#93E396;border:1px solid rgba(0,0,0,.15)"></span> Alta | 1 | 1 | 3 |

### Leitura da revisão

As funcionalidades de maior esforço técnico são "Extrair características de cada figura" e "Rodar inferência do modelo embarcado", ambas no Cluster 3 e ambas dependentes do trabalho conduzido no repositório de IA. Elas concentram o risco técnico do MVP, e são também os dois únicos cartões vermelhos do quadro.

As funcionalidades de maior valor de UX e menor esforço, como "Confirmar desenho e avançar", "Apagar traço e refazer" e "Registrar concordância ou discordância", são candidatas naturais às primeiras ondas do sequenciador.

"Listar avaliações anteriores", "Aviso de que não é diagnóstico" e "Modo demonstração" receberam o menor valor de negócio do quadro, o que explica sua ausência nas primeiras ondas.

## Histórico de Versões

| Versão | Descrição | Autor(es) | Data | Revisor(es) | Data de Revisão |
|---|---|---|---|---|---|
| 1.0 | Criação da página com o registro das Atividades 6 e 7 da Lean Inception, transcritas do quadro de Visão do Produto | [Artur Mendonça Arruda](https://github.com/ArtyMend07) | 18/09/2026 | [Lucas Mendonça Arruda](https://github.com/lucasarruda9) | 19/09/2026 |
| 1.1 | Inclusão da coluna de confiança, com a cor do post-it de cada funcionalidade no quadro da Atividade 7 | [Artur Mendonça Arruda](https://github.com/ArtyMend07) | 21/09/2026 | | |
