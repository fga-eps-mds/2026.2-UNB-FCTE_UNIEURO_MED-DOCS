# Plano de Gestão de Riscos

## Introdução

A gestão de riscos é um componente essencial no desenvolvimento de software, garantindo que os projetos alcancem seus objetivos com sucesso e dentro do prazo previsto. Este plano de gestão de riscos tem como objetivo identificar, analisar, priorizar e mitigar os riscos potenciais que podem surgir ao longo do ciclo de vida do desenvolvimento do software, ressaltando que é um produto novo, sendo implementado do zero.

O contexto do projeto agrava a exposição a certos riscos e reduz outros, sendo fundamental que a equipe esteja ciente desses riscos e tenha estratégias para lidar com eles. A gestão de riscos eficaz não apenas protege o projeto contra possíveis falhas, mas também contribui para a melhoria contínua do processo de desenvolvimento, promovendo uma cultura de proatividade e resiliência.

Este documento fornece uma visão geral das estratégias e processos que serão implementados para assegurar que os riscos sejam gerenciados de maneira eficaz, minimizando impactos negativos e promovendo a entrega do MVP dentro do prazo final e com sua devida qualidade.

### Tipos de risco

Os riscos foram divididos nas seguintes categorias:

- Externo
- Gerencial
- Organizacional
- Técnico

## Definições

### Probabilidade e impacto dos riscos

| Nível | Probabilidade | Porcentagem de certeza |
| :---: | :---: | :---: |
| 1 | Muito baixa | 0% - 19% |
| 2 | Baixa | 20% - 39% |
| 3 | Média | 40% - 59% |
| 4 | Alta | 60% - 79% |
| 5 | Muito alta | 80% - 100% |

### Impacto

| Nível | Impacto |
| :---: | :---: |
| 1 | Muito baixo |
| 2 | Baixo |
| 3 | Médio |
| 4 | Alto |
| 5 | Muito alto |

### Matriz de probabilidade X impacto

| Probabilidade / Impacto | Muito baixo | Baixo | Médio | Alto | Muito alto |
| :---: | :---: | :---: | :---: | :---: | :---: |
| Muito baixa | 1 | 2 | 3 | 4 | 5 |
| Baixa | 2 | 4 | 6 | 8 | 10 |
| Média | 3 | 6 | 9 | 12 | 15 |
| Alta | 4 | 8 | 12 | 16 | 20 |
| Muito alta | 5 | 10 | 15 | 20 | 25 |

### Graus de risco

| Grau | Risco |
| :---: | :---: |
| 1 - 5 | Baixo |
| 6 - 12 | Médio |
| 15 - 25 | Elevado |

## Levantamento de riscos

### Tabela de Riscos

| Risco | Descrição | Categoria |
| :---: | :---: | :---: |
| R01 | Dificuldade com as tecnologias definidas | Técnico |
| R02 | Saída de algum integrante do projeto | Gerencial |
| R03 | Divergência nos horários disponíveis dos integrantes | Organizacional |
| R04 | Alteração no escopo do projeto | Gerencial |
| R05 | Integrante com problema de saúde | Externo |
| R06 | Indisponibilidade do cliente ou de especialistas para esclarecimento de requisitos | Externo |
| R07 | Sobrecarga de membros da equipe, principalmente perto das entregas de release | Gerencial |
| R08 | Falha de equipamento | Externo |
| R09 | Dependência entre atividades | Organizacional |
| R10 | Perda ou corrupção de dados armazenados localmente no dispositivo | Técnico |
| R11 | Resultados insatisfatórios da solução desenvolvida | Técnico |
| R12 | Falta de dados adequados para desenvolvimento e validação | Externo |
| R13 | Dificuldade em treinar um modelo de IA com desempenho adequado | Técnico |
| R14 | Questões de privacidade e proteção de dados sensíveis | Externo |

### Causa e Consequência dos Riscos

| Risco | Causa | Consequência |
| :---: | :---: | :---: |
| R01 | Falta de experiência da equipe com tecnologias como React Native/Expo e modelos de IA embarcados | Atrasos no desenvolvimento e aumento da curva de aprendizado |
| R02 | Desistência, trancamento de disciplina ou imprevisto pessoal de integrante (equipe estudantil) | Redução da capacidade da equipe e sobrecarga dos demais membros |
| R03 | Conflitos de agenda entre integrantes com outras disciplinas e compromissos acadêmicos | Dificuldade de comunicação e atraso na execução das atividades |
| R04 | Mudanças nos requisitos solicitadas pelo cliente (UniEuro) | Retrabalho e impacto no cronograma do projeto |
| R05 | Problemas de saúde de integrantes | Ausência temporária e atraso nas entregas |
| R06 | Falta de disponibilidade do cliente ou de especialistas (ex.: professor/PO da UniEuro) | Dificuldade na definição de requisitos e atrasos no projeto |
| R07 | Distribuição inadequada de tarefas, especialmente perto das releases | Queda na produtividade e risco de burnout |
| R08 | Problemas técnicos em equipamentos (tablets, notebooks) | Interrupção do trabalho e perda de produtividade |
| R09 | Forte dependência entre tarefas de frentes diferentes (ex.: modelo de IA e aplicativo) | Efeito cascata de atrasos no cronograma |
| R10 | Falha na gravação, App fechado no meio de uma avaliação, ou problema no armazenamento local do Tablet | Perda de avaliações já realizadas e necessidade de repetir a coleta |
| R11 | Limitações da solução ou erros na implementação (ex.: desempenho do modelo de IA no tablet) | Entregas que não atendem aos requisitos esperados |
| R12 | Falta ou baixa qualidade dos dados disponíveis para treinar/validar o modelo | Dificuldade na validação e baixa confiabilidade da solução |
| R13 | Dados insuficientes, modelo mal calibrado ou problema mais difícil do que o previsto | Resultado da avaliação pouco confiável, exigindo retrabalho no modelo |
| R14 | Falta de cuidado no tratamento/armazenamento de dados pessoais de saúde dos usuários | Exposição indevida de dados ou impedimento de uso em ambiente real |

### Prevenção e Solução dos Riscos

| Risco | Prevenção | Solução |
| :---: | :--- | :---: |
| R01 | Capacitação prévia da equipe e escolha adequada de tecnologias | Buscar apoio externo, estudos adicionais ou simplificação da solução |
| R02 | Documentação do projeto e compartilhamento de conhecimento | Redistribuição das tarefas entre os membros restantes |
| R03 | Planejamento de horários e definição de reuniões fixas | Reorganização do cronograma e uso de comunicação assíncrona |
| R04 | Definição clara de requisitos e controle de mudanças | Replanejamento do projeto e priorização de funcionalidades |
| R05 | Distribuição equilibrada de tarefas | Redistribuição das atividades e ajuste no cronograma |
| R06 | Agendamento prévio de reuniões com cliente/especialistas | Tomada de decisões com base em suposições documentadas até validação |
| R07 | Planejamento adequado da carga de trabalho | Redistribuição de tarefas e ajuste de prazos |
| R08 | Manutenção preventiva e uso de backup de arquivos | Utilização de equipamentos alternativos e recuperação de dados |
| R09 | Planejamento das atividades considerando dependências | Reorganização da ordem das tarefas e ajuste no cronograma |
| R10 | Testes de persistência de dados e rotina de backup/exportação periódica | Recuperação a partir do último backup e revisão do mecanismo de gravação local |
| R11 | Testes contínuos e validações frequentes com o cliente | Correção da solução e ajustes nos requisitos |
| R12 | Busca antecipada por bases de dados adequadas | Utilização de dados alternativos ou adaptação da solução |
| R13 | Validação incremental do modelo com dados de teste desde as primeiras sprints | Ajustar o modelo, buscar mais dados ou simplificar o problema a ser resolvido |
| R14 | Anonimização de dados e boas práticas de segurança desde o início do projeto | Revisão do tratamento de dados e adequação às exigências da LGPD |


## Histórico de versões

| Versão | Descrição | Autor | Data | Revisor | Data de revisão |
|---|---|---|---|---|---|
| 1.0 | Criação da documentação de riscos | [Eduardo Ferreira](https://github.com/eduardoferre) | 27/09/2026 | A definir | — |