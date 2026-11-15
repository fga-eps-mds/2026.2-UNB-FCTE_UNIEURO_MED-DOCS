# Plano de Comunicação

## Objetivo

Este plano registra como a equipe se comunica entre si, com o *Product Owner* (PO), com o cliente e com o professor: quem recebe cada informação, por qual canal, com que frequência e quem é o responsável. Ele descreve a prática que a equipe já segue e complementa a seção de [gestão visual e comunicação da metodologia](metodologia.md#6-gestao-visual-e-comunicacao), que lista os canais e onde cada decisão fica registrada.

## Partes interessadas

| Parte interessada | O que precisa saber | Canal | Frequência | Responsável |
| :--- | :--- | :--- | :--- | :--- |
| PO (Vinícius de Carvalho Rispoli) | Histórias a validar, incremento entregue, dúvidas de produto e pendências de aceite | Reunião no Microsoft Teams, Discord e WhatsApp para lembretes | Semanal e sempre que houver história nova | Dupla de liderança |
| Cliente (Arthur Dutra do Bomfim) | Histórias a validar, APK para teste e decisões que afetam o uso do tablet | Reunião no Microsoft Teams e Discord | Semanal e a cada APK gerado | Dupla de liderança |
| Professor | Andamento do projeto, entregas das releases e decisões gerenciais | Reuniões de avaliação, repositório DOCS e Aprender 3 | A cada release | Dupla de liderança |
| Equipe | Divisão das tarefas, andamento, impedimentos e combinados | WhatsApp, GitHub e Zenhub | Contínua | Todos os integrantes |

A dupla de liderança muda a cada duas semanas, conforme a [escala de lideranças](../equipe/operacional.md#escala-de-liderancas).

## Agenda de trabalho

### Rotina semanal

| Quando | Atividade | Participantes | Canal | Responsável | Registro |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Antes da reunião | Montar a pauta com as histórias que serão discutidas | Dupla de liderança | WhatsApp | Dupla de liderança | Lista de issues na pauta |
| Segunda-feira, 19h30 às 20h30 | Reunião semanal com o PO e o cliente | Equipe, PO e cliente | Microsoft Teams | Dupla de liderança | [Ata da reunião](../atas-reunioes/index.md) |
| Após a reunião | Envio da ata ao PO e ao cliente | Dupla de liderança | Discord | Dupla de liderança | Ata publicada no DOCS |
| Durante a semana | Envio das histórias para validação, com contexto e critérios de aceitação | Equipe, PO e cliente | Discord, com lembrete por WhatsApp ao PO | Dupla de liderança | Comentário na issue |
| A cada incremento | Geração do APK para o PO e o cliente testarem | Equipe, PO e cliente | Discord | Dupla de liderança | Erro relatado vira issue |
| Contínuo | Divisão das tarefas, andamento e impedimentos | Equipe | WhatsApp, GitHub e Zenhub | Responsável de cada issue | Issue atualizada no Zenhub |

Decisões tomadas no WhatsApp que mudam escopo, prioridade, prazo ou responsável são registradas na issue correspondente, como manda a [metodologia](metodologia.md#62-canais-e-registro).

### Prazos das releases

| Data | Marco | O que é comunicado |
| :---: | :--- | :--- |
| 09/11/2026 | Validação prévia das histórias da R3 ([Ata 12](../atas-reunioes/Ata-12-EPS-2026-11-09-PO.md)) | Histórias da R3 apresentadas ao PO e ao cliente na reunião semanal; o restante enviado pelo Discord |
| 30/11/2026 | R3, marco do MVP | Demonstração ao professor, ao PO e ao cliente; APK da release |
| 07/12/2026 | Release final (RF) | Versão estabilizada e APK final |
| 14/12/2026 | Encerramento do projeto | Entrega do APK e dos artefatos da disciplina; devolução dos tablets ao cliente (proposta) |

As datas seguem o [cronograma](cronograma.md).

## Uso dos tablets

Os tablets do cliente ficam com a equipe para os testes do aplicativo no dispositivo real até o último dia da disciplina, **14/12/2026**, quando são devolvidos ao cliente.

!!! warning "Pendente de confirmação"
    Esse prazo é a proposta da equipe e ainda precisa ser confirmado com o PO e o cliente na reunião semanal. O combinado deve ser registrado na ata da reunião em que for confirmado.

## Reunião semanal

A dupla de liderança conduz a reunião: abre a pauta, apresenta as histórias que precisam de validação e registra as decisões para a ata.

A reunião é aberta. Qualquer integrante pode abrir o microfone a qualquer momento para tirar dúvidas, complementar uma explicação ou levantar um problema. A equipe não adota um rodízio fixo de fala, porque a reunião é dinâmica e a pauta muda conforme as respostas do PO e do cliente; obrigar cada integrante a falar tomaria o tempo da reunião sem trazer informação nova. A participação de cada um aparece nas histórias que leva à pauta, nas dúvidas registradas na ata e no trabalho rastreado nas issues e nos PRs.

As histórias já implementadas não são demonstradas uma a uma na reunião, para que ela não se estenda. Em vez disso, a equipe gera o APK, o PO e o cliente o testam no tablet e informam os erros encontrados, que viram issues.

## Validação e aceite

1. A equipe envia as histórias ao PO e ao cliente, com contexto, critérios de aceitação e protótipo, pela reunião semanal ou pelo Discord.
2. O PO e o cliente testam o APK e respondem ao formulário de aceite.
3. Se o PO não responder, a dupla de liderança envia um lembrete por WhatsApp, canal que ele usa no dia a dia.
4. Sem resposta, a equipe segue o desenvolvimento normalmente, sem esperar o aceite formal. Ajustes pedidos depois pelo PO ou pelo cliente entram como correção. Essa regra foi combinada com o PO na [Ata 12](../atas-reunioes/Ata-12-EPS-2026-11-09-PO.md) e é a contingência do risco R06 no [plano de riscos](riscos.md#riscos-concretizados).

## Histórico de versões

| Versão | Descrição | Autor | Data | Revisor | Data de revisão |
|---|---|---|---|---|---|
| 1.0 | Criação do plano de comunicação, com partes interessadas, agenda semanal, prazos das releases, uso dos tablets, condução da reunião e fluxo de validação e aceite | [Daniel Ferreira Nunes](https://github.com/Mach1r0) | 15/11/2026 | A definir | — |
