---
title: Estimativa do Backlog
---

# Estimativa do Backlog do Produto

## 1. Finalidade

Este documento registra como a equipe estimou as histórias de usuário do backlog do
aplicativo, em pontos de história, e o resultado obtido até 12/10/2026.

A estimativa responde a dois apontamentos da avaliação da R1, registrados na
[Ata 08](../atas-reunioes/Ata-08-EPS-2026-10-02-PO.md): o backlog não tinha
estimativa, o que impedia conhecer o seu tamanho, e os pontos tinham sido dados a
tarefas. A partir desta estimativa, os pontos ficam só nas histórias de usuário e a
soma por release alimenta o EVM-Ágil descrito no
[Plano de Custos](plano_de_custos.md).

O trabalho corresponde à issue
[#71](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-DOCS/issues/71).

## 2. Fundamentação

### 2.1 Pontos de história

O ponto de história mede o tamanho de uma história em relação às outras, sem
converter em horas. A equipe já usa histórias de usuário no formato de Cohn (2004),
e o EVM-Ágil adotado no projeto (Sulaiman, Barton e Blackburn, 2006) parte da soma
dos pontos planejados para a release.

### 2.2 Planning poker

O planning poker foi descrito por Grenning (2002) para o planejamento de releases.
O cliente lê a história, a equipe tira dúvidas, cada pessoa escreve a sua estimativa
sem comentar e todas as cartas são viradas ao mesmo tempo. Quando as estimativas
coincidem, o valor é registrado sem discussão. Quando divergem, quem deu o menor e o
maior valor explica o motivo e a equipe busca o consenso.

Três pontos do texto de Grenning orientaram a aplicação neste projeto:

- O objetivo é uma estimativa aproximada do esforço para delimitar o escopo. O autor
  afirma que a precisão de cada estimativa não é a meta.
- Toda a equipe estima, e não só as pessoas mais experientes ou mais falantes.
- Sem consenso em uma história, ela pode ser adiada, dividida ou ficar com o menor
  valor, porque é uma entre muitas.

O guia da Mountain Goat Software ([s.d.]), empresa de Mike Cohn, acrescenta que a
escolha de cada pessoa é privada para evitar a ancoragem, que uma a três rodadas
costumam bastar e que o consenso não exige unanimidade, só concordância suficiente
para usar a estimativa. O baralho típico citado tem os valores 0, 1, 2, 3, 5, 8, 13,
20, 40 e 100. Para equipes remotas, a recomendação é usar uma ferramenta que esconda
as estimativas até todos escolherem.

A ancoragem é o desvio de uma estimativa em direção a um número visto antes. Aranda
e Easterbrook (2005) observaram esse efeito em estimativas de software, inclusive
quando o número apresentado era irrelevante para a tarefa.

### 2.3 Evidência empírica

Moløkken-Østvold, Haugen e Benestad (2008) compararam, em um projeto de software, o
consenso obtido com planning poker com a média das estimativas individuais das
mesmas tarefas. O consenso foi menos otimista e mais preciso que a média.

Mahnič e Hovelja (2012) estudaram 13 equipes de estudantes em um projeto com Scrum,
situação próxima à desta disciplina. As estimativas do planning poker ficaram mais
perto do esforço real que a combinação estatística das estimativas individuais.

Os dois estudos sustentam uma decisão deste documento: o valor de cada história é o
que a equipe validou em conjunto, e não a média das estimativas individuais.

## 3. Como a equipe aplicou

A técnica foi adaptada à forma de trabalho da equipe, que tem dez integrantes e
conduz a maior parte do alinhamento de forma assíncrona. A dinâmica foi conduzida
por [Artur Mendonça Arruda](https://github.com/ArtyMend07).

1. As histórias de usuário abertas do repositório do aplicativo foram listadas em
   uma planilha compartilhada, uma por linha, com o link da issue, o épico e a
   release. Tarefas ficaram de fora.
2. Cada integrante recebeu uma coluna e preencheu a sua estimativa para cada
   história, na escala de Fibonacci. Os valores usados foram 2, 3, 5, 8 e 13.
3. As histórias #5 e #6, que já tinham 8 pontos no ZenHub, serviram de referência
   para as demais.
4. Depois do preenchimento, o condutor propôs como consenso o valor mais votado de
   cada história. No único empate, da história #11, a proposta ficou com o valor do
   lado da mediana.
5. A proposta foi apresentada à equipe, com destaque para as histórias mais
   divididas. A equipe concordou com os valores, e o condutor os registrou na
   coluna de consenso.

Houve duas rodadas. A primeira, em 28/09/2026, cobriu as histórias #5, #6, #7, #21
e #23. A segunda, de 05/10 a 12/10/2026, estendeu a planilha a todo o backlog e
manteve os valores da primeira. As histórias #58 e #59, criadas em 07/10, entraram
durante a segunda rodada.

### 3.1 Diferenças em relação à técnica

| Aspecto | Planning poker de referência | Como foi feito | Efeito |
|---|---|---|---|
| Momento | Reunião com toda a equipe | Preenchimento assíncrono, ao longo de uma semana | Todos puderam estimar sem depender de um horário comum |
| Sigilo da estimativa | Escolha privada e revelação simultânea | Planilha comum, em que cada pessoa via as estimativas já preenchidas | Risco de ancoragem nos valores de quem preencheu antes |
| Esclarecimento da história | O cliente lê a história e a equipe tira dúvidas antes de estimar | Cada pessoa leu a issue pelo link da planilha | Dúvidas sobre a história não foram resolvidas antes da estimativa |
| Divergência | Quem deu o menor e o maior valor explica, e a equipe estima de novo | Proposta do valor mais votado, validada pela equipe, sem nova rodada de estimativas individuais | O consenso é a concordância com a proposta, sem a explicação de quem estimou nos extremos |
| Registro | Valor anotado na carta da história | Coluna de consenso preenchida pelo condutor | O valor fica rastreável ao lado das estimativas individuais |

### 3.2 Limitações

- A planilha não esconde as estimativas, então a independência das estimativas
  individuais não pode ser afirmada. É a principal diferença em relação à técnica.
- Um integrante preencheu 11 das 24 histórias. As demais têm nove estimativas.
- Os critérios de aceitação das histórias #7 e #21 estavam em revisão
  ([#82](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-DOCS/issues/82))
  durante a estimativa.
- O consenso partiu do valor mais votado. Em cinco histórias esse valor teve menos
  da metade das estimativas (#8, #11, #15, #16 e #58), e em três teve exatamente a
  metade (#5, #10 e #12).

Para as próximas rodadas, o registro em ferramenta que revele as estimativas só
depois de todos responderem elimina a primeira limitação.

## 4. Resultado

A planilha com as estimativas está em
[`planning-poker-historias.csv`](../assets/dados/planning-poker-historias.csv). A
release de cada história é a release-alvo do [roadmap](roadmap.md). A coluna de release
da planilha traz o marco que a issue tinha no GitHub quando a planilha foi montada.

**Tabela 1:** Estimativas individuais e consenso por história, em pontos de história

| História | Release-alvo | Artur | Cláudio | Daniel | Eduardo | Gabriel | Gustavo | Henrique | Lucas | Thales | Vitor | Faixa | Mais votado | Consenso |
|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| [#5](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/5) Cadastro do médico no tablet | R2 | 8 | 8 | 8 | 8 | 5 | 5 | 5 | 5 | 5 | 8 | 5 a 8 | 5 e 8 | 8 |
| [#6](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/6) Login do médico antes de aplicar o teste | R2 | 5 | 8 | 8 | 8 | 8 | 8 | 5 | 8 | 5 | 5 | 5 a 8 | 8 | 8 |
| [#7](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/7) Registro do atendimento antes do teste | R2 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| [#8](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/8) Instrução simples antes de cada desenho | R3 | 2 | 8 | 13 | 8 | 5 | 3 | 3 | 2 | 8 | 8 | 2 a 13 | 8 | 8 |
| [#9](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/9) Três tarefas de desenho em sequência | R3 | 8 | 8 | 13 | 8 | 8 | 5 | 8 | 8 | 8 | 8 | 5 a 13 | 8 | 8 |
| [#10](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/10) Captura do traçado e da imagem final | R3 | 8 | 5 | 8 | 13 | 13 | 8 | 13 | 13 | 13 | 8 | 5 a 13 | 13 | 13 |
| [#11](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/11) Tela final do paciente sem escore | R3 | 2 | 8 | 13 | 5 | 5 | 8 | 3 | 3 | 5 | 8 | 2 a 13 | 5 e 8 | 5 |
| [#12](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/12) Escore por desenho calculado no tablet | R3 | 13 | 8 | 13 | 8 | 8 | 5 | 5 | 8 | 8 | 5 | 5 a 13 | 8 | 8 |
| [#13](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/13) Escore geral com faixa de incerteza | R3 | 5 | 8 | 13 | 8 | 8 | 5 | 8 | 8 | 8 | 5 | 5 a 13 | 8 | 8 |
| [#14](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/14) Desenho, escore e o que influenciou o resultado | R3 | 8 | 13 | 13 | 13 | 13 | 5 | 8 | 13 | 8 | 13 | 5 a 13 | 13 | 13 |
| [#15](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/15) Uso completo sem internet | R3 | 2 | 5 | 8 | 8 | 3 |  | 5 | 3 | 5 | 5 | 2 a 8 | 5 | 5 |
| [#16](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/16) Nenhum dado enviado para fora do tablet | R3 | 2 | 5 | 13 | 5 | 8 |  | 5 | 5 | 8 | 8 | 2 a 13 | 5 | 5 |
| [#17](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/17) Dados cifrados no tablet | R3 | 8 | 13 | 8 | 13 | 13 |  | 8 | 13 | 8 | 13 | 8 a 13 | 13 | 13 |
| [#21](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/21) Aceite do TCLE antes do teste | R2 | 3 | 5 | 5 | 3 | 3 |  | 3 | 3 | 3 | 3 | 3 a 5 | 3 | 3 |
| [#22](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/22) Exportar dados da avaliação em XML | R3 | 8 | 13 | 8 | 8 | 13 |  | 8 | 8 | 5 | 5 | 5 a 13 | 8 | 8 |
| [#23](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/23) Confirmar ou refazer desenho antes de avançar | R3 | 5 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 5 | 5 a 8 | 8 | 8 |
| [#24](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/24) Configurar alto contraste e tamanho da fonte | Após o MVP | 5 | 8 | 5 | 5 | 8 |  | 5 | 5 | 8 | 8 | 5 a 8 | 5 | 5 |
| [#25](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/25) Salvar e retomar avaliações no tablet | R3 | 8 | 5 | 8 | 5 | 5 |  | 8 | 5 | 8 | 8 | 5 a 8 | 8 | 8 |
| [#46](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/46) Tela inicial do profissional com os atalhos | Sem release | 3 | 8 | 8 | 8 | 5 |  | 5 | 3 | 8 | 8 | 3 a 8 | 8 | 8 |
| [#47](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/47) Excluir um paciente com confirmação | Sem release | 5 | 8 | 5 | 8 | 8 |  | 8 | 5 | 8 | 8 | 5 a 8 | 8 | 8 |
| [#48](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/48) Recuperar a senha sem internet | Sem release | 5 | 13 | 8 | 8 | 13 |  | 13 | 5 | 13 | 13 | 5 a 13 | 13 | 13 |
| [#49](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/49) Acesso do responsável pela pesquisa a todos os atendimentos | Sem release | 5 | 13 | 8 | 8 | 8 |  | 8 | 13 | 8 | 8 | 5 a 13 | 8 | 8 |
| [#58](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/58) Excluir um exame aberto por engano | Sem release | 3 | 8 | 5 | 5 | 5 |  | 8 | 3 | 5 | 8 | 3 a 8 | 5 | 5 |
| [#59](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/59) Lista dos pacientes atendidos na tela inicial | Sem release | 5 | 5 | 5 | 5 | 5 |  | 5 | 2 | 8 | 5 | 2 a 8 | 5 | 5 |

**Fonte:** planilha de estimativas da equipe, situação em 12/10/2026.

As histórias com maior divergência são a #8, a #11 e a #16, com estimativas de 2 a
13. Na história #5 as estimativas ficaram divididas entre 5 e 8 pontos, e o consenso
foi 8, valor que ela já tinha no ZenHub.

## 5. Pontos planejados por release

No EVM-Ágil, os pontos planejados para a release (PRP) são a soma dos pontos das
histórias previstas para ela. A Tabela 2 soma os valores de consenso da Tabela 1.

**Tabela 2:** Pontos planejados por release

| Release | Histórias | Pontos planejados |
|---|:-:|:-:|
| R2 | 4 | 24 |
| R3 | 13 | 110 |
| Após o MVP | 1 | 5 |
| Sem release definida | 6 | 47 |
| **Backlog** | **24** | **186** |

**Fonte:** Tabela 1 e [roadmap](roadmap.md).

O consenso de cada história é registrado no campo de estimativa da issue no ZenHub,
só nas histórias de usuário. É desse campo que o EVM lê os pontos: o script
[`scripts/coleta_zenhub.py`](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-DOCS/blob/main/scripts/coleta_zenhub.py)
grava os pontos por sprint em `zenhub_analytics.json`, e o dashboard consome esse
arquivo, como descrito em [Coleta de métricas](../metricas/coleta-de-metricas.md).

## 6. Pendências

- Registrar no ZenHub os valores de consenso e retirar pontos de tarefas, se ainda
  houver.
- Definir a release das seis histórias sem release, para que entrem no PRP.
- Rever as estimativas das histórias #7 e #21 se a revisão dos critérios mudar o
  escopo delas.

## 7. Referências

ARANDA, Jorge; EASTERBROOK, Steve. Anchoring and adjustment in software estimation.
In: *European Software Engineering Conference and ACM SIGSOFT Symposium on the
Foundations of Software Engineering (ESEC/FSE)*, 2005. p. 346-355.

COHN, Mike. *User Stories Applied: For Agile Software Development*. Boston:
Addison-Wesley, 2004.

GRENNING, James. *Planning Poker or How to avoid analysis paralysis while release
planning*. 2002. Disponível em:
<https://wingman-sw.com/papers/PlanningPoker-v1.1.pdf>. Acesso em: 12 out. 2026.

MAHNIČ, Viljan; HOVELJA, Tomaž. On using planning poker for estimating user
stories. *Journal of Systems and Software*, v. 85, n. 9, p. 2086-2095, 2012.

MOLØKKEN-ØSTVOLD, Kjetil; HAUGEN, Nils Christian; BENESTAD, Hans Christian. Using
planning poker for combining expert estimates in software projects. *Journal of
Systems and Software*, v. 81, p. 2106-2117, 2008.

MOUNTAIN GOAT SOFTWARE. *Planning Poker*. [s.d.]. Disponível em:
<https://www.mountaingoatsoftware.com/agile/planning-poker>. Acesso em: 12 out. 2026.

SULAIMAN, Tamara; BARTON, Brent; BLACKBURN, Thomas. AgileEVM: Earned Value
Management in Scrum Projects. In: *Agile Conference*, 2006. IEEE, 2006.

## Histórico de Versões

| Versão | Descrição | Autor(es) | Data | Revisor(es) | Data de Revisão |
|---|---|---|---|---|---|
| 1.0 | Registro da dinâmica de estimativa, das estimativas e do consenso por história e dos pontos planejados por release | [Artur Mendonça Arruda](https://github.com/ArtyMend07) | 12/10/2026 | | |
