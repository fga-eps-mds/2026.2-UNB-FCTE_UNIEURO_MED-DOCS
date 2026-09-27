

# Roadmap do Produto — 2026.2

O roadmap relaciona os marcos da disciplina ao incremento que a equipe consegue demonstrar. As ondas do [sequenciador](../produto/sequenciador.md) indicam prioridade, não equivalem às sprints. As entregas abaixo distinguem o que já existe na branch de integração do APP dos objetivos das próximas releases, que dependem de implementação, testes e validação.

O quadro do Miro registra o planejamento visual original; **a tabela de sta página é a referência atual para o escopo das releases**.

<div class="roadmap-visual" markdown>

<iframe
  src="https://miro.com/app/live-embed/uXjVHn_328k=/?embedMode=view_only_without_ui&moveToViewport=-1511%2C5577%2C9007%2C3675&embedId=567016492009"
  title="Roadmap do produto MED no Miro"
  loading="lazy"
  frameborder="0"
  scrolling="no"
  allow="fullscreen; clipboard-read; clipboard-write"
  allowfullscreen>
</iframe>

</div>

## Marcos oficiais

| Data | Marco | Resultado demonstrável / situação |
|---|---|---|
| **10/08** | Início do projeto | Lean Inception e preparação técnica. |
| **28/09** | **R1 — interfaces de acesso** | Telas de cadastro e login navegáveis; o cadastro avisa sobre campos vazios e senhas divergentes. **Cadastro persistente e autenticação não integram a entrega confirmada.** |
| **26/10** | **R2 — acesso local e primeira avaliação (objetivo)** | Cadastro e login offline, atendimento e TCLE registrados, dados protegidos e primeiro desenho demonstrado localmente, se as dependências forem concluídas. O desenho isolado é avanço parcial das USs das três tarefas, não seu aceite. |
| **30/11** | **R3 — marco do MVP (objetivo)** | Três tarefas, captura e retomada, inferência e resultados locais, exportação XML sob solicitação; tudo condicionado à integração, à validação no tablet e às decisões do parceiro. Escopo não concluído deve ser registrado como desvio. |
| **07/12** | **Release final** | Correções e estabilização do incremento validado; acessibilidade priorizada conforme capacidade. |
| **14/12** | Encerramento | APK, documentação, resultados e limitações efetivamente alcançados. |

!!! warning "Situação da R1 em 26/09/2026"
    Na branch de integração do APP, há telas de acesso e validações básicas do
    formulário de cadastro. O botão de login ainda informa que a funcionalidade
    será conectada depois. A persistência do cadastro está em uma branch de
    trabalho, após o [PR APP #34](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/pull/34),
    e os testes estão no [PR APP #31](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/pull/31).
    Sua integração e a demonstração no tablet ainda precisam ser verificadas.
    Portanto, esta R1 não comprova as histórias de [cadastro local](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/5)
    e [login](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/6) como concluídas.

## Planejamento detalhado

As datas oficiais permanecem. Uma funcionalidade só passa de objetivo para entrega confirmada quando está integrada à branch correta, seus critérios de aceitação foram testados e existe evidência de demonstração. Os objetivos de R2 e R3 serão revistos ao fim de cada release, conforme capacidade e dependências reais.

### Rastreabilidade das histórias de usuário até o MVP

Esta distribuição relaciona as **18 USs do backlog do APP** às releases. A R1 ainda não concluiu nenhuma US: suas telas são apenas parte das histórias de cadastro e login. Cada US aparece na release em que **todos** os seus critérios de aceitação devem ser verificados; trabalho parcial em uma release anterior não significa história pronta. R2 e R3 são metas, não funcionalidades já entregues.

| Release-alvo | US do APP | Resultado necessário para aceitar a história |
|---|---|---|
| **R2** | [#5 — Cadastro do médico](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/5) | Conta persistida localmente, com validação e senha protegida. |
| **R2** | [#6 — Login do médico](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/6) | Autenticação offline e recusa de credenciais inválidas. |
| **R2** | [#7 — Registro do atendimento](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/7) | Atendimento vinculado ao profissional, data/hora e campos aprovados, inclusive escolaridade quando exigida. |
| **R2** | [#21 — Aceite do TCLE](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/21) | Termo aprovado, decisão e horário registrados; sem aceite, nenhuma coleta de desenho. |
| **R3** | [#8 — Instrução simples por desenho](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/8) | Instrução legível e aprovada antes de cada uma das três tarefas. |
| **R3** | [#9 — Três tarefas de desenho](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/9) | Relógio, pentágono e cubo na ordem aprovada pelo parceiro, com traço responsivo e sem escore ao paciente. |
| **R3** | [#10 — Captura do traçado e da imagem](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/10) | Traçado temporal e imagem fiel de cada tarefa vinculados ao atendimento. |
| **R3** | [#11 — Tela final do paciente sem escore](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/11) | Agradecimento sem nota; resultado protegido para acesso do profissional. |
| **R3** | [#12 — Escore por desenho no tablet](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/12) | Pontuação reproduzível dos três desenhos com modelo embarcado e sem rede. |
| **R3** | [#13 — Escore geral e incerteza](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/13) | Resultado geral com faixa e aviso de incerteza alta conforme regras validadas. |
| **R3** | [#14 — Desenho, escore e explicação](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/14) | Desenhos, escores e características explicativas em linguagem clínica, apenas ao profissional; depende do modelo e do parceiro. |
| **R3** | [#15 — Uso completo sem internet](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/15) | Fluxo inteiro, do login ao resultado, testado em modo avião. |
| **R3** | [#16 — Nenhum dado enviado para fora do tablet](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/16) | Sem chamadas de rede no fluxo; XML da #22 gerado somente sob comando, sem envio automático. |
| **R3** | [#17 — Dados cifrados no tablet](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/17) | Proteção iniciada antes da coleta na R2; aceite completo na R3, com atendimentos, desenhos e resultados ilegíveis fora do aplicativo e chave separada dos dados. |
| **R3** | [#22 — Exportar avaliação em XML](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/22) | Arquivo gerado localmente, validado contra esquema aprovado e sem transmissão automática. |
| **R3** | [#23 — Confirmar ou refazer desenho](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/23) | Desfazer, limpar e confirmar cada tarefa sem pontuar traços descartados. |
| **R3** | [#25 — Salvar e retomar avaliação](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/25) | Progresso salvo, retomada após interrupção e consulta local às avaliações do profissional. |
| **Após o MVP** | [#24 — Configurar contraste e fonte](https://github.com/fga-eps-mds/2026.2-UNB-FCTE_UNIEURO_MED-APP/issues/24) | Ajustes configuráveis nas três tarefas; candidata à release final, sem dispensar a legibilidade padrão da #8. |


### Execução por sprint

| Etapa | Período | Release | Entrega delimitada | Condição para considerar concluída |
|---|---|---|---|---|
| Preparação | 10/08–30/08 | — | Visão do Produto, sequenciador, arquitetura inicial e base dos repositórios. | Artefatos publicados e ambiente de desenvolvimento disponível. |
| **Sprint 1 — telas de acesso** | 31/08–13/09 | R1 | Estrutura do app, navegação e telas de cadastro e login. | Telas presentes na branch de integração do APP. |
| **Sprint 2 — demonstração da R1** | 14/09–27/09 | **R1 · 28/09** | Navegação entre as telas e avisos de campos obrigatórios e senhas divergentes no cadastro. | Demonstrar as interfaces no aplicativo; registrar que criar conta e entrar ainda não foram validados como fluxo funcional. |
| **Sprint 3 — acesso local funcional** | 29/09–11/10 | R2 | Integrar cadastro e login locais (#5 e #6), registro do atendimento (#7) e iniciar a proteção dos dados (#17). | Conta persiste, credenciais são verificadas offline e dados coletados ficam protegidos; o aceite integral da #17 permanece na R3, após incluir os resultados. |
| **Sprint 4 — consentimento e primeiro desenho** | 12/10–25/10 | **R2 · 26/10** | Registrar TCLE (#21) e demonstrar a primeira tarefa com salvamento local; este desenho inicia, mas não conclui, as USs #8, #9, #10, #23 e #25. | TCLE aprovado e testado; fluxo demonstrado no tablet após o acesso funcional. O aceite das USs das três tarefas permanece na R3. |
| **Sprints 5–7 — integração do MVP** | 27/10–29/11 | **R3 · 30/11** | Concluir as USs R3 da tabela: três tarefas, captura, retomada, resultados e inferência offline, controles do desenho e XML local. | Modelo exportado e integrado, critérios de todas as USs R3 testados no tablet e decisões do PO registradas. Itens não verificados permanecem pendentes, mesmo na data da R3. |
| **Sprint 8 — estabilização** | 01/12–06/12 | **RF · 07/12** | Corrigir defeitos do incremento entregue e aplicar melhorias de acessibilidade que caibam sem regressão. | APK e documentação revisados; alterações adicionais demonstradas e aceitas. |
| Encerramento | 08/12–14/12 | Pós-RF | Consolidar evidências, limitações, resultados e trabalhos futuros. | Entrega final corresponde ao software efetivamente testado. |

## Relação entre ondas, sprints e releases

- O sequenciador define prioridade; este roadmap define o recorte demonstrável por release.
- A R1 confirma apenas as interfaces de acesso que já estão integradas. Cadastro e login funcionais dependem de implementação e teste e foram deslocados para o objetivo da R2.
- R2 e R3 são **objetivos de planejamento**, não declarações de funcionalidade pronta. Mudanças no escopo ou nas datas exigem registro na issue/ata e atualização do cronograma.
- A R3 continua sendo o marco acadêmico do MVP; se o fluxo completo não estiver pronto, a equipe deve apresentar o incremento real e o desvio, sem declarar o MVP concluído.

## Histórico de versão

| Data | Versão | Descrição | Autor |
|---|---:|---|---|
| 13/09/2026 | 1.0 | Criação do roadmap a partir do cronograma oficial da disciplina. | Equipe MED |
| 25/09/2026 | 1.1 | Redução do escopo da R1 para cadastro e login e replanejamento do primeiro fluxo de avaliação para a R2. | Equipe MED |
| 26/09/2026 | 1.2 | Ajuste da R1 ao que está integrado no APP e explicitação das dependências dos objetivos de R2 e R3. | Equipe MED (proposta para revisão) |
| 26/09/2026 | 1.3 | Mapeamento das 18 USs do backlog para R2, R3 e pós-MVP, com critérios e divergências de escopo explicitados. | Equipe MED (proposta para revisão) |

