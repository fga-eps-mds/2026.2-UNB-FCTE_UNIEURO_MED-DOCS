# Visão do Produto — MED

Esta página é a síntese da Visão do Produto. O detalhamento completo, produzido nas dinâmicas de Lean Inception, está distribuído nas páginas listadas em [Documentos da Visão do Produto](#documentos-da-visao-do-produto), no fim deste documento. Todo esse conjunto é a Visão do Produto do MED.

## Problema

O rastreio cognitivo de idosos hoje é aplicado em papel e pontuado à mão. Isso consome tempo de consulta, varia de avaliador para avaliador, não gera registro comparável ao longo do tempo e carece de simplicidade, tanto para o médico aplicar quanto para o paciente idoso responder.

As alternativas existentes (testes em papel, ou plataformas digitais como DCTclock/Linus Health) não resolvem isso: dependem de hardware proprietário, exigem nuvem, foram validadas em população norte-americana e não têm versão em português, não considerando, portanto, a variação de escolaridade da população brasileira.

O perfil, o comportamento e as necessidades de cada usuário estão detalhados em [Lean Inception — Personas](lean-inception.md#4-personas).

## Objetivo do semestre

Como este é um produto novo, o objetivo do semestre é entregar a primeira versão funcional (MVP) do app, incluindo:

- APK Android funcional, rodando localmente no tablet, 100% offline.
- Modelo de IA embarcado no aplicativo (sem chamadas externas/nuvem).
- As 3 tarefas de desenho implementadas, apresentadas em sequência com instruções simples.
- Captura do traçado e da imagem final de cada desenho.
- Cálculo do escore por teste e do escore geral, com indicação de incerteza/faixa de desempenho.
- Cadastro e login do médico (sem login para o paciente).
- Registro de quem aplicou o teste, em que condições, vinculado ao atendimento.
- Tela de resultado para o médico mostrando desenho + escore + quais características influenciaram o score.
- Tela final para o paciente sem exibir o score (agradecimento apenas).
- Nenhum dado enviado a servidor externo.

O objetivo será considerado cumprido se cada item acima puder ser demonstrado rodando no tablet, com um médico completando o fluxo real de ponta a ponta (login → aplicação → resultado).

## Público-alvo

| Perfil | Necessidade | Como o produto atende |
|---|---|---|
| Paciente idoso | Fazer o teste sem se sentir diminuído ou "reprovado", de forma simples e sem ajuda | Tarefas de desenho, sem exibir score ao paciente, sem exigir login |
| Médico generalista/geriatra | Aplicar em poucos minutos e confiar no resultado | Escore objetivo e reprodutível, exibido junto do desenho e da faixa de incerteza |

Os perfis completos estão em [Lean Inception — Personas](lean-inception.md#4-personas).

## Proposta de valor

Diferente de testes tradicionais em papel e de plataformas digitais como DCTclock/Linus Health, que dependem de hardware proprietário, exigem nuvem e foram validadas apenas em população norte-americana. O produto roda em tablet Android comum, funciona 100% offline mantendo os dados na instituição, e é validado sobre a população brasileira, considerando a variação de escolaridade.

## Escopo

### Dentro do escopo
- Aplicativo Android (APK), rodando localmente no tablet, 100% offline, com modelo de IA embarcado.
- Ferramenta de rastreio/triagem cognitiva, como apoio à decisão do profissional (não substitui avaliação médica).
- 3 testes de desenho, com cálculo de escore por teste e escore geral (com faixa de incerteza).
- Cadastro/login do médico e registro de quem aplicou o teste.

### Fora do escopo
- Diagnóstico, prescrição, conduta clínica ou integração com prontuário eletrônico.
- Versão Web, multiplataforma ou publicação em loja de aplicativos.
- Acompanhamento longitudinal e envio de dados a servidor externo.

A lista completa de É / Não É e Faz / Não Faz está em [Lean Inception](lean-inception.md#2-e-nao-e-faz-nao-faz).


## Documentos da Visão do Produto

A Visão do Produto do MED não cabe em uma página só. Esta é a síntese, e as páginas abaixo carregam o detalhamento por atividade da Lean Inception. Todas fazem parte do mesmo documento.

| Página | Conteúdo | Atividades |
|---|---|---|
| [Lean Inception](lean-inception.md) | Declaração de visão, É / Não É e Faz / Não Faz, objetivos de negócio, personas e jornadas de usuário | 1 a 5 |
| [Funcionalidades](funcionalidades.md) | Brainstorming de funcionalidades, clusters e revisão técnica, de negócio e de UX | 6 e 7 |
| [Sequenciador](sequenciador.md) | Ondas do MVP e dos incrementos | 8 |
| [Canvas MVP](canvas-mvp.md) | Proposta do MVP, hipóteses, métricas de validação e custo estimado | 10 |

## Histórico de versões

| Versão | Descrição | Autor(es) | Data | Revisor(es) | Data de Revisão |
|---|---|---|---|---|---|
| 1.0 | Criação do documento: Declaração de Visão, É/Não É, Objetivos, Personas e Jornadas de Usuário | [Artur Mendonça Arruda](https://github.com/ArtyMend07) | 03/09/2026 | [Lucas Mendonça Arruda](https://github.com/lucasarruda9), [Gabriel Lopes de Amorim](https://github.com/BrzGab) | |
| 2.0 | Reestruturação do documento no formato Problema/Objetivo do semestre/Público-alvo/Proposta de valor/Escopo, sintetizando o conteúdo da Lean Inception (v1.0) | [Eduardo Ferreira](https://github.com/eduardoferre) | 05/09/2026| | |
| 2.1 | Restabelecimento da rastreabilidade da síntese com as páginas de detalhamento, substituindo as referências em texto por links, e registro das demais páginas que compõem a Visão do Produto | [Artur Mendonça Arruda](https://github.com/ArtyMend07) | 18/09/2026 | | |
