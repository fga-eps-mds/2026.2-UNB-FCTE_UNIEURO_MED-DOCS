# Visão Operacional

Este documento tem como objetivo apresentar o panorama do desenvolvimento operacional do projeto, incluindo aspectos da organização do time, ferramentas utilizadas, estratégias de pareamento e gestão de conhecimento. 

## Ferramentas Utilizadas

Para o desenvolvimento do projeto e suas atividades, o time utiliza diversas ferramentas para comunicação, desenvolvimento do código-fonte, gestão de tarefas e controle de informações, listadas na tabela abaixo:

| Ferramenta | Finalidade | Categoria |
| :--- | :--- | :--- |
| GitHub | Armazenamento e controle de versão do código-fonte do aplicativo e documentação | Gerenciamento |
| ZenHub | Gestão de tarefas e acompanhamento do progresso do projeto | Gerenciamento|
| Discord | Comunicação rápida entre equipe e stakeholders | Comunicação |
| Whatsapp | Comunicação rápida entre os membros da equipe | Comunicação |
| Microsoft Teams | Realização de reuniões síncronas entre membros da equipe e stakeholders | Comunicação |
| Google Docs | Criação e edição de documentos colaborativamente.| Documentação |
| Github Pages | Hospedagem de documentação do projeto | Documentação |
| Canva | Criação de material para apresentações | Documentação |
| Visual Studio Code | Desenvolvimento do código-fonte do projeto | Desenvolvimento |
| SonarQube | Análise de qualidade do código-fonte e identificação de vulnerabilidades | Desenvolvimento |
| Figma | Criação de protótipos e quadros para validação com stakeholders | Desenvolvimento |
| Expo | Desenvolvimento do aplicativo mobile em React Native | Desenvolvimento |

## Quadro de Conhecimento e Estratégias de Pareamento

Para compreender o nível de proficiência técnica de cada membro do time e identificar lacunas de conhecimento que possam representar riscos para o desenvolvimento do projeto projeto, foram desenvolvidos dois quadros de acompanhamento, sendo eles:

>**`Quadro de Conhecimento`**: retrata o nível de proficiência técnica de cada membro do time, a partir da autoavaliação registrada na planilha de habilidades, identificando lacunas de conhecimento que representam risco para o projeto.

>**`Estratégias de Pareamento`**: registra as decisões de alocação dos membros da equipe, com a justificativa de cada pareamento, de forma a distribuir o conhecimento de maneira equilibrada e reduzir riscos.

---
### Planilha de Habilidades
Para a elaboração do quadro de conhecimento e decisão das estratégias de pareamento, foi desenvolvida uma planilha, na qual cada membro da equipe registrava seu nível de proficiência nas ferramentas/tecnologias a serem utilizadas no projeto. A planilha pode ser vista abaixo:

<iframe src="https://docs.google.com/spreadsheets/d/1iIR7TQVh9llJ0tOEl-gJgm6kFNBGZbTfWLmXhPPHyFI/edit?usp=sharing&rm=minimal&widget=true&headers=false" width="100%" height="600" frameborder="0"></iframe>

[Abrir a planilha em uma nova aba](https://docs.google.com/spreadsheets/d/1iIR7TQVh9llJ0tOEl-gJgm6kFNBGZbTfWLmXhPPHyFI/edit?usp=sharing){:target="_blank"}

### Escala de Proficiência

| Nível | Significado |
| :--- | :--- |
| Nenhum | Nunca utilizou ou teve contato mínimo. |
| Básico | Já utilizou em contexto de estudo/tutorial, com supervisão ou apoio constante. |
| Intermediário | Consegue utilizar de forma autônoma na maior parte das tarefas comuns. |
| Avançado | Domina a tecnologia, incluindo casos complexos, e pode orientar outros membros. |



---
### Panorama de Conhecimento da Equipe

Com base no dados da planilha, obteve-se um panorama do nível de proficiência da equipe nas tecnologias a serem utilizadas no projeto, destacando pontos fortes e lacunas de conhecimento que podem representar riscos para o desenvolvimento do projeto:

#### Pontos fortes do time

- **Git / GitHub**: 9 dos 11 membros em nível Avançado, portanto não representa risco.
- **Python**: Apenas um membro em nível básico, portanto a equipe apresenta uma base sólida para uso da linguagem
- **CI/CD e Testes**: nível Intermediário na maior parte do time.

#### Lacunas de conhecimento identificadas

| Tecnologia | Situação | Ponto de atenção |
| :--- | :--- | :--- |
| **Expo** | 4 membros em "Nenhum" e apenas 1 em Avançado (Gustavo Henrique) | Maior cautela na divisão de tarefas relacionadas ao Expo para evitar dependência de uma única pessoa |
| **React Native** | Maioria dos membros em "Básico" | Melhor acompanhamento do desenvolvimento das tarefas relacionadas ao React Native |
| **PyTorch** | 4 membros em "Nenhum" | Certa cautela na divisão de tarefas relacionadas ao PyTorch para amenizar possíveis dificuldades |
| **TensorFlow** | 4 membros em "Nenhum"| Certa cautela na divisão de tarefas relacionadas ao TensorFlow para amenizar possíveis dificuldades |
| **Testes (Jest, Detox, etc.)** | Ninguém em Avançado | Melhor acompanhamento no desenvolvimento e manutenção de testes |

#### Leitura estratégica

Através do levantamento feito pela planilha, identificamos dois polos de conhecimento bem definidos e pouco sobrepostos:

- **Polo IA/Dados** (Python, PyTorch, TensorFlow)
- **Polo DevOps/Processo** (Git/GitHub, CI/CD, Testes)

Foi identificado um polo com conhecimento relativamente sólido, mas que requer melhor acompanhamento e gestão de tarefas:
- **Polo Mobile/Frontend** (JavaScript, TypeScript, React Native, Expo)


### Estratégia de Pareamento

A estratégia de pareamento para o desenvolvimento do projeto visa manter uma melhor organização na distribuição de tarefas, de modo que as lacunas de conhecimento sejam reduzidas e que todos os membros possam contribuir de forma efetiva para o desenvolvimento do projeto, tendo foco nos seguintes pontos:

- **Reduzir lacunas críticas**: sempre que possível, parear membros com uma experiência menor (Básico/Nenhum) numa tecnologia aqueles que tenham uma base mais consolidada (Intermediário/Avançado).
- **Evitar dependência de pessoa única (bus factor)**: distribuir as tarefas de modo que nenhuma tecnologia dependa de exclusivamente de um membro da equipe, permitindo maior flexibilidade e colaboração no desenvolvimento.
- **Alternância de liderança**: Conforme estabelecido na disciplina, a liderança do projeto se alterna a cada duas semanas.Este fator deve sempre ser levado em consideração, de modo a organizar melhor a distribuição de tarefas e responsabilidades, evitando sobrecargas e permitindo melhor acompanhamento do desenvolvimento do projeto.


## Histórico de Versão

| Versão | Data | Descrição | Autor | Revisor |
| :----: | ---------- | --------- | ------------ | ------------ |
| 1.0 | 20/09/2026 | Criação do documento operacional da equipe e Adição das ferramentas utilizadas estratégia de pareamento| [Henrique Galdino Couto](https://github.com/hgaldino05) | [Daniel Ferreira Nunes](https://github.com/Mach1r0) |
| 1.1 | 21/09/2026 | Inclusão do quadro de conhecimentos (planilha) | [Henrique Galdino Couto](https://github.com/hgaldino05) | [Daniel Ferreira Nunes](https://github.com/Mach1r0)  |