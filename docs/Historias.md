# Histórias de Usuário

## Bloco 1: Acesso e Cadastro do Médico

### US 01: Cadastro de Nova Conta do Profissional
* **Como** profissional de saúde,
* **Quero** preencher um formulário com meus dados básicos e CRM,
* **Para que** eu possa criar minha conta na plataforma.
* **Critérios de Aceitação:**
  1. O sistema deve validar se o formato do e-mail é válido e se a senha atende aos requisitos mínimos de segurança.
  2. O sistema deve obrigar o preenchimento do campo CRM para habilitar o envio do formulário.

### US 02: Login do Profissional
* **Como** profissional de saúde cadastrado,
* **Quero** inserir meu e-mail e senha na tela de login,
* **Para que** eu possa acessar meu painel e gerenciar os testes dos pacientes.
* **Critérios de Aceitação:**
  1. O sistema deve redirecionar o usuário para o dashboard principal após a autenticação bem-sucedida.
  2. O sistema deve exibir uma mensagem de erro na tela caso as credenciais fornecidas sejam inválidas.

---

## Bloco 2: Triagem do Paciente e Termo de Consentimento

### US 03: Cadastro do Paciente para Avaliação
* **Como** profissional de saúde,
* **Quero** preencher os dados básicos do paciente (nome, data de nascimento, escolaridade),
* **Para que** a avaliação cognitiva seja devidamente identificada e associada ao indivíduo.
* **Critérios de Aceitação:**
  1. O sistema deve exigir o preenchimento de todos os campos do formulário (Nome Completo, Número da Ficha, Data de Nascimento, Escolaridade e Sexo) antes de liberar a página pro termo de consentimento.
  2. O campo deve aplicar máscara de data (`DD/MM/AAAA`), validar se a data inserida é válida e impedir a inserção de datas futuras.
  3. O campo deve aceitar apenas valores numéricos inteiros representando o total de anos de estudo do paciente.
  4. O sistema deve preencher automaticamente o bloco "PROFISSIONAL RESPONSÁVEL" com o Nome, CRM e E-mail do médico autenticado na sessão atual, mantendo esses campos desabilitados para edição manual.
  5. Ao acionar o botão "IR PARA O TERMO DE CONSENTIMENTO" com os dados válidos, o sistema deve persistir as informações temporariamente na sessão e redirecionar para a etapa seguinte.
  6. O Nome Completo do paciente deve ser armazenado apenas no banco de dados local do dispositivo, para uso do profissional de saúde, e nunca deve compor qualquer pacote de dados exportado.

### US 04: Apresentação e Aceite do TCLE
* **Como** profissional de saúde,
* **Quero** exibir o Termo de Consentimento Livre e Esclarecido (TCLE) na tela para o paciente ou seu responsável legal ler e assinar antes da avaliação,
* **Para que** a realização do teste e a coleta dos dados de saúde fiquem legalmente resguardadas.
* **Critérios de Aceitação:**
  1. O sistema deve renderizar o texto do TCLE com suporte a rolagem para leitura completa.
  2. Os seletores de consentimento devem permitir alternar dinamicamente entre "SIM" e "NÃO".
  3. O sistema deve manter a navegação para os testes bloqueada até que o botão de "Assinar e Iniciar" seja acionado com a assinatura preenchida.

---

## Bloco 3: Motor de Desenho e Interação

### US 05: Desenho com Caneta na Área de Trabalho
* **Como** paciente realizando a avaliação,
* **Quero** desenhar na tela utilizando apenas a caneta stylus,
* **Para que** eu possa realizar o traçado dos testes cognitivos.
* **Critérios de Aceitação:**
  1. O sistema deve ignorar o toque dos dedos e capturar exclusivamente entradas vindas de caneta stylus.
  2. O sistema deve renderizar o traço no canvas em tempo real.

### US 06: Reversão de Traço
* **Como** paciente,
* **Quero** acionar um comando para remover o último traço desenhado,
* **Para que** eu possa corrigir um erro recente sem precisar refazer todo o desenho.
* **Critérios de Aceitação:**
  1. O sistema deve disponibilizar o botão "DESFAZER" visível na área de controles lateral em todas as etapas de desenho.
  2. Ao acionar o botão "DESFAZER", o sistema deve apagar imediatamente o último traço executado pelo paciente na tela.
  3. O sistema deve permitir o acionamento sequencial da ação de desfazer para reverter múltiplos traços até que a área de trabalho retorne ao estado inicial.
  4. O botão "DESFAZER" deve permanecer desabilitado enquanto não houver nenhum traço desenhado na tela.

### US 07: Apagar Desenho Completo
* **Como** paciente,
* **Quero** acionar um botão para limpar totalmente a área de desenho,
* **Para que** eu possa reiniciar a tarefa do zero caso necessário.
* **Critérios de Aceitação:**
  1. O sistema deve disponibilizar o botão "APAGAR TUDO" na barra de controles lateral em todas as etapas de desenho.
  2. O botão "APAGAR TUDO" deve permanecer desabilitado enquanto não houver nenhum traço desenhado no canvas.
  3. Ao acionar o botão "APAGAR TUDO", o sistema deve exibir uma janela modal de confirmação com o título "APAGAR O DESENHO?" e as opções "CANCELAR" e "APAGAR".
  4. Ao acionar a opção "CANCELAR", o sistema deve fechar a janela modal e manter o desenho atual sem nenhuma alteração.
  5. Ao acionar a opção "APAGAR", o sistema deve limpar totalmente a área de desenho do canvas, zerar os traços da tarefa atual e manter o paciente na mesma etapa do teste.
  6. O sistema deve registrar o evento de apagar tudo salvando a data e o horário exatos em que a ação ocorreu para compor as métricas da avaliação.

---

## Bloco 4: Captura de Dados e Métricas do Traçado

### US 08: Captura de Coordenadas, Ordem e Tempo do Traçado
* **Como** profissional de saúde,
* **Quero** que o aplicativo registre em tempo real as coordenadas cartesianas (X, Y), a ordem cronológica dos traços e o tempo exato de execução do paciente,
* **Para que** esses dados métricos fiquem guardados com precisão para a posterior análise neurológica.
* **Critérios de Aceitação:**
  1. O sistema deve armazenar os pontos cartesianos do traçado associados à respectiva marcação temporal.
  2. O sistema deve registrar a sequência numérica exata em que cada traço foi executado pelo paciente.

### US 09: Armazenamento Local
* **Como** profissional de saúde,
* **Quero** que o aplicativo salve os dados e progressos dos testes de forma segura no banco de dados local do tablet,
* **Para que** todas as avaliações fiquem integralmente registradas no dispositivo sem dependência de rede.
* **Critérios de Aceitação:**
  1. O sistema deve persistir os dados da avaliação e os traços do desenho no banco de dados local do dispositivo.
  2. O sistema deve permitir a recuperação e a visualização dos registros salvos no próprio tablet.

---

## Bloco 5: Processamento e Inteligência Artificial

### US 10: Execução de Inferência do Modelo de IA Embarcado
* **Como** profissional de saúde,
* **Quero** que o aplicativo processe o modelo de inteligência artificial localmente no tablet utilizando os dados do traçado capturado,
* **Para que** seja gerada uma pontuação preliminar de risco de demência de forma rápida, sem depender de conexão com a internet.
* **Critérios de Aceitação:**
  1. O modelo embarcado deve processar os traços coletados da caneta e retornar a inferência de escore com sucesso.
  2. O sistema deve renderizar o resultado da inferência na tela em até 3 segundos após a solicitação do processamento. *(sem fonte documental ainda — confirmar viabilidade com quem for treinar/exportar o modelo antes de travar como critério de aceitação)*

---

## Bloco 6: Fluxo de Telas, Instruções e Encerramentos

### US 11: Exibição de Instruções Simples por Tarefa
* **Como** paciente,
* **Quero** visualizar telas de instruções claras e simplificadas antes do início de cada teste cognitivo,
* **Para que** a execução do exercício ocorra sem dúvidas sobre o que deve ser feito.
* **Critérios de Aceitação:**
  1. O sistema deve apresentar um card ou tela explicativa inicial contendo orientações textuais para cada teste.
  2. O sistema deve liberar a tela de desenho somente após a conclusão da tela de instrução.

### US 12: Tela de Resultado para o Profissional de Saúde
*(renomeada — o título anterior, "Tela de Encerramento", colidia com a "Tela de encerramento sem escore" do paciente, que é uma tela diferente e não deve mostrar escore nenhum)*
* **Como** profissional de saúde,
* **Quero** visualizar uma tela de conclusão ao término do teste com o resumo e o escore gerado,
* **Para que** eu possa acompanhar o fechamento da avaliação do paciente.
* **Critérios de Aceitação:**
  1. O sistema deve exibir uma tela de sucesso informando o término da avaliação, distinta da tela de encerramento exibida ao paciente.
  2. O sistema deve apresentar os resultados numéricos gerados pela inferência de forma visível na interface do médico.

---

## Bloco 7: Exportação de Dados

### US 13: Exportação de Dados Anonimizados para a Base de Pesquisa
*(reescrita — a versão anterior falava em "integrar com sistemas externos", o que contraria o item "fora do escopo" de `visao.md`: integração com prontuário eletrônico / envio a servidor externo. O que está validado em `funcionalidades.md` é exportar dados anonimizados para a base de pesquisa da própria equipe)*
* **Como** profissional de saúde,
* **Quero** exportar o pacote de dados do atendimento, incluindo métricas e traçados da avaliação, em um arquivo XML estruturado,
* **Para que** eu possa contribuir com a base de dados de pesquisa da equipe.
* **Critérios de Aceitação:**
  1. O sistema deve disponibilizar um botão de exportação funcional para gerar o arquivo no formato XML.
  2. O arquivo XML gerado deve conter os metadados, traços e resultados numéricos referentes à avaliação realizada.
  3. **(novo)** O arquivo XML não deve conter nenhum dado de identificação direta do paciente (nome completo, por exemplo); a referência ao paciente no arquivo deve usar apenas o Número da Ficha.

## Histórico de Versões

| Versão | Descrição | Autor(es) | Data | Revisor(es) | Data de Revisão |
|---|---|---|---|---|---|
| | | | | | |