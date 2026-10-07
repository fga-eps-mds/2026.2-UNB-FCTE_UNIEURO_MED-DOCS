# Plano de Gerenciamento da Qualidade — MED 2026.2

> Versão 2.0, levantamento de 28/09/2026. Este plano combina critérios de qualidade com a situação observada da R1. Métricas, testes automatizados, aceite funcional e qualidade clínica são evidências distintas; uma não substitui a outra. A revisão e aprovação pela equipe ainda estão pendentes.

## 1. Objetivo, escopo e princípios

A equipe acompanha a qualidade do aplicativo Android (APP), do módulo de inteligência artificial (IA), da integração entre ambos e das evidências publicadas no repositório DOCS. Para o software em desenvolvimento, a referência é a branch de integração develop; para uma release, é o commit da tag publicado em main. Toda medição deve indicar repositório, branch ou tag, commit, data da análise, valor e link para a execução ou relatório.

O aplicativo e a inferência devem funcionar integralmente sem internet. Dados de atendimento, imagens, traçados e resultados não devem sair do tablet automaticamente, e o paciente não deve ver o escore. As restrições estão na [Visão do Produto](../produto/visao.md), na [Arquitetura](../produto/arquitetura.md) e nas histórias de usuário. Um gate verde do SonarCloud indica conformidade com regras de análise do código presente; não atesta execução no tablet, aceite da história ou validade clínica.

As metas acadêmicas do [Cronograma](cronograma.md) são: cobertura de testes unitários de pelo menos **85% na R1**, pelo menos **85% com testes de integração na R2** e pelo menos **90% na R3**. Este plano mede cada repositório com código de produto testável separadamente. Não se faz média de APP e IA, nem se considera uma métrica ausente como zero ou como meta cumprida. As regras operacionais adicionais abaixo são propostas de controle para revisão da equipe.

## 2. Linha de base verificada em 28/09/2026

| Evidência | APP | IA |
|---|---|---|
| Branch de integração consultada | develop, commit 53a8833 | develop, commit da9f7fb |
| Release R1 | [v1.0.0](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/releases/tag/v1.0.0), main no commit 8c61a76 | [v1.0.0](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-IA/releases/tag/v1.0.0); ainda sem artefato de modelo |
| Última análise de develop exibida no SonarCloud | 28/09, 03h29 UTC | 28/09, 04h09 UTC |
| Linhas analisadas (NCLOC) | 1.370 | Não publicada após a exclusão de arquivos auxiliares |
| Cobertura total publicada | **96,0%** | **Não publicada** |
| Duplicação total | 2,2% | Não publicada |
| Code smells | 12 | 0 reportados |
| Bugs / vulnerabilidades reportados | 0 / 0 | 0 / 0 |
| Quality gate de develop | **Aprovado**; cobertura nova 96,0% e duplicação nova 1,2% | **Aprovado**, sem condição de cobertura avaliada |
| CI mais recente da integração | [Build de develop aprovado](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/actions/runs/36374433461) | [Build de develop aprovado](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-IA/actions/runs/36376520477) |

Fontes: [SonarCloud APP/develop](https://sonarcloud.io/project/overview?id=fga-eps-mds_2026.2-UNB-FCTE_UNIEURO_MED-APP&branch=develop), [SonarCloud APP/main](https://sonarcloud.io/project/overview?id=fga-eps-mds_2026.2-UNB-FCTE_UNIEURO_MED-APP&branch=main) e [SonarCloud IA/develop](https://sonarcloud.io/project/overview?id=fga-eps-mds_2026.2-UNB-FCTE_UNIEURO_MED-IA&branch=develop). A análise de APP/main da R1 ocorreu em 28/09, 04h39 UTC e também mostrou **96,0% de cobertura e gate aprovado**. A análise do Sonar pode não expor o SHA na consulta pública; os commits acima identificam as branches verificadas no GitHub, e a correspondência exata com cada análise deve ser registrada no pipeline.

### 2.1 O que mudou no APP

Os [PRs #31 (testes)](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/pull/31), [#36 (cadastro e login locais)](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/pull/36) e [#26 (release e métricas)](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/pull/26) foram incorporados a develop; o [PR #37](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/pull/37) levou develop à main para a R1. Há código de SQLite, migração, repositório de profissionais, validação de cadastro, hash PBKDF2-SHA256 com sal, verificação de senha, telas de acesso e menu. Há testes Jest para banco, repositório, senha, cadastro, login, estilos e tema.

O workflow de Build executa instalação limpa, testes com cobertura e análise Sonar. O Jest exige no mínimo 90% de linhas, instruções e funções e 80% de ramos. A cobertura publicada pelo Sonar é **96,0% no código incluído no cálculo**; rotas que apenas reexportam telas e variantes web não embarcadas estão excluídas. A exclusão precisa permanecer documentada e não deve esconder lógica de produto. O gate da release em main está aprovado, mas a [release v1.0.0 do APP](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/releases/tag/v1.0.0) anexa código/testes compactados e JSON de métricas, **não um APK**.

### 2.2 O que mudou na IA

O pipeline de release e exportação de métricas entrou em develop pelo [PR #11](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-IA/pull/11). O [PR #12](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-IA/pull/12) excluiu workflows e script de métricas da análise do Sonar. A branch de integração ainda não contém código de treino, inferência, testes de modelo ou artefato embarcável. Os resultados do primeiro treino permanecem no [PR #10](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-IA/pull/10), em revisão.

Por isso, o gate verde da IA é registrado como **configuração de análise aprovada, produto de IA ainda não mensurável**. Não se atribui 0% de cobertura, nem se declara a meta de cobertura cumprida. A release v1.0.0 sem artefato de modelo não demonstra inferência local nem desempenho clínico.

### 2.3 Evidência do painel gerencial

O [dashboard gerencial](https://2026-2-unb-fcte-unieuro-med-docs.streamlit.app) e a [coleta de métricas](../metricas/coleta-de-metricas.md) estão publicados. A aba de qualidade lê arquivos JSON versionados; os arquivos agregados Sonar de APP e IA presentes em analytics-raw-data foram coletados em **21/09**. Eles são anteriores à medição acima e não substituem a consulta atual à branch da release. O painel deve exibir data, origem, branch e indicação de dado ausente ou simulado antes de ser usado como evidência da R1.

## 3. Critérios de qualidade e aceitação

| Eixo | Condição de aceite proposta | Evidência exigida |
|---|---|---|
| Código e CI | Build e testes pertinentes aprovados no commit da release; gate Sonar aprovado na branch/tag analisada | Link do workflow, SHA, relatório de testes, LCOV e análise Sonar |
| Cobertura | Metas do cronograma por repositório com código testável; informar denominador e exclusões | Percentual total e novo, arquivos excluídos, data e branch |
| Segurança | Nenhuma vulnerabilidade crítica/alta ou defeito bloqueador conhecido sem decisão registrada; senha nunca armazenada em texto simples | Análise, inspeção da persistência, teste e issue de tratamento |
| Histórias de usuário | Todos os critérios aplicáveis ao incremento demonstrado passam no tablet-alvo sem internet | Roteiro preenchido, resultado observado, APK/commit, dispositivo e responsável |
| Dados locais | Dados persistem conforme o requisito e não são enviados automaticamente; acesso não autorizado é bloqueado | Teste de reabertura, modo avião, inspeção de fluxo/rede e comportamento de sessão |
| IA | Modelo reproduzível, exportado, integrado e testado offline; métricas e limitações registradas | Código e versão de dados, parâmetros, resultados por execução, artefato e teste no tablet |
| Processo e dashboard | Métricas com fonte, data, branch e interpretação; dados simulados e ausentes identificados | JSON, execução da coleta, link do painel e revisão de consistência |

A equipe deve manter **100% dos cenários críticos planejados para o incremento aprovado** e nenhum defeito bloqueador aberto antes de declarar uma história aceita. Trata-se de critério operacional proposto; caso haja exceção, registrar causa, impacto, responsável e aceite explícito. Cenário não executado permanece pendente. Zero bugs reportados pelo Sonar não significa ausência de defeitos funcionais.

### 3.1 R1: cadastro e login no tablet

As [US #5 (cadastro)](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/5) e [#6 (login)](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/6) foram fechadas no GitHub após a integração do código. Isso não substitui a demonstração dos critérios de aceitação. O [roadmap](roadmap.md) ainda registra a R1 como interfaces navegáveis e remete o aceite completo das USs à R2; a equipe deve atualizar esse registro conforme o resultado do teste real.

| Cenário crítico | Resultado esperado | Situação pública em 28/09 |
|---|---|---|
| Cadastrar profissional sem internet | Conta local criada; login possível após fechar e reabrir o app | Implementação e testes automatizados integrados; falta evidência pública do teste no tablet |
| Campos inválidos, CPF/CRM incorretos e duplicados | Cadastro rejeitado, mensagem compreensível e nenhum registro indevido | Casos automatizados presentes; confirmar comportamento no dispositivo |
| Senha e dados de acesso | Hash com sal no SQLite, sem senha em texto simples; credenciais erradas não abrem o menu | Código e testes integrados; inspecionar banco e fluxo no tablet |
| Login válido e inválido | Válido leva ao menu; inválido não revela se e-mail está cadastrado e não concede acesso | Código e testes integrados; falta demonstração observada no tablet |
| Acesso às telas profissionais | Rotas protegidas também após reabrir o app ou navegar diretamente | Não há evidência pública de teste de sessão e bloqueio de rotas |
| Fluxo do paciente e retorno ao médico | Paciente não faz login nem vê escore; retorno exige confirmação do médico | Critérios da US #6 ligados ao fluxo de avaliação; ainda não demonstráveis integralmente na R1 |

O roteiro de execução deve registrar: versão e SHA do APK, modelo e sistema do tablet, rede desativada, dados de teste não reais, passos, resultado esperado, resultado observado, captura ou vídeo sem dados sensíveis, defeito/issue, executor e data. A release no GitHub contém fontes e métricas, mas não um APK; informar separadamente onde está o artefato instalável usado na demonstração.

### 3.2 R2 e R3: qualidade por incremento

Na **R2**, acrescentar testes de integração de atendimento, TCLE, persistência, primeiro desenho, proteção dos dados e interação entre APP e IA conforme o escopo aprovado. A meta é pelo menos 85% de cobertura com testes de integração, além de validação offline no tablet. O modelo preliminar só é aceito se houver código, artefato exportado e teste de entrada/saída versionados.

Na **R3**, exigir pelo menos 90% de cobertura e testes unitários, de integração, de sistema e de interface conforme o cronograma. Verificar as três tarefas, captura e retomada, inferência embarcada, resultados restritos ao profissional, ausência de escore na tela do paciente e XML local quando solicitado. Casos com dados de saúde devem usar material de teste autorizado e não devem ser versionados. Metas de desempenho clínico do modelo precisam ser acordadas com o PO antes da avaliação; **este plano não inventa um limiar clínico**.

### 3.3 Reprodutibilidade e proteção dos dados da IA

Cada experimento deve registrar versão e origem permitida dos dados, separação treino/validação/teste, semente, parâmetros, versão do código, métricas por execução, resumo estatístico, limitações e artefato exportado. O resultado do melhor treino isolado não deve ser apresentado como média de execuções nem como validação clínica. Antes da integração, verificar compatibilidade de formato e tempo de inferência no tablet em modo avião.

O APP já usa hash de senha, mas isso **não equivale à cifra do banco inteiro** nem demonstra proteção de dados clínicos futuros. A revisão deve cobrir chaves, armazenamento local, descarte e exportação autorizada; acompanhar os riscos [R10, R13 e R14](riscos.md).

## 4. Ciclo de medição, decisão e tratamento de desvios

| Momento | Quem verifica | Registro mínimo |
|---|---|---|
| Em cada PR | Autor e revisor | Issue vinculada, teste alterado, comandos/resultados, análise estática e riscos da mudança |
| Após merge em develop | Qualidade/DevOps | SHA, workflow, cobertura/gate, diferenças de métrica e falhas abertas |
| Antes da release em main | Liderança, Qualidade e PO quando aplicável | Tag/commit, artefato instalável, teste no tablet, critérios das USs, exceções e decisão de aceite |
| Após a release | Equipe | Defeitos, regressões, indicadores atualizados, causa e ação com responsável/prazo |

Para resultado abaixo da meta: registrar a medição e sua origem; abrir ou atualizar issue de desvio; atribuir responsável e prazo; corrigir e repetir o teste; se a entrega prosseguir com exceção, documentar risco e decisão. Não alterar exclusões de cobertura apenas para atingir o percentual sem justificativa técnica. O dashboard deve distinguir resultado da branch de integração, resultado da release e dado histórico.

## 5. Ações de qualidade imediatas

1. **Registrar a prova funcional da R1:** executar a matriz de cadastro/login no tablet em modo avião, com APK identificável e resultados observados. Manter pendentes os critérios da US #6 que dependem do fluxo do paciente.
2. **Consolidar a medição de APP:** anexar ao registro da R1 o [Build de main aprovado](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/actions/runs/36378600379), o LCOV, o Sonar de main (96,0%) e as exclusões de cobertura. Triar os 12 code smells e eventuais defeitos funcionais; não confundir gate aprovado com aceite completo.
3. **Disponibilizar o APK de demonstração:** indicar link, SHA e dispositivo usado. O ZIP da release v1.0.0 contém fonte e testes, não o aplicativo instalável.
4. **Construir a evidência de IA:** revisar o PR #10, versionar código/artefato de modelo e testes; medir cobertura e desempenho só quando houver código de produto analisável. Manter o gate atual como evidência de configuração, não de modelo.
5. **Atualizar as fontes gerenciais:** executar a coleta após os merges, registrar branch/commit/análise em cada JSON, atualizar o painel e corrigir páginas que ainda mostram a situação de 26/09 como atual.
6. **Alinhar o roadmap ao aceite real:** descrever o que foi demonstrado na R1 e manter o restante das USs #5/#6 como pendência se não houver prova no tablet.

## 6. Referências e histórico

- [Cronograma](cronograma.md), [Metodologia](metodologia.md), [Roadmap](roadmap.md) e [Coleta de métricas](../metricas/coleta-de-metricas.md).
- [APP: pipeline de Build](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/blob/develop/.github/workflows/build.yml), [IA: pipeline de Build](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-IA/blob/develop/.github/workflows/build.yml).
- [SonarCloud APP/develop](https://sonarcloud.io/project/overview?id=fga-eps-mds_2026.2-UNB-FCTE_UNIEURO_MED-APP&branch=develop) e [SonarCloud IA/develop](https://sonarcloud.io/project/overview?id=fga-eps-mds_2026.2-UNB-FCTE_UNIEURO_MED-IA&branch=develop). Consulta em 28/09/2026.

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
|---|---|---|---|---|
| 1.0 | 26/09/2026 | Criação do plano com linha de base do SonarCloud, critérios de teste e ações para APP e IA | Equipe MED (proposta para revisão) | Pendente |
| 1.1 | 27/09/2026 | Alinhamento ao roadmap, à coleta automatizada e ao plano de riscos incorporados à main | Equipe MED (proposta para revisão) | Pendente |
| 2.0 | 28/09/2026 | Nova linha de base após integração de cadastro, testes e releases; critérios de aceite por incremento e limites da análise de IA | Proposta para revisão da equipe | Pendente |
