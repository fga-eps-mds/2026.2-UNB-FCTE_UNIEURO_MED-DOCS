# Visão do Produto — MED

## Problema

O rastreio cognitivo de idosos hoje é aplicado em papel e pontuado à mão. Isso consome tempo de consulta, varia de avaliador para avaliador, não gera registro comparável ao longo do tempo e carece de simplicidade, tanto para o médico aplicar quanto para o paciente idoso responder.

As alternativas existentes (testes em papel, ou plataformas digitais como DCTclock/Linus Health) não resolvem isso: dependem de hardware proprietário, exigem nuvem, foram validadas em população norte-americana e não têm versão em português, não considerando, portanto, a variação de escolaridade da população brasileira.

*(detalhamento de perfil e comportamento dos usuários na página de Lean Inception → Personas)*

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

*(perfis detalhados na página de Lean Inception → Personas)*

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

*(lista completa de É/Não É e Faz/Não Faz na página de Lean Inception)*


## Histórico de versões

| Versão | Descrição | Autor(es) | Data | Revisor(es) | Data de Revisão |
|---|---|---|---|---|---|
| 1.0 | Criação do documento: Declaração de Visão, É/Não É, Objetivos, Personas e Jornadas de Usuário | [Artur Mendonça Arruda](https://github.com/ArtyMend07) | 03/09/2026 | [Lucas Mendonça Arruda](https://github.com/lucasarruda9), [Gabriel Lopes de Amorim](https://github.com/BrzGab) | |
| 2.0 | Reestruturação do documento no formato Problema/Objetivo do semestre/Público-alvo/Proposta de valor/Escopo, sintetizando o conteúdo da Lean Inception (v1.0) | [Eduardo Ferreira](https://github.com/eduardoferre) | 05/09/2026| | |
