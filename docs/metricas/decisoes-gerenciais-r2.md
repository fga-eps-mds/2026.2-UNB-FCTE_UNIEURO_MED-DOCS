# Decisões gerenciais da R2

Esta página registra as decisões gerenciais do DA-R2, como pede o cronograma da
disciplina: cada decisão parte de um dado do dashboard e traz **causa, evidência e
ação**. Os valores são do dia **24/10/2026**, com a versão 1.2.6 do aplicativo.

Os indicadores usados estão em [Qualidade do produto](qualidade-do-produto.md) e em
[Processo e comparação R1 × R2](processo-e-comparativo.md).

**Tabela 1:** Decisões gerenciais da R2

| Id | Decisão | Indicador de origem |
|---|---|---|
| D-R2-01 | Levar o aceite pendente para a reunião da R2 e registrar o risco | Velocidade e entrega do comprometido (P2) |
| D-R2-02 | Planejar a Sprint 4 pela capacidade real, sem puxar história nova no meio da sprint | Estabilidade do escopo (P3) |
| D-R2-03 | Manter e estender o padrão de comentar as regras de negócio | Qualidade do código (QC) e comentários (m2) |
| D-R2-04 | Corrigir os problemas abertos no SonarCloud | Código bloqueante (m7) e defeitos prováveis (m8) |

**Fonte:** [Gabriel Lopes de Amorim](https://github.com/BrzGab), 2026

## D-R2-01: Levar o aceite pendente para a reunião da R2 e registrar o risco

**Causa.** A velocidade é zero em todas as sprints: nenhum ponto de história foi aceito
pelos *Product Owners*. Cinco histórias, com 45 pontos, estão na coluna Aceitação PO:
#5 (cadastro), #6 (login), #7 (registro do atendimento), #8 (instrução) e #46 (tela
inicial). Os APKs e os formulários de aceitação da R1 e da Release Minor 1 já foram
enviados. Na reunião de 19/10 ([Ata 10](../atas-reunioes/Ata-10-EPS-2026-10-19-PO.md)),
o *Product Owner* e o cliente se comprometeram a responder, com prazo do cliente em
20/10, e até 24/10 não há resposta registrada. Sem aceite, a entrega do comprometido
(P2) fica em 0 e o índice de processo da R2 fica na faixa crítica (P = 0,58).

**Evidência.** Aba "Q-Rapids e R1 × R2" do dashboard (Processo e Comparação entre
Releases); [Processo e comparação R1 × R2](processo-e-comparativo.md); coluna Aceitação
PO do ZenHub; encaminhamentos da Ata 10.

**Ação.**

1. Fazer o teste de aceitação ao vivo na reunião da R2, com o APK instalado e o
   formulário aberto, e registrar o resultado em ata.
2. Registrar no [Plano de Gestão de Riscos](../processo/riscos.md) que o risco R06
   (indisponibilidade do cliente ou de especialistas) se concretizou, com a resposta
   adotada.
3. Mostrar no dashboard os pontos em Aceitação PO separados dos aceitos, mantendo
   "somente aceitas" como padrão, para que o time não pareça parado quando está
   esperando aceite.

## D-R2-02: Planejar a Sprint 4 pela capacidade real, sem puxar história nova no meio da sprint

**Causa.** Na Sprint 3, 37 dos 74 pontos comprometidos entraram com a sprint em
andamento: as histórias #21, #8, #9 e #10, apresentadas aos *Product Owners* em 19/10,
e a #11, puxada da R3. Só metade do compromisso final estava planejada no início da
sprint, e a estabilidade do escopo da R2 caiu para 0,75 (P3). Ao mesmo tempo, os pontos
planejados por sprint passaram de 21 na R1 para 57 na R2, sem nenhum ponto aceito.

**Evidência.** Aba "Q-Rapids e R1 × R2" do dashboard (Processo);
[Processo e comparação R1 × R2](processo-e-comparativo.md); sprints do ZenHub.

**Ação.** No planejamento da Sprint 4, comprometer só histórias validadas pelo *Product
Owner* e dentro da capacidade medida nas sprints anteriores, e registrar como
replanejamento qualquer história que entre com a sprint em andamento.

## D-R2-03: Manter e estender o padrão de comentar as regras de negócio

**Causa.** A qualidade do código (QC) está na faixa de atenção desde a R1 por causa dos
comentários: a densidade de arquivos com 10% a 30% de linhas comentadas (m2) era 0,22
na R1 e 0,24 na RM1. Na versão 1.2.6 ela subiu para 0,41 e a QC chegou a 0,80, no
limite da faixa adequada. A melhora veio do código novo (as telas de desenho e a tela
final), que já entrou com as regras comentadas, e não dos arquivos antigos: 39 dos 66
arquivos de código continuam fora da faixa.

**Evidência.** Aba "Q-Rapids e R1 × R2" do dashboard, seção "De onde vem cada nota";
[Qualidade do produto](qualidade-do-produto.md).

**Ação.** Manter o padrão nos arquivos novos e comentar as regras de negócio e as
restrições não óbvias dos arquivos antigos, sem comentários óbvios só para subir a
métrica, como orienta a Tabela 4 do
[Plano de Qualidade](../processo/plano_de_qualidade.md). Cobrar isso na revisão dos PRs.

## D-R2-04: Corrigir os problemas abertos no SonarCloud

**Causa.** Três problemas seguem abertos na `develop` desde a R1 ou a RM1: um grave de
manutenibilidade e um de confiabilidade no `registration.ts`, e um de confiabilidade no
`cpf-protection.ts`. Eles deixam m7 em 0,98 e m8 em 0,97. Os valores só subiram da R1
para a R2 porque o código cresceu de 18 para 66 arquivos, e não porque os problemas
foram resolvidos.

**Evidência.** Aba "Q-Rapids e R1 × R2" do dashboard, seção "De onde vem cada nota";
SonarCloud da `develop`.

**Ação.** Corrigir os três problemas, o que leva m7 e m8 a 1,00, ou registrar a exceção,
como pede a seção 6 do [Plano de Qualidade](../processo/plano_de_qualidade.md).

## Pendência para a R3

A qualidade interna do repositório de IA ainda não está medida: a última análise do
SonarCloud é de 17/09, com 19 linhas de código. Isso depende da issue #13 do repositório
de IA e fica como ponto de atenção para a R3.

## Uso crítico de IA na análise

O cálculo do Q-Rapids, os indicadores de processo e estas decisões foram feitos com
apoio de IA generativa (Claude). Cada resultado foi conferido antes de entrar no
dashboard ou nesta página.

**Tabela 2:** Saídas da IA aceitas e rejeitadas

| Saída da IA | Decisão | Como foi conferida |
|---|---|---|
| Implementação das fórmulas m1 a m8 e da agregação do plano de qualidade | Aceita | Testes automatizados, alteração proposital das regras para ver os testes falharem e recálculo independente de uma versão |
| Coleta dos problemas do SonarCloud por branch e da branch de cada release | Aceita | Branch de cada release conferida pelo histórico do git |
| Afirmação de que m7 e m8 subiram da R1 para a R2 porque os problemas foram corrigidos | Rejeitada | A lista de arquivos mostrou os mesmos problemas abertos; os valores subiram porque o código cresceu |
| Sugestão de usar os limiares do notebook de 2026.1 (85% de cobertura e 300 s por teste) | Rejeitada | O time manteve os limiares do próprio plano, que seguem para validação do professor |
| Afirmação de que o notebook do professor era obrigatório no DA-R2 e de que as decisões valiam 30% da nota | Rejeitada | Não consta no plano de ensino nem no cronograma de 2026.2; veio de documentos de times de 2026.1 |
| Contagem de 0 defeitos quando o arquivo de bugs ainda não tinha sido coletado | Rejeitada | Corrigida para "não medida", como manda o princípio do plano de qualidade |
| Ação original da D-R2-01 (enviar o APK e o formulário aos *Product Owners*) | Rejeitada | O time lembrou que os formulários já tinham sido enviados; a ação foi trocada pelo aceite ao vivo e pelo registro do risco |

**Fonte:** [Gabriel Lopes de Amorim](https://github.com/BrzGab), 2026

## Limitações

- **Data dos valores.** As decisões usam os valores de 24/10. A página
  [Processo e comparação R1 × R2](processo-e-comparativo.md) mostra os de 22/10, e por
  isso traz P3 = 0,77 e 32 de 69 pontos.
- **Sprint 3 em andamento.** P2, P3 e a velocidade da R2 mudam se houver aceite antes do
  fechamento da R2.

## Histórico de versão

| Versão | Data | Descrição | Autor | Revisor |
|:------:|------|-----------|-------|---------|
| `1.0` | 25/10/2026 | Decisões gerenciais da R2 | [Gabriel Lopes de Amorim](https://github.com/BrzGab) | |
