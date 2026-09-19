# Backlog do MVP 

Este documento detalha o escopo da primeira entrega do projeto

## Bloco 1: Acesso e Cadastro do Médico

### US 01: Cadastro de Nova Conta do Profissional
* **Como** profissional de saúde,
* **Quero** preencher um formulário com meus dados básicos e CRM,
* **Para que** eu possa criar minha conta na plataforma.
* **Critérios de Aceitação:**
  1. Validação de e-mail válido e senha segura.
  2. Campo obrigatório para preenchimento do CRM.

### US 02: Login do Profissional
* **Como** profissional de saúde cadastrado,
* **Quero** inserir meu e-mail e senha na tela de login,
* **Para que** eu possa acessar meu painel e gerenciar os testes dos pacientes.
* **Critérios de Aceitação:**
  1. Autenticação bem-sucedida redireciona para o dashboard principal.
  2. Mensagem de erro amigável em caso de credenciais inválidas.

### US 03: Recuperação de Senha
* **Como** profissional que esqueceu a senha,
* **Quero** solicitar a redefinição de senha por e-mail,
* **Para que** eu consiga recuperar o acesso à minha conta sem travamentos.
* **Critérios de Aceitação:**
  1. Envio de link temporário e seguro para o e-mail cadastrado.

---

## Bloco 2: Termo de Consentimento

### US 04: Apresentação e Aceite do TCLE (Paciente/Responsável)
* **Como** profissional de saúde,
* **Quero** exibir o Termo de Consentimento Livre e Esclarecido (TCLE) na tela para o paciente ou seu responsável legal ler e aceitar antes da avaliação,
* **Para que** a realização do teste e a coleta dos dados de saúde fiquem legalmente resguardadas.
* **Critérios de Aceitação:**
  1. O sistema deve apresentar o texto do TCLE de forma legível.
  2. Deve haver um mecanismo de aceite digital (botão/checkbox) antes de liberar a tela dos testes.

---

## Bloco 3: Motor de Desenho e Interação

### US 05: Desenho com Caneta na Área de Trabalho
* **Como** paciente realizando a avaliação,
* **Quero** desenhar na tela utilizando apenas a caneta stylus,
* **Para que** eu possa realizar o traçado dos testes cognitivos.
* **Critérios de Aceitação:**
  1. O sistema deve capturar exclusivamente entradas vindas de caneta stylus, ignorando o toque dos dedos.
  2. O traço deve ser renderizado em tempo real com fluidez.

### US 06: Reversão de Traço
* **Como** paciente,
* **Quero** acionar um comando para remover o último traço desenhado (comportamento de pilha),
* **Para que** eu possa corrigir um erro recente sem precisar refazer todo o desenho.
* **Critérios de Aceitação:**
  1. O sistema deve manter uma pilha com a ordem cronológica dos traços realizados.
  2. Ao acionar o botão de desfazer, o último traço adicionado deve ser imediatamente removido do canvas.

### US 07: Apagar Desenho Completo
* **Como** paciente,
* **Quero** acionar um botão para limpar totalmente a área de desenho,
* **Para que** eu possa reiniciar a tarefa do zero caso necessário.
* **Critérios de Aceitação:**
  1. O sistema deve exibir um botão ou comando claro de limpeza total.
  2. Ao acionar a ação, todos os traços do canvas e os registros da pilha atual devem ser apagados.