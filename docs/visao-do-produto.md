# Visão do Produto

Documento gerado a partir das dinâmicas de Lean Inception do projeto.

## 1. Declaração da Visão do Produto
**Para:** Médicos generalistas / Médicos que avaliam pessoas idosas em ambiente hospitalar, e pacientes idosos submetidos a avaliação neurológica.
**Cujo (Problema):** O rastreio cognitivo hoje é aplicado em papel e pontuado à mão, o que consome tempo de consulta, varia de avaliador para avaliador, não gera registro comparável no tempo e carece de simplicidade.
**O (Produto):** É um aplicativo Android que roda localmente no tablet do hospital, com modelo de IA embarcado.
**Que (Benefício):** Realiza triagem e analisa tarefas de desenho, entregando ao médico um escore objetivo e reprodutível em poucos minutos, sem internet e sem que o dado do paciente saia da instituição. Entrega ao paciente um teste curto, sem exposição desnecessária.
**Diferentemente de:** Testes clínicos tradicionais e plataformas digitais de avaliação cognitiva (como DCTclock / Linus Health), que dependem de hardware proprietário, exigem nuvem, são validados em população norte-americana e não têm versão em português.
**O Nosso Produto:** Contará com 3 testes de desenho, roda em tablet Android comum, funciona 100% offline mantendo os dados na instituição. Usa IA para auxiliar na análise e é validado sobre a população brasileira, considerando a variação de escolaridade.

## 2. É / Não É - Faz / Não Faz

### É
- Aplicativo Android (APK).
- Roda localmente no tablet do hospital.
- Modelo de IA embarcado no aplicativo.
- Ferramenta de rastreio / triagem cognitiva.
- Apoio à decisão do profissional.
- Baseado em tarefas de desenho.
- Usável por pessoa idosa com pouca familiaridade com tecnologia.
- Software que trata dado sensível de saúde.

### Não É
- Diagnóstico.
- Prescrição nem conduta.
- Substituto da avaliação médica.
- Aplicação Web.
- Multiplataforma (iOS, desktop).
- Aplicativo de loja (Play Store).
- Integrado a prontuário eletrônico.
- Plataforma de acompanhamento longitudinal.

### Faz
- Coleta desenhos feitos pelo paciente na tela.
- Classifica em faixas de desempenho.
- Retorna resultado da triagem de declínio cognitivo.
- Captura a imagem final de cada desenho e o traçado.
- Roda a inferência no próprio tablet, sem internet.
- Gera escore por teste e escore geral.
- Apresenta as 3 tarefas em sequência, dando instruções simples.
- Autentica o médico (cadastro e login).
- Registra quem aplicou, em que condições e vincula o atendimento ao médico.
- Usa IA para apoiar análise e guarda o resultado da triagem.

### Não Faz
- Não substitui o profissional da saúde.
- Não dá recomendações, nem mostra resultados ou laudos ao paciente.
- Não usa métricas de pressão da caneta, angulação ou tremor.
- Não indica medicação nem possíveis condições de saúde.
- Não toma decisão sozinha (sem revisão médica).
- Não classifica sem mostrar incerteza.
- Não pede login ao paciente.
- Não mostra evolução no tempo.
- Não envia dados para o servidor.
- Não possui mais de 3 testes.

## 3. Objetivos de Negócio
- **Cluster 1 (IA e Escore):** A IA deve acertar igual a um especialista; Escore confiável; Comparar com avaliação de médico; Saber a margem de erro.
- **Cluster 2 (Experiência do Paciente):** O idoso fazer sem ajuda; Não constranger o paciente; Entender a instrução de primeira; Ninguém desistir no meio.
- **Cluster 3 (Experiência do Médico):** Caber nos minutos da consulta; Médico entender o resultado sozinho; O médico confiar no número; Não dar trabalho extra pro médico.
- **Sem Cluster (Dados):** Juntar desenhos de gente de verdade; Poder usar os dados dos pacientes.

## 4. Personas

### Persona 1: Seu José (Paciente)
- **Perfil:** 78 anos, viúvo há 3 anos, mora sozinho. Ex-motorista de ônibus aposentado, estudou até a 5ª série. A filha o traz nas consultas. Hipertenso e diabético, toma remédios controlados.
- **Comportamento:** Diz que está ótimo mesmo quando não está. Minimiza esquecimentos (diz que é fator da idade). Nunca usou tablet, usa celular só para ligar. Letra trêmula, apoia a mão para escrever. Quando não entende, não pergunta.
- **Necessidades:** Não se sentir diminuído na frente da família. Saber que não tem nota nem prova. Saber para que serve aquilo que estão pedindo. Fazer sozinho, sem ninguém segurando a mão dele.

### Persona 2: Dr. Marcelo (Médico)
- **Perfil:** 51 anos, geriatra. Consultório particular + 1 dia em hospital-escola. 20 anos de formado, mestrado. Atende de 12 a 16 idosos por dia, dá aula na graduação.
- **Comportamento:** Pede evidência antes de adotar qualquer coisa. Quer saber amostra, referência e quem pontuou. Não aceita "a inteligência artificial disse". Se o número não se explica, ignora e olha o desenho. Confia mais no que ele mesmo vê. Teme responsabilidade sobre decisão de máquina. Pergunta pela referência bibliográfica. Usa os instrumentos que ele já conhece.
- **Necessidades:** Ver o desenho junto com o número. Saber quais características puxaram o score. Conhecer a margem de erro e o limite da amostra. Poder discordar do sistema e registrar isso. Clareza de que a responsabilidade clínica é dele. Ter o que dizer à família quando ela perguntar. Saber de onde veio o score de referência.

## 5. Jornadas de Usuário

### Jornada 1: Seu José (Faz a triagem)
1. Recebe o tablet.
2. Ouve a instrução do médico.
3. Vê a primeira tarefa na tela.
4. Desenha com a caneta.
5. Confirma que terminou.
6. Vê a segunda tarefa, desenha e confirma.
7. Vê a terceira tarefa, desenha e confirma.
8. Tela de agradecimento sem o score.
9. Devolve o tablet sem saber que foi pontuado.

### Jornada 2: Dr. Marcelo (Aplicação de rotina)
1. Abre o app no tablet.
2. Faz login.
3. Inicia nova avaliação.
4. Informa dados mínimos do paciente.
5. Entrega o tablet e dá a instrução.
6. Aguarda o paciente terminar os 3 desenhos.
7. Recebe o tablet de volta.
8. Vê os 3 desenhos e os escores.
9. Vê quais características puxaram o escore.
10. Vê a faixa de desempenho e a incerteza.
11. Concorda ou registra discordância.
12. Decide se encaminha para avaliação aprofundada.

### Jornada 3: Dr. Marcelo (Usa pela primeira vez)
1. Recebe o tablet configurado pelo hospital.
2. Abre o app.
3. Cria a conta / recebe credencial.
4. Vê uma explicação curta do que o app faz.
5. Vê o aviso de que não é diagnóstico.
6. Faz uma aplicação de teste.
7. Entende como ler a tela de resultado.
8. Aplica no primeiro paciente real.

| Versão | Descrição | Autor(es) | Data | Revisor(es) | Data de Revisão |
|---|---|---|---|---|---|
| 1.0 | Criação do documento: Declaração de Visão, É/Não É, Objetivos, Personas e Jornadas de Usuário | [Artur Mendonça Arruda](https://github.com/ArtyMend07) | 03/09/2026 | [Lucas Mendonça Arruda](https://github.com/lucasarruda9), [Gabriel Lopes de Amorim](https://github.com/BrzGab) | |
