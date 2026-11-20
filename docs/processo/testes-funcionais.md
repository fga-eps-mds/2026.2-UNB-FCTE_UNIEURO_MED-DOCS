# Plano de Testes Funcionais — MNEMA

## 1. Finalidade

Este plano define os testes funcionais do aplicativo MNEMA: a verificação, pela equipe,
de que o APK instalado no tablet faz o que as histórias de usuário pedem. Ele detalha o
nível **Sistema** da Tabela 7 do [Plano de Qualidade](plano_de_qualidade.md#51-niveis-de-teste)
e produz as medidas de qualidade externa E3, E5, E6, E7, E8 e E9 da Tabela 6 do mesmo plano.

Os testes automatizados (unitários, de integração e de sistema no Jest) rodam em todo
PR, mas rodam no computador, com o banco em memória. Eles não mostram que o APK
instala, abre sem internet, responde à caneta e grava os dados no aparelho de verdade.
Os testes funcionais cobrem essa diferença.

O teste funcional não substitui o teste de aceitação. A equipe executa os cenários
antes de enviar o APK aos *Product Owners*. O aceite continua sendo dos *Product
Owners*, com o formulário de aceitação (Plano de Qualidade, seção 5.2).

## 2. Abordagem

- **Tipo:** teste manual de caixa-preta, do ponto de vista de quem usa o aplicativo.
- **Onde:** no APK da release, instalado no tablet do projeto, com o **modo avião
  ligado** durante toda a execução.
- **Quando:** em cada release (Release Minor e Release Major) e antes de cada envio de
  APK aos *Product Owners*.
- **Quem:** uma pessoa da equipe que não implementou a história, sempre que possível.
- **Dados:** só dados fictícios. Os CPFs de teste são gerados com dígitos
  verificadores válidos e não pertencem a ninguém.
- **De onde vêm os cenários:** dos critérios de aceitação (BDD) das histórias
  entregues. Cada cenário indica a história de origem.

### 2.1 O que fica para os testes automatizados

Alguns critérios não podem ser provocados à mão no tablet. Eles continuam cobertos
pelos testes automatizados e não entram no roteiro:

**Tabela 1** – Critérios cobertos só pelos testes automatizados

| Critério | História | Teste automatizado |
|---|---|---|
| Gravação "tudo ou nada" quando o banco falha | #10 | `tests/integration/gravacao-desenho.integration.test.tsx` |
| Traços apagados gravados e marcados como apagados | #10 e #23 | `tests/integration/gravacao-desenho.integration.test.tsx` |
| CPF e dados protegidos ilegíveis no arquivo do banco (E4) | #17 | `tests/integration/cifra-do-banco.integration.test.ts` |
| Um médico não vê o que outro coletou, pela consulta ao banco | #59 | `tests/integration/tela-inicial.integration.test.tsx` |

## 3. Preparação

1. Baixar o APK anexado à release que será testada e anotar a tag (por exemplo,
   `v2.1.0`).
2. Anotar o modelo do tablet e a versão do Android.
3. Ligar o **modo avião** e confirmar que o Wi-Fi e os dados móveis estão desligados.
4. Ter à mão duas contas de médico fictícias (médico A e médico B) e três pacientes
   fictícios com CPFs válidos.
5. Ter a caneta do tablet, se houver, e testar também com o dedo.

## 4. Cenários

Cada cenário tem um identificador fixo (TF-nn), para comparar a mesma execução entre
releases.

### 4.1 Instalação e funcionamento sem internet

**Tabela 2** – Instalação e funcionamento sem internet

| Id | Cenário | Passos | Resultado esperado | Origem |
|---|---|---|---|---|
| TF-01 | Instalação limpa | Desinstalar o MNEMA, instalar o APK da release e abrir | O aplicativo abre na tela de login | E9 |
| TF-02 | Atualização sem perda de dados | Com dados de uma versão anterior, instalar o APK novo por cima | Instala sem pedir para desinstalar, e as contas e os pacientes continuam lá | E9 |
| TF-03 | Nenhuma permissão de rede | No computador, rodar `aapt dump permissions` no APK | Nenhuma permissão de internet ou de rede | E5, #16 |
| TF-04 | Fluxo completo em modo avião | Com o modo avião ligado, executar do TF-05 ao TF-30 | Nenhuma tela pede internet nem mostra erro de conexão | #15 |
| TF-05 | Tamanho do APK | Anotar o tamanho do arquivo do APK | Valor registrado na execução | E8 |

### 4.2 Cadastro e conta do médico (#5)

**Tabela 3** – Cadastro e conta do médico

| Id | Cenário | Passos | Resultado esperado | Origem |
|---|---|---|---|---|
| TF-06 | Cadastro com dados válidos | Na tela de cadastro, preencher todos os campos do médico A e confirmar | A conta é criada e o médico A consegue entrar com ela | #5 |
| TF-07 | Campo obrigatório vazio | Tentar confirmar o cadastro com um campo obrigatório vazio | O aplicativo indica qual campo falta e não cria a conta | #5 |
| TF-08 | Consulta dos próprios dados | Entrar e abrir as configurações | Aparecem o nome, o e-mail e o CRM do médico | #5 |
| TF-09 | Edição dos dados | Alterar o nome em "Editar meus dados" e confirmar com a senha atual | O novo nome aparece na tela inicial | #5 |
| TF-10 | Dado já usado por outra conta | Na conta do médico B, tentar usar o e-mail do médico A | O aplicativo informa que o dado já está em uso e não altera nada | #5 |
| TF-11 | Troca de senha | Trocar a senha, sair e entrar com a nova e depois com a antiga | Entra com a nova; a antiga é recusada | #5 |
| TF-12 | Senha atual incorreta | Tentar editar os dados com a senha atual errada | O aplicativo informa que a senha não confere e nada muda | #5 |
| TF-13 | Conta desativada | Desativar a conta do médico B e tentar entrar com ela | A sessão termina, e o login seguinte mostra "e-mail ou senha inválidos" | #5 |

### 4.3 Login e proteção do fluxo do paciente (#6 e #11)

**Tabela 4** – Login e proteção do fluxo do paciente

| Id | Cenário | Passos | Resultado esperado | Origem |
|---|---|---|---|---|
| TF-14 | Login correto | Entrar com o e-mail e a senha do médico A | Abre a tela inicial com o nome e o CRM dele | #6, #46 |
| TF-15 | Senha errada | Entrar com uma senha errada | O aplicativo avisa que os dados não conferem | #6 |
| TF-16 | Paciente sem login | Iniciar um exame e seguir até a tela final | Nenhuma tela pede login ao paciente | #6 |
| TF-17 | Voltar do Android no fluxo do paciente | Numa tarefa de desenho, apertar o voltar do Android | O aplicativo não sai da tarefa | #6 |
| TF-18 | Tela final sem escore | Terminar as três tarefas | Aparece só o agradecimento, sem escore, faixa ou resultado | #11, E6 |
| TF-19 | Resultado protegido | Na tela final, tentar voltar às telas do médico | O aplicativo pede a confirmação do médico | #11 |

### 4.4 Tela inicial e lista de pacientes (#46 e #59)

**Tabela 5** – Tela inicial e lista de pacientes

| Id | Cenário | Passos | Resultado esperado | Origem |
|---|---|---|---|---|
| TF-20 | Primeiro acesso | Entrar com uma conta sem pacientes | A lista informa que não há pacientes, e "Exportar todos" fica desabilitado | #46 |
| TF-21 | Sair | Tocar em "Sair" | A sessão termina e o aplicativo volta para o login | #46 |
| TF-22 | Dados e ordem da lista | Com pacientes atendidos, abrir a tela inicial | Cada linha tem nome, ficha, data e situação do último exame e quantidade de exames. O exame mais recente vem primeiro. Nenhum resultado do modelo aparece | #59 |
| TF-23 | Busca | Buscar por parte do nome sem acento, pela ficha e pelos primeiros dígitos do CPF | Só aparecem os pacientes que correspondem; sem correspondência, aparece o aviso de nenhum paciente | #59 |
| TF-24 | Só os pacientes do médico | Atender um paciente com o médico A, sair e entrar com o médico B | O médico B não vê o paciente atendido só pelo médico A | #59 |
| TF-25 | Abrir um paciente | Tocar num paciente da lista | Abre a tela com os dados do paciente e os exames do médico, do mais recente ao mais antigo | #59 |

### 4.5 Registro do atendimento e termo de consentimento (#7 e #21)

**Tabela 6** – Registro do atendimento e termo de consentimento

| Id | Cenário | Passos | Resultado esperado | Origem |
|---|---|---|---|---|
| TF-26 | Atendimento registrado | Tocar em "Novo exame", preencher os dados do paciente e confirmar | Abre o termo de consentimento | #7 |
| TF-27 | Campos inválidos | Tentar confirmar com CPF inválido, data de nascimento futura e escolaridade vazia | O aplicativo indica cada campo a corrigir e não registra o atendimento | #7 |
| TF-28 | Termo completo | Na tela do termo, rolar até o fim | O texto completo e a versão do termo aparecem; nenhuma tarefa abre antes da decisão | #21 |
| TF-29 | Assinatura obrigatória | Sem assinar, olhar o botão "Assinar e iniciar" | O botão fica desabilitado | #21 |
| TF-30 | Aceite pelo paciente | Assinar com a caneta e tocar em "Assinar e iniciar" | Abre a instrução da primeira tarefa | #21 |
| TF-31 | Aceite pelo responsável legal | Marcar "Responsável legal", informar o CPF dele, assinar e iniciar | Abre a instrução da primeira tarefa | #21 |
| TF-32 | Recusa do termo | Tocar em "Recusar" e confirmar | Nenhuma tarefa abre; na lista, o exame aparece como termo recusado | #21 |
| TF-33 | Desistir da recusa | Tocar em "Recusar" e depois em "Voltar" | O termo volta a aparecer, sem decisão gravada | #21 |

### 4.6 Instrução e tarefas de desenho (#8, #9 e #23)

**Tabela 7** – Instrução e tarefas de desenho

| Id | Cenário | Passos | Resultado esperado | Origem |
|---|---|---|---|---|
| TF-34 | Instrução de cada tarefa | Passar pelas três instruções | Cada uma tem o título, a frase combinada com o parceiro, "Tarefa n de 3" e o botão "Começar" | #8 |
| TF-35 | Ordem das tarefas | Seguir o exame do começo ao fim | A ordem é relógio, cópia do cubo e trilhas | #9 |
| TF-36 | Confirmar sem desenho | Abrir uma tarefa sem desenhar | "Confirmar" fica desabilitado | #9 |
| TF-37 | Traço na hora | Desenhar rápido com a caneta e com o dedo | O traço acompanha a ponta, sem atraso visível, e não muda ao levantar a caneta | #9 |
| TF-38 | Figura do cubo | Abrir a cópia do cubo | A figura de modelo fica visível ao lado da área de desenho durante toda a tarefa | #9 |
| TF-39 | Trilhas | Abrir as trilhas | Aparecem os círculos de 1 a 5 e de A a E | #9 |
| TF-40 | Desfazer | Desenhar três traços e tocar em "Desfazer" | Só o último traço sai | #23 |
| TF-41 | Apagar tudo | Desenhar, tocar em "Apagar tudo" e confirmar | A área fica vazia, sem mudar as tarefas anteriores | #23 |
| TF-42 | Confirmar uma vez só | Tocar duas vezes seguidas em "Confirmar" | O aplicativo avança só uma tarefa | #23 |
| TF-43 | Exame registrado | Terminar o exame e abrir o paciente na lista | O exame aparece com a data e a hora do início, sem nenhum escore na lista | #10 |

### 4.7 Cenários das histórias em andamento

Estes cenários entram no roteiro quando a história for integrada à `develop`.

**Tabela 8** – Cenários das histórias em andamento

| Id | Cenário | Passos | Resultado esperado | Origem |
|---|---|---|---|---|
| TF-44 | Retomada sem perda de dados | Desistir do exame na segunda tarefa, fechar o aplicativo e retomar | O exame volta na tarefa em que parou, sem repetir a primeira | #25, E3 |
| TF-45 | Exclusão de exame em andamento | Excluir um exame em andamento, confirmando com a senha | O exame sai da lista do paciente | #58 |
| TF-46 | Exame finalizado não é excluído | Abrir um exame concluído | Não há opção de excluir | #58, #47 |
| TF-47 | Superusuário vê todos | Entrar com a conta do administrador | A lista mostra os pacientes de todos os médicos, com quem atendeu | #49 |
| TF-48 | Tempo da inferência | Aplicar 20 exames seguidos e cronometrar o cálculo do escore | Registrar o percentil 95 do tempo | #12, E7 |
| TF-49 | Memória na inferência | Medir a memória de pico durante o cálculo do escore | Registrar o valor | #12, E8 |

## 5. Medidas produzidas

**Tabela 9** – Medidas de qualidade externa produzidas pelo roteiro

| Medida | Como sai deste roteiro |
|---|---|
| E3 Retomada sem perda de dados | `TF-44 aprovados / TF-44 executados` |
| E5 Permissões de rede no APK | Quantidade encontrada no TF-03 |
| E6 Resultado exibido ao paciente | Telas do paciente com escore encontradas no TF-18 |
| E7 Tempo de inferência | Percentil 95 do TF-48 |
| E8 Memória e tamanho do APK | TF-05 e TF-49 |
| E9 Instalação do APK | `instalações bem-sucedidas / tentativas` no TF-01 e no TF-02 |

Além delas, cada execução informa a taxa de cenários aprovados:
`cenários que passaram / cenários executados`.

## 6. Registro da execução

Cada execução vira um arquivo em `docs/qualidade/execucoes/`, com o nome da tag (por
exemplo, `tf-v2.1.0.md`), neste formato:

**Tabela 10** – Cabeçalho do registro de cada execução

| Campo | Valor |
|---|---|
| Release e tag | |
| Tablet e versão do Android | |
| Data | |
| Quem executou | |
| Modo avião ligado | Sim / Não |

**Tabela 11** – Resultado de cada cenário na execução

| Id | Resultado | Evidência | Bug aberto | Observação |
|---|---|---|---|---|
| TF-01 | Passou / Falhou / Bloqueado / Não executado | print ou vídeo | #nº | |

**Resultados possíveis:**
- **Passou:** o resultado esperado aconteceu.
- **Falhou:** o resultado foi outro. Abrir uma issue de bug com a severidade e o Id do
  cenário.
- **Bloqueado:** um cenário anterior impediu a execução.
- **Não executado:** a história ainda não está na release.

## 7. Critério de saída

A release só é enviada aos *Product Owners* quando:

- todos os cenários das histórias da release passam;
- nenhum bug de severidade Alta ou Crítica fica aberto (E2 = 0);
- E5 e E6 são zero.

Um cenário que falha numa história já aceita também conta como regressão (Plano de
Qualidade, Tabela 7).

## Histórico de versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
|---|---|---|---|---|
| 1.0 | 20/11/2026 | Roteiro de testes funcionais no tablet, com os cenários tirados dos critérios de aceitação das histórias entregues, as medidas de qualidade externa que ele produz e o registro de cada execução | [Gabriel Lopes de Amorim](https://github.com/BrzGab) | Pendente |
