# Plano de Gerenciamento da Qualidade

## 1. Objetivo e abrangência

Este plano define como a equipe planeja, verifica e acompanha a qualidade do aplicativo Android e do modelo de IA do MED durante o semestre 2026.2. A análise estática do SonarCloud fornece indicadores de código, mas a aceitação de uma release também depende de testes automatizados, execução no tablet e validação dos critérios das histórias de usuário.

O aplicativo e a inferência devem funcionar **100% offline**. Dados de atendimento, imagens, traçados e escores não podem sair do dispositivo; o paciente não deve visualizar o escore. Essas restrições são verificadas conforme a [Visão do Produto](../produto/visao.md), a [Arquitetura](../produto/arquitetura.md) e os critérios de aceitação das histórias.

Este documento contém **metas de qualidade e uma linha de base observada**, não uma declaração de que as metas já foram atingidas. As metas herdadas do [Cronograma](cronograma.md) são identificadas como tais; os demais limites operacionais são propostas para validação da equipe.

## 2. Fontes, unidade de análise e linha de base

A unidade de acompanhamento é cada repositório com código executável, na branch de integração `develop`. A `main` do APP e da IA não representa o incremento em desenvolvimento. Cada medição deve registrar repositório, branch, commit analisado, data da análise, valor e link da evidência. A consulta abaixo foi realizada em **26/09/2026**; o instante da análise exibida pelo SonarCloud deve ser registrado na próxima coleta.

| Indicador em `develop` | [APP no SonarCloud](https://sonarcloud.io/project/overview?id=fga-eps-mds_2026.2-UNB-FCTE_UNIEURO_MED-APP&branch=develop) | [IA no SonarCloud](https://sonarcloud.io/project/overview?id=fga-eps-mds_2026.2-UNB-FCTE_UNIEURO_MED-IA&branch=develop) |
|---|---:|---:|
| Linhas de código analisadas (NCLOC) | 777 | 20 |
| Cobertura publicada | 0,0% | Não publicada |
| Bugs / vulnerabilidades reportados | 0 / 0 | 0 / 0 |
| `Code smells` | 6 | 0 |
| Duplicação no código total | 4,1% | 0,0% |
| `Quality gate` | **Reprovado** | **Aprovado**, com escopo ainda insuficiente |

No APP, as condições que reprovam o gate são **cobertura de código novo de 0,0%** frente ao limite de 80% e **duplicação de código novo de 4,2%** frente ao limite de 3%. Esses valores de **código novo** não devem ser confundidos com os 0,0% de cobertura e 4,1% de duplicação do **código total**. Os demais itens do gate consultado estavam aprovados.

A ausência de cobertura na IA significa **sem medição publicada**, não 0%. Seu gate aprovado se refere ao pequeno conjunto analisado, ainda sem implementação de inferência e suíte de testes na branch de integração; não comprova qualidade do modelo. Da mesma forma, zero bugs reportados não equivale a ausência de defeitos em uso. O APP ainda não publica no Sonar a cobertura prevista pelo [PR de testes #31](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/pull/31), que está em revisão.

### Atualização da linha de base

Ao final de cada sprint, a frente de Qualidade/DevOps registra os valores atuais da API do SonarCloud ou do painel do projeto, com link para a análise. Dados coletados em PR são identificados como **pré-integração**; só a análise da branch de integração compõe o resultado consolidado da sprint. Se uma métrica não for publicada, registra-se **N/D — não disponível**, a causa e a ação para instrumentá-la. Valores simulados do dashboard nunca substituem resultados do Sonar ou do pipeline.

## 3. Critérios de qualidade

### 3.1 Código, segurança e testes automatizados

| Critério | Meta e interpretação | Fonte de comprovação |
|---|---|---|
| Gate do SonarCloud | **Aprovado** na branch de integração antes de considerar a release concluída. Condições atuais: classificação A para confiabilidade, segurança e manutenibilidade do código novo; cobertura nova ≥ 80%; duplicação nova ≤ 3%; 100% dos `security hotspots` novos revisados. Se a configuração mudar, registrar a alteração e sua justificativa. | Painel/API do SonarCloud e check do PR |
| Cobertura exigida pela disciplina | **≥ 85% de cobertura de testes unitários na R1, ≥ 85% com testes de integração na R2 e ≥ 90% na R3**, conforme o [Cronograma](cronograma.md). Reportar separadamente por repositório que tenha código de produção testável; não calcular média entre APP e IA nem declarar cumprimento quando a cobertura estiver N/D. A equipe deve validar o denominador e as exclusões antes da aferição. | Relatório LCOV ou equivalente, pipeline e SonarCloud |
| Testes automatizados | Testes relevantes para a alteração executados e aprovados no PR; falhas não podem ser ocultadas ou ignoradas para obter gate verde. O APP deve incluir casos válidos e inválidos de cadastro/login, persistência e fluxos adicionados. A IA deve testar pré-processamento, inferência, formato de saída e integração quando houver código versionado. | Pipeline, relatório de testes e PR |
| Defeitos e vulnerabilidades | Nenhum defeito bloqueador ou vulnerabilidade crítica/alta sem tratamento antes de liberar o incremento. Achados do Sonar devem ser triados; falsos positivos exigem justificativa no PR/issue. | SonarCloud, issues e revisão |
| Duplicação e manutenibilidade | Usar o limite do gate para código novo; acompanhar tendência de duplicação e `code smells` totais, com ação quando houver crescimento não justificado. O valor total de 4,1% no APP é linha de base, não meta. | SonarCloud por branch e por PR |

A meta de cobertura do cronograma refere-se ao projeto acadêmico; a regra de acompanhamento por repositório e as exclusões de arquivos precisam ser aprovadas pela equipe. Cobertura alta mede execução de linhas, não substitui qualidade das asserções nem aceitação funcional. Enquanto a IA não tiver código testável na integração, registrar **N/D e pendência**, sem tratar o gate verde como cumprimento da meta de cobertura.

### 3.2 Comportamento do aplicativo no tablet

Uma história só é aceita quando seus critérios observáveis passam no dispositivo-alvo, com evidência vinculada à issue ou ao PR. Considerando a redução do escopo da R1 proposta no [PR de roadmap #57](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-DOCS/pull/57), verificar especialmente cadastro e login do profissional **sem internet**, persistência após fechar e reabrir o aplicativo, rejeição de campos e credenciais inválidos e bloqueio de acesso não autorizado. Se o replanejamento não for aprovado, os cenários de avaliação e desenho previstos no cronograma também precisam ser executados na R1. Telas navegáveis, isoladamente, não atendem a esses critérios.

Para as releases seguintes, os roteiros devem incluir consentimento, as três tarefas de desenho, salvamento/recuperação local, execução da inferência embarcada e separação entre a tela de resultado do profissional e a tela final do paciente. Cada roteiro registra versão do APK, modelo do tablet, configuração de rede, passos, resultado esperado, resultado observado, evidência e responsável. A liberação exige **100% dos cenários críticos aprovados** e **nenhum defeito bloqueador aberto**; cenários não executados são pendências, não aprovações.

### 3.3 Qualidade do modelo de IA e dados

SonarCloud avalia o código da IA, não a validade do modelo. Quando o treino e a inferência forem versionados, cada experimento deve registrar versão dos dados, separação treino/validação/teste, semente, parâmetros, versão do código, métricas (por exemplo, acurácia, F1 e AUC quando aplicáveis), resultados por execução e limitações. A equipe deve definir com o PO critérios quantitativos de aceitação do modelo, inclusive por perfil de paciente, antes de declarar sua adequação. **Não há meta clínica aprovada neste plano.**

A integração deve comprovar que o artefato exportado executa no tablet sem rede, mantém o formato de entrada/saída acordado e não envia dados clínicos. Dados brutos e identificações de pacientes não podem ser versionados. Resultados de treino ainda presentes apenas em PR são evidência preliminar, não resultado de release.

## 4. Verificação, registro e resposta a desvios

| Momento | Verificação | Evidência e responsável |
|---|---|---|
| A cada PR | Revisão por outra pessoa, testes pertinentes, análise Sonar e vínculo com a issue/critério de aceitação | Autor anexa comandos/resultados; revisor e Qualidade/DevOps conferem |
| Ao fim da sprint | Comparação das métricas de `develop` com a linha de base, triagem de achados e atualização do painel | Qualidade/DevOps registra tabela datada e issues de ação; liderança acompanha |
| Antes da release | Gate, cobertura, testes funcionais no tablet, defeitos críticos e aceite do PO/cliente quando aplicável | Equipe reúne links de pipelines, APK, roteiros e ata/issue de aceite |
| Após a release | Revisão de incidentes, regressões e metas não alcançadas | Equipe documenta causa, responsável, prazo e decisão de correção |

Quando uma meta falhar: (1) registrar o resultado e a evidência; (2) abrir ou atualizar issue com causa, risco, responsável e prazo; (3) corrigir e medir novamente; (4) se não for possível antes da release, submeter a exceção e o impacto à decisão explícita da equipe e do responsável pelo produto. Uma exceção documentada não transforma métrica reprovada em aprovada.

## 5. Ações iniciais a partir da linha de base

1. **APP — cobertura:** concluir a revisão do [PR #31](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/pull/31), executar a suíte e publicar o relatório LCOV na análise da branch de integração. Reavaliar a cobertura total, a cobertura nova e o gate; registrar o denominador e as exclusões.
2. **APP — duplicação:** localizar no Sonar os trechos novos que levaram a duplicação a 4,2%, corrigir ou justificar o achado e repetir a análise. A meta operacional é atender à condição de ≤ 3% do gate.
3. **R1 — fluxo real:** executar e registrar os critérios de aceitação das histórias de [cadastro](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/5) e [login](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/6) com o tablet desconectado.
4. **IA — evidência válida:** integrar código reproduzível de treino e inferência, adicionar testes e repetir a análise Sonar. Definir com o PO as métricas e metas do modelo antes de comparar versões ou reivindicar qualidade clínica.
5. **Painel gerencial:** apresentar somente dados coletados e datados; identificar claramente N/D, fonte simulada ou análise desatualizada. Manter os links para os projetos Sonar e para os relatórios de teste de cada release.

## 6. Referências e histórico

- [Projeto APP no SonarCloud — branch develop](https://sonarcloud.io/project/overview?id=fga-eps-mds_2026.2-UNB-FCTE_UNIEURO_MED-APP&branch=develop). Consulta em 26/09/2026.
- [Projeto IA no SonarCloud — branch develop](https://sonarcloud.io/project/overview?id=fga-eps-mds_2026.2-UNB-FCTE_UNIEURO_MED-IA&branch=develop). Consulta em 26/09/2026.
- [Cronograma do MED](cronograma.md) — metas de cobertura e marcos de release.
- [Metodologia do MED](metodologia.md) — critérios de conclusão, PRs e ciclo de inspeção.

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
|---|---|---|---|---|
| 1.0 | 26/09/2026 | Criação do plano com linha de base do SonarCloud, critérios de teste e ações para APP e IA | Equipe MED (proposta para revisão) | Pendente |
