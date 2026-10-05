# Identidade Visual

Este documento é o guia de identidade visual do aplicativo de apoio ao rastreio cognitivo por meio de tarefas de desenho. Ele define a marca, as cores, as fontes, os componentes da interface e as regras de acessibilidade. Toda tela desenhada e todo código de interface do aplicativo devem seguir este guia, para que o produto fique padronizado do desenho à implementação.

## Como usar este guia

- **Quem desenha as telas** usa as cores, os estilos de texto e os componentes daqui. Quando precisar de algo que não existe no guia, propõe a mudança no guia primeiro e depois desenha.
- **Quem implementa** usa os tokens da seção [Tokens para o código](#tokens-para-o-codigo), que espelham este guia no arquivo `src/constants/theme.ts` do aplicativo. Cor, tamanho de texto e espaçamento não devem ser escritos direto no componente.
- **Quem revisa uma tela ou um PR** confere a [lista de verificação](#lista-de-verificacao) no fim da página.

## Fundamentos da marca

### Contexto e público

O aplicativo tem dois públicos que usam o mesmo tablet em momentos diferentes:

- o **profissional de saúde**, com alto nível de instrução, mas sem pressupor familiaridade com tecnologia. Ele faz o cadastro, inicia o exame e lê o resultado;
- o **paciente idoso**, com 60 anos ou mais, muitas vezes com baixa escolaridade, pouca familiaridade com tablets e alguma dificuldade de visão ou de coordenação. Ele aceita o termo e faz os desenhos.

Por isso existem dois "tons" de interface: as **telas do profissional**, mais densas, e as **telas do paciente**, com letras e botões maiores, uma ação principal por vez e nenhuma informação que possa constranger, como nota, escore ou tempo.

### Personalidade

A identidade deve comunicar:

- **clareza**, sem elementos ambíguos nem excesso de informação;
- **confiança**, adequada a um contexto de pesquisa e de saúde;
- **acolhimento**, sem infantilizar o paciente idoso;
- **sobriedade**, usando a cor de forma funcional, e não decorativa;
- **acessibilidade**, com leitura e toque confortáveis para quem tem visão ou coordenação reduzidas.

## Logotipo

O logotipo é formado por um **símbolo** e pelo **nome do produto**. O símbolo é a letra inicial do nome, em branco, sobre um quadrado de cantos arredondados no laranja da marca. O nome fica abaixo do símbolo, em caixa alta e na cor azul-noite.

### Versões e usos

| Versão | Onde usar |
|---|---|
| Assinatura vertical (símbolo + nome) | Abertura do aplicativo, tela de login, apresentações e capas |
| Símbolo sozinho | Ícone do aplicativo no tablet e espaços pequenos |

### Construção do símbolo

- O símbolo é um quadrado com cantos arredondados em **30% do lado** (por exemplo, 22 dp de raio num símbolo de 72 dp).
- A letra usa a fonte Outfit SemiBold, branca, centralizada e com altura aproximada de metade do quadrado.

### Área de proteção e redução

- Manter ao redor da marca uma margem mínima equivalente a **1/4 da largura do símbolo**.
- Não exibir o símbolo com menos de **32 px** em meios digitais.
- Na assinatura completa, não reduzir a ponto de o nome ficar com menos de **16 px** de altura.
- Aplicar a assinatura completa sobre fundo branco ou outro fundo claro e liso.

### Usos indevidos

Não distorcer, inclinar, girar ou reorganizar os elementos; não trocar as cores por tons fora da paleta; não aplicar sombras ou contornos extras; e não colocar a marca sobre imagens que atrapalhem a leitura.

## Tipografia

### Famílias

O aplicativo usa **duas fontes**, cada uma com um papel:

| Fonte | Papel | Onde usar |
|---|---|---|
| **Outfit** | Fonte de destaque | Títulos, botões, rótulos de campo, rótulos de seção, números grandes do resultado e o logotipo |
| **Inter** | Fonte de leitura | Textos corridos, instruções, descrições, mensagens e o que o usuário digita nos campos |

A Outfit tem formas arredondadas e amigáveis, que funcionam bem em títulos e botões. A Inter foi feita para leitura em tela e é mais confortável em textos longos. As duas são gratuitas e estão no Google Fonts. No aplicativo, elas são carregadas pelos pacotes `@expo-google-fonts/outfit` e `@expo-google-fonts/inter`.

Quando uma delas não estiver disponível, a ordem de substituição é:

```css
font-family: Outfit, Inter, Arial, sans-serif;   /* destaque */
font-family: Inter, Arial, sans-serif;           /* leitura */
```

<div class="type-specimen" aria-label="Amostra das fontes do aplicativo">
  <p class="type-caption">OUTFIT SEMIBOLD · TÍTULOS E BOTÕES</p>
  <p class="type-display type-outfit">Desenhe um relógio</p>
  <p class="type-caption">INTER REGULAR · TEXTOS E INSTRUÇÕES</p>
  <p class="type-body">Com todos os números, marcando onze horas e dez minutos.</p>
  <p class="type-characters">Aa Bb Cc · 0123456789</p>
</div>

### Escala de texto

Os tamanhos estão em **dp**, a unidade de tela do Android, considerando um tablet de referência de 1280 × 800 dp. Os nomes dos estilos devem ser os mesmos na ferramenta de design e no código.

| Estilo | Fonte | Tamanho / altura da linha | Onde usar |
|---|---|---|---|
| **Título gigante** | Outfit Bold | 72 / 80 | Número de destaque no resultado e tela de encerramento do paciente |
| **Título médio** | Outfit SemiBold | 34 / 42 | Título de tela e de diálogo |
| **Título pequeno** | Outfit SemiBold | 24 / 32 | Título de cartão e de seção, e a instrução curta da tarefa |
| **Botão** | Outfit SemiBold | 26 / 32 nas telas do paciente · 20 / 26 nas telas do profissional | Texto de botão |
| **Rótulo grande** | Outfit Medium | 20 / 26 | Opções de escolha, indicador de tarefa e botões discretos |
| **Rótulo pequeno** | Outfit Medium | 16 / 22 | Rótulo de campo, cabeçalho de tabela e rótulos de seção |
| **Corpo grande** | Inter Regular | 24 / 36 | Textos das telas do paciente e de diálogos |
| **Corpo médio** | Inter Regular | 18 / 28 | Textos das telas do profissional e conteúdo dos campos |
| **Corpo pequeno** | Inter Regular | 16 / 24 | Mensagens de erro no campo e textos de apoio |

**Regras:**

- **O menor texto do aplicativo é 16.** Nas telas do paciente, o menor é 20.
- O peso fino (Light, Thin) não é usado. Os pesos são 400, 500, 600 e 700.
- Texto alinhado à esquerda. Centralizado só em títulos curtos, telas de encerramento e botões.
- Nada de texto justificado nem de itálico em blocos longos.
- O aplicativo deve continuar funcionando quando o usuário aumentar o tamanho da letra no Android.

### Caixa alta

!!! warning "Caixa alta só em rótulos curtos"
    Palavras escritas só com maiúsculas são mais difíceis de ler, principalmente para idosos e pessoas com baixa escolaridade, porque todas as letras ficam com o mesmo contorno. Por isso:

    - **Títulos, botões, instruções e mensagens** são escritos com **maiúscula só no início**: "Criar conta", "Desenhe um relógio", "Continuar o exame".
    - A **caixa alta** fica restrita ao **logotipo**, a **siglas** (CRM, CPF, TCLE, XML, CCL) e a **rótulos curtos de seção** de até três palavras, como "Motivo" ou "Registrado".
    - Quando um rótulo estiver em caixa alta, use espaçamento entre letras de 4%. No resto do texto, o espaçamento é 0.

## Cores

### Paleta da marca

São quatro cores de marca, mais o azul-noite e o branco como cores de apoio.

<div class="swatches">
  <div class="swatch"><span style="background:#9A3412"></span><b>Laranja da marca</b><code>#9A3412</code></div>
  <div class="swatch"><span style="background:#7F1D1D"></span><b>Vinho profundo</b><code>#7F1D1D</code></div>
  <div class="swatch"><span style="background:#FFE8D6"></span><b>Pêssego claro</b><code>#FFE8D6</code></div>
  <div class="swatch"><span style="background:#FEF3C7"></span><b>Creme</b><code>#FEF3C7</code></div>
  <div class="swatch"><span style="background:#0F172A"></span><b>Azul-noite</b><code>#0F172A</code></div>
  <div class="swatch"><span style="background:#FFFFFF"></span><b>Branco</b><code>#FFFFFF</code></div>
</div>

| Cor | Para que serve |
|---|---|
| **Laranja da marca** `#9A3412` | Botão principal, contorno de botão secundário, opção selecionada, indicador de progresso e links. É a cor de ação |
| **Laranja escuro** `#7C2D12` | Texto sobre o pêssego claro, como na descrição da tarefa |
| **Vinho profundo** `#7F1D1D` | Ações que destroem ou encerram (desistir, apagar, recusar, excluir) e a faixa "Este resultado não é diagnóstico" |
| **Pêssego claro** `#FFE8D6` | Fundo de lembretes e instruções da tarefa, fundo da opção selecionada e destaques do paciente |
| **Creme** `#FEF3C7` | Fundo da classe prevista no resultado e fundo das mensagens de aviso |
| **Azul-noite** `#0F172A` | Títulos, textos principais, traço do desenho e logotipo |
| **Branco** `#FFFFFF` | Cartões, diálogos, campos e a área de desenho |

### Neutros e superfícies

| Nome | Cor | Para que serve |
|---|---|---|
| Fundo do aplicativo | `#E8EBF8` | Fundo das telas do profissional e das telas de tarefa |
| Fundo acolhedor | `#FFF7ED` | Fundo das telas do paciente fora da tarefa (encerramento e termo) |
| Superfície | `#FFFFFF` | Cartões, diálogos e área de desenho |
| Superfície suave | `#F3F4FC` | Fundo de campo, opção não selecionada e blocos de registro |
| Texto principal | `#0F172A` | Títulos e textos |
| Texto secundário | `#475569` | Descrições, rótulos e textos de apoio |
| Texto de exemplo | `#5B6B82` | O texto de exemplo dentro de um campo vazio (*placeholder*) |
| Borda de controle | `#64748B` | Borda de campo, de opção e de caixa de seleção |
| Borda decorativa | `#CBD5E1` | Borda de cartão e da área de desenho |
| Divisória | `#E2E8F0` | Linhas que separam conteúdos |
| Véu do diálogo | `rgba(15, 23, 42, 0.45)` | Escurece a tela atrás de um diálogo |

!!! info "Por que o texto de exemplo e a borda dos campos são mais escuros"
    A WCAG pede contraste de pelo menos 4,5:1 para texto e 3:1 para a borda de um controle. Tons claros comuns nesses lugares, como `#94A3B8` e `#CBD5E1`, ficam em 2,3:1 e 1,4:1 sobre o fundo do campo. Com `#5B6B82` e `#64748B`, os valores passam para 5,0:1 e 4,3:1. A borda decorativa `#CBD5E1` continua valendo para cartões, que não são controles.

### Cores de mensagem

Cada tipo de mensagem tem uma cor de texto e ícone, uma cor de fundo e **sempre um ícone e um texto**. A cor nunca é a única pista, porque parte dos usuários não distingue bem as cores.

<div class="feedback-grid">
  <div class="feedback feedback--sucesso" markdown="span">:material-check-circle: <b>Sucesso.</b> Profissional cadastrado.</div>
  <div class="feedback feedback--aviso" markdown="span">:material-alert: <b>Aviso.</b> A bateria do tablet está fraca.</div>
  <div class="feedback feedback--erro" markdown="span">:material-close-circle: <b>Erro.</b> O CPF informado não é válido.</div>
  <div class="feedback feedback--info" markdown="span">:material-information: <b>Informação.</b> O arquivo XML foi salvo na pasta escolhida.</div>
</div>

| Tipo | Texto e ícone | Fundo | Contraste | Ícone | Quando usar |
|---|---|---|---|---|---|
| **Sucesso** | `#166534` | `#DCFCE7` | 6,5:1 | `check-circle` | Uma ação terminou bem: conta criada, arquivo salvo, exame concluído |
| **Aviso** | `#92400E` | `#FEF3C7` | 6,4:1 | `alert` | Algo pede atenção, mas não impede de continuar |
| **Erro** | `#B91C1C` | `#FEE2E2` | 5,3:1 | `close-circle` | Algo deu errado ou um dado está incorreto e precisa ser corrigido |
| **Informação** | `#1E40AF` | `#DBEAFE` | 7,2:1 | `information` | Um fato útil, sem pedir ação |

Duas cores têm papel fixo fora das mensagens:

- **Verde de conclusão** `#15803D`, com o ícone branco por cima (contraste de 5,0:1), só no grande sinal de "Terminou!" do paciente.
- **Atenção alta no resultado** `#B91C1C`, para marcar no resultado as figuras em que o modelo encontrou alterações. É o mesmo vermelho do erro, mas aparece sempre com o rótulo escrito ("Alta atenção"), nunca sozinho.

### Modo escuro

As telas do profissional seguem o tema do tablet, claro ou escuro. No modo escuro, o laranja da marca fica escuro demais (contraste de 2,4:1 sobre o fundo escuro), então ele é trocado por um laranja claro.

| Papel | Claro | Escuro | Contraste no escuro |
|---|---|---|---|
| Ação principal | `#9A3412` com texto branco | `#FDBA74` com texto `#0F172A` | 10,6:1 |
| Fundo | `#E8EBF8` | `#0F172A` | — |
| Superfície | `#FFFFFF` | `#1E293B` | — |
| Texto principal | `#0F172A` | `#E2E8F0` | 11,9:1 |
| Texto secundário | `#475569` | `#94A3B8` | 7,0:1 |
| Sucesso | `#166534` | `#86EFAC` | 10,4:1 |
| Aviso | `#92400E` | `#FCD34D` | 10,2:1 |
| Erro | `#B91C1C` | `#FCA5A5` | 7,7:1 |
| Informação | `#1E40AF` | `#93C5FD` | 8,1:1 |

!!! note "As telas do paciente são sempre claras"
    As telas de termo, instrução, desenho e encerramento usam sempre o modo claro, mesmo com o tablet no modo escuro. Assim a área de desenho é igual para todos os pacientes e o traço azul-noite fica sempre sobre o branco.

## Espaçamento, forma e profundidade

### Espaçamento

Todos os espaços são múltiplos de **4**, e de preferência de **8**: `4 · 8 · 12 · 16 · 24 · 32 · 48 · 64`.

| Onde | Espaço |
|---|---|
| Entre o rótulo e o campo | 8 |
| Entre campos e entre botões vizinhos | 16 |
| Entre grupos de conteúdo | 24 |
| Margem interna de cartão e diálogo | 32 (paciente: 48) |
| Margem da tela | 40 |

### Cantos arredondados

| Elemento | Raio |
|---|---|
| Campo, opção de escolha, chip e bloco de mensagem | 12 |
| Botão | 16 |
| Cartão e área de desenho | 24 |
| Diálogo e cartão principal de tela | 28 |
| Chip de seleção (formato de pílula) | 999 |

### Sombras

| Nível | Sombra | Onde |
|---|---|---|
| 1 | `0 4 16 rgba(15, 23, 41, 0.06)` | Área de desenho |
| 2 | `0 6 20 rgba(15, 23, 41, 0.08)` | Cartões |
| 3 | `0 10 32 rgba(15, 23, 41, 0.12)` | Cartão principal da tela (login, cadastro, encerramento) |
| 4 | `0 14 40 rgba(15, 23, 41, 0.30)` | Diálogos, sempre com o véu atrás |

## Botões

### Tipos

<div class="button-row">
  <span class="btn-sample btn-primario">Criar conta</span>
  <span class="btn-sample btn-secundario">Exportar XML</span>
  <span class="btn-sample btn-destrutivo">Apagar</span>
  <span class="btn-sample btn-destrutivo-contorno">Sim, desistir</span>
  <span class="btn-sample btn-discreto">Desistir do exame</span>
  <span class="btn-sample btn-texto">Já tenho conta</span>
</div>

| Tipo | Aparência | Quando usar |
|---|---|---|
| **Primário** | Fundo laranja `#9A3412`, texto branco | A ação principal da tela. **Só um por tela ou diálogo.** Ex.: "Criar conta", "Confirmar", "Começar", "Continuar o exame" |
| **Secundário** | Fundo branco, contorno de 2 dp e texto em laranja | Ações alternativas. Ex.: "Desfazer", "Exportar XML", "Cancelar" |
| **Destrutivo** | Fundo vinho `#7F1D1D`, texto branco | Confirmar algo que apaga ou encerra, dentro de um diálogo. Ex.: "Apagar", "Excluir paciente", "Confirmar recusa" |
| **Destrutivo de contorno** | Fundo branco, contorno e texto em vinho | Quando a saída destrutiva não é a ação recomendada. Ex.: "Sim, desistir", ao lado de "Continuar o exame" |
| **Discreto** | Fundo `#F3F4FC`, borda `#64748B` e texto `#475569` | Ação rara e de baixa prioridade, que não deve chamar a atenção do paciente. Ex.: "Desistir do exame" na tela de desenho |
| **De texto** | Sem fundo, texto em laranja e sublinhado ao pressionar | Navegação secundária. Ex.: "Já tenho conta, entrar", "Esqueci a senha" |

### Tamanhos

| Tamanho | Altura | Texto | Onde usar |
|---|---|---|---|
| **Médio** | 64 dp | Botão 20 | Telas do profissional |
| **Grande** | 84 dp | Botão 26 | Telas do paciente e diálogos que o paciente vê |
| **Extragrande** | 112 dp | Botão 26 | Só o "Confirmar" da tela de desenho, que é a ação mais importante do paciente |

Nenhum alvo de toque pode ter menos de **48 × 48 dp**, mesmo os botões de texto e os ícones.

### Estados

| Estado | Como fica |
|---|---|
| Normal | Como descrito acima |
| Pressionado | Cor de fundo 10% mais escura (primário `#7C2D12`, destrutivo `#651515`) ou fundo pêssego claro nos botões de contorno |
| Foco do teclado | Anel de 3 dp em `#1E40AF` por fora do botão |
| Desabilitado | Fundo `#E2E8F0` e texto `#475569`, sem sombra. Sempre explicar perto do botão o que falta para habilitá-lo |
| Carregando | O texto troca por um indicador giratório e a palavra da ação no gerúndio ("Salvando"). O botão não aceita um segundo toque |

### Ordem dos botões

- Nas telas do profissional e nos diálogos, os botões ficam lado a lado, alinhados à direita, com o **primário (ou destrutivo) por último**, à direita.
- Na tela de desenho, os botões ficam empilhados na coluna da direita: os de edição em cima ("Desfazer", "Apagar tudo") e o "Confirmar" embaixo, separado, para não ser tocado sem querer.
- O texto do botão diz **exatamente o que acontece**: "Apagar desenho", e não "Sim" ou "OK".

## Campos e escolhas

### Campo de texto

- **Rótulo sempre visível acima do campo**, no estilo rótulo pequeno. O texto de exemplo dentro do campo não substitui o rótulo, porque some quando a pessoa começa a digitar.
- Altura de **60 dp**, fundo `#F3F4FC`, borda de 1,5 dp em `#64748B`, cantos de 12 e texto no estilo corpo médio.
- **Com foco:** borda de 2 dp em laranja `#9A3412`.
- **Com erro:** borda de 2 dp em `#B91C1C` e, logo abaixo do campo, o ícone `close-circle` com a mensagem no estilo corpo pequeno, também em `#B91C1C`.
- Campos de senha têm um botão de mostrar e esconder a senha (ícones `eye` e `eye-off`).

### Opção de escolha (Sim ou Não)

Usada para respostas de sim ou não, como no termo de consentimento.

- Altura de **56 dp**, cantos de 12, texto no estilo rótulo grande.
- **Selecionada:** fundo pêssego claro `#FFE8D6`, borda de 2 dp e texto em laranja, com o círculo de seleção preenchido.
- **Não selecionada:** fundo `#F3F4FC`, texto `#475569` e o círculo vazio com borda `#64748B`.

### Chip de seleção

Usado para escolher um motivo, como no diálogo de desistência.

- Formato de pílula, altura de **48 dp** e texto no estilo rótulo pequeno.
- **Selecionado:** fundo laranja e texto branco. **Não selecionado:** fundo branco, borda `#64748B` e texto `#475569`.

## Mensagens e diálogos

O aplicativo **não usa o alerta padrão do Android** (o `Alert.alert`), aquela caixa branca que não deixa claro se é erro, aviso ou confirmação. No lugar dele, usa estes quatro formatos:

| Formato | Quando usar | Exemplo |
|---|---|---|
| **Erro no campo** | Um dado digitado está errado. A mensagem aparece embaixo do próprio campo, e todos os erros do formulário aparecem de uma vez | "Informe um CPF válido, com 11 números." |
| **Faixa de mensagem** | Algo sobre a tela toda, como um erro ao salvar ou um aviso. Fica no topo do conteúdo, com a cor e o ícone do tipo, até a pessoa resolver ou fechar | "Não foi possível salvar. Tente de novo." |
| **Diálogo de confirmação** | Antes de uma ação que apaga, encerra ou não pode ser desfeita. Tem título em forma de pergunta, uma frase com a consequência e dois botões | "Apagar o desenho?" · "Tudo o que foi desenhado nesta tarefa será apagado." · Cancelar / Apagar desenho |
| **Aviso rápido** | Confirmar que uma ação terminou bem. Aparece embaixo, some sozinho em 4 segundos e não tem botão | "Arquivo XML salvo." |

**Como escrever uma mensagem:**

- Diga o que aconteceu e como resolver, nesta ordem: "O e-mail já está cadastrado. Entre com a sua senha ou use outro e-mail."
- Não culpe o usuário ("Você digitou errado") e não use termos técnicos ("Erro 500", "falha de validação").
- Não use ponto de exclamação em mensagem de erro.
- **No login, a mensagem é sempre a mesma**, "E-mail ou senha inválidos.", para não revelar quais e-mails estão cadastrados.

### Blocos de registro

Blocos de registro avisam que algo ficou registrado para a pesquisa, como "Registrado: apagamento registrado nesta tarefa, com o horário" e "Parou em: a tarefa atual fica registrada como ponto de parada". Esses blocos são do tipo **informação neutra**: fundo `#F3F4FC` (ou pêssego claro nas telas do paciente), rótulo curto em caixa alta e em laranja, e o texto no estilo corpo médio em `#475569`.

### Faixa "Este resultado não é diagnóstico"

A faixa vinho no topo do resultado é obrigatória em toda tela que mostra o resultado do modelo. Ela usa o vinho `#7F1D1D` com o texto branco (contraste de 10,0:1) e o ícone `alert-octagon`.

## Ícones

### Biblioteca

O aplicativo usa uma única biblioteca, a **Material Design Icons**. No código, ela vem pelo `MaterialCommunityIcons`, do pacote `@expo/vector-icons`, que já faz parte do Expo. No site de documentação, os mesmos ícones aparecem com a sintaxe `:material-nome:`, o que facilita mostrar no guia exatamente o ícone que vai no app.

### Regras

- **Todo ícone tem um rótulo escrito ao lado.** Ícone sozinho só é permitido quando o significado é universal e existe um rótulo de acessibilidade para o leitor de tela (por exemplo, o olho de mostrar a senha).
- Ações e navegação usam a versão **de contorno** (`-outline`). Estados e mensagens usam a versão **preenchida**.
- Tamanhos: **24 dp** como padrão, **20 dp** dentro de botões, à esquerda do texto, e **32 a 48 dp** nos destaques das telas do paciente.
- O ícone usa a mesma cor do texto ao lado dele.

### Ícones definidos

| Ação ou significado | Ícone | Nome |
|---|---|---|
| Início | :material-home-outline: | `home-outline` |
| Novo exame | :material-clipboard-plus-outline: | `clipboard-plus-outline` |
| Paciente | :material-account-outline: | `account-outline` |
| Lista de pacientes | :material-account-group-outline: | `account-group-outline` |
| Exportar XML | :material-file-export-outline: | `file-export-outline` |
| Configurações | :material-cog-outline: | `cog-outline` |
| Sair da conta | :material-logout: | `logout` |
| Excluir | :material-trash-can-outline: | `trash-can-outline` |
| Desfazer | :material-undo: | `undo` |
| Apagar tudo | :material-eraser: | `eraser` |
| Confirmar | :material-check: | `check` |
| Chamar o profissional | :material-hand-back-right-outline: | `hand-back-right-outline` |
| Desistir do exame | :material-exit-run: | `exit-run` |
| Registrar discordância | :material-comment-alert-outline: | `comment-alert-outline` |
| Sincronizar tablets | :material-sync: | `sync` |
| Mostrar e esconder a senha | :material-eye-outline: :material-eye-off-outline: | `eye-outline`, `eye-off-outline` |
| Sucesso | :material-check-circle: | `check-circle` |
| Aviso | :material-alert: | `alert` |
| Erro | :material-close-circle: | `close-circle` |
| Informação | :material-information: | `information` |
| Resultado não é diagnóstico | :material-alert-octagon: | `alert-octagon` |
| Tarefa do relógio | :material-clock-outline: | `clock-outline` |
| Tarefa do cubo | :material-cube-outline: | `cube-outline` |

O ícone da terceira tarefa será definido quando a figura dessa tarefa for confirmada com o cliente.

## Padrões de tela

### Telas do profissional

- **Barra superior** branca, com 64 dp de altura, mostrando à esquerda quem é o paciente e quem aplica, e à direita a etapa atual.
- Conteúdo em cartões brancos sobre o fundo `#E8EBF8`.
- Texto no estilo corpo médio, botões médios.

### Telas do paciente

- **Uma ação principal por tela**, em botão grande ou extragrande.
- Texto no estilo corpo grande. Nenhum texto menor que 20.
- **Nunca mostrar** escore, classe, probabilidade nem qualquer informação de tempo.
- **Indicador de progresso** na barra superior: um círculo de 16 dp por tarefa (o atual em laranja, os outros em `#CBD5E1`) e o texto "Tarefa 1 de 3".
- A frase de ajuda "Se precisar de ajuda, chame o profissional" usa o estilo rótulo grande, para o paciente conseguir ler.

### Área de desenho

- Fundo branco, borda decorativa de 2 dp em `#CBD5E1`, cantos de 24 e sombra de nível 1.
- O traço do paciente é azul-noite `#0F172A`, com espessura de 4 a 6 dp.
- Nada dentro da área além do que o paciente desenha. A instrução e a figura de referência ficam fora dela.

## Acessibilidade

- **Contraste mínimo:** 4,5:1 para texto, 3:1 para texto grande (24 ou mais, ou 19 em negrito) e 3:1 para bordas de controles e ícones. Todas as combinações deste guia foram conferidas.
- **Alvo de toque** de pelo menos 48 × 48 dp, com pelo menos 8 dp entre alvos vizinhos.
- **A cor nunca é a única pista:** estados e mensagens sempre têm ícone e texto.
- **Rótulo de acessibilidade** em todo botão e ícone, para o leitor de tela (TalkBack).
- **Instruções curtas e diretas**, com uma ação por etapa.
- O layout continua funcionando com a letra ampliada pelo Android, sem cortar texto nem esconder botões.
- Foco visível em todos os elementos que podem ser selecionados.
- Antes de consolidar a identidade, testar com profissionais e com idosos.

## Tokens para o código

Os valores deste guia viram constantes no arquivo `src/constants/theme.ts` do aplicativo. A implementação é uma tarefa à parte, no repositório do aplicativo. O formato proposto é este:

```ts
export const Brand = {
  orange: '#9A3412',       // ação principal
  orangeDark: '#7C2D12',   // pressionado e texto sobre pêssego
  wine: '#7F1D1D',         // destrutivo e faixa de aviso do resultado
  peach: '#FFE8D6',
  cream: '#FEF3C7',
  midnight: '#0F172A',
  white: '#FFFFFF',
} as const;

export const Colors = {
  light: {
    primary: '#9A3412', onPrimary: '#FFFFFF', primaryPressed: '#7C2D12',
    destructive: '#7F1D1D', onDestructive: '#FFFFFF',
    background: '#E8EBF8', backgroundWarm: '#FFF7ED',
    surface: '#FFFFFF', surfaceSoft: '#F3F4FC',
    text: '#0F172A', textSecondary: '#475569', placeholder: '#5B6B82',
    borderControl: '#64748B', borderDecorative: '#CBD5E1', divider: '#E2E8F0',
    focus: '#1E40AF', scrim: 'rgba(15, 23, 42, 0.45)',
    success: '#166534', successBg: '#DCFCE7',
    warning: '#92400E', warningBg: '#FEF3C7',
    error: '#B91C1C', errorBg: '#FEE2E2',
    info: '#1E40AF', infoBg: '#DBEAFE',
  },
  dark: {
    primary: '#FDBA74', onPrimary: '#0F172A', primaryPressed: '#FB923C',
    destructive: '#F87171', onDestructive: '#0F172A',
    background: '#0F172A', backgroundWarm: '#0F172A',
    surface: '#1E293B', surfaceSoft: '#334155',
    text: '#E2E8F0', textSecondary: '#94A3B8', placeholder: '#CBD5E1',
    borderControl: '#94A3B8', borderDecorative: '#475569', divider: '#334155',
    focus: '#93C5FD', scrim: 'rgba(0, 0, 0, 0.6)',
    success: '#86EFAC', successBg: '#14532D',
    warning: '#FCD34D', warningBg: '#78350F',
    error: '#FCA5A5', errorBg: '#7F1D1D',
    info: '#93C5FD', infoBg: '#1E3A8A',
  },
} as const;

export const FontFamilies = {
  display: 'Outfit_600SemiBold', displayBold: 'Outfit_700Bold', label: 'Outfit_500Medium',
  regular: 'Inter_400Regular', semibold: 'Inter_600SemiBold',
} as const;

export const Type = {
  titleHuge:  { fontFamily: 'Outfit_700Bold',     fontSize: 72, lineHeight: 80 },
  titleMd:    { fontFamily: 'Outfit_600SemiBold', fontSize: 34, lineHeight: 42 },
  titleSm:    { fontFamily: 'Outfit_600SemiBold', fontSize: 24, lineHeight: 32 },
  buttonLg:   { fontFamily: 'Outfit_600SemiBold', fontSize: 26, lineHeight: 32 },
  buttonMd:   { fontFamily: 'Outfit_600SemiBold', fontSize: 20, lineHeight: 26 },
  labelLg:    { fontFamily: 'Outfit_500Medium',   fontSize: 20, lineHeight: 26 },
  labelSm:    { fontFamily: 'Outfit_500Medium',   fontSize: 16, lineHeight: 22 },
  bodyLg:     { fontFamily: 'Inter_400Regular',   fontSize: 24, lineHeight: 36 },
  bodyMd:     { fontFamily: 'Inter_400Regular',   fontSize: 18, lineHeight: 28 },
  bodySm:     { fontFamily: 'Inter_400Regular',   fontSize: 16, lineHeight: 24 },
} as const;

export const Spacing = { xs: 4, sm: 8, md: 12, lg: 16, xl: 24, xxl: 32, xxxl: 48, huge: 64 } as const;
export const Radius = { control: 12, button: 16, card: 24, dialog: 28, pill: 999 } as const;
export const ButtonHeight = { md: 64, lg: 84, xl: 112 } as const;
```

## Lista de verificação

Antes de aprovar uma tela desenhada ou um PR com interface:

- [ ] As cores são todas deste guia, sem nenhuma cor nova.
- [ ] Títulos e botões estão com maiúscula só no início.
- [ ] Nenhum texto tem menos de 16 dp (20 nas telas do paciente).
- [ ] Existe só um botão primário na tela.
- [ ] Ações destrutivas usam o vinho e passam por um diálogo de confirmação.
- [ ] Todo campo tem rótulo visível e estado de erro.
- [ ] Mensagens usam um dos quatro formatos, com ícone, e não o alerta padrão.
- [ ] Todo ícone tem rótulo escrito ou rótulo de acessibilidade.
- [ ] Todos os alvos de toque têm pelo menos 48 × 48 dp.
- [ ] As telas do paciente não mostram escore, classe, probabilidade nem tempo.

## Pendências

- Aprovar o logotipo definitivo com o cliente e registrar aqui as versões horizontal, monocromática e reduzida.
- Definir o ícone da terceira tarefa.
- Implementar os tokens no `theme.ts` e trocar o alerta padrão do Android pelos componentes de mensagem.
- Validar as fontes, as cores e os tamanhos em testes com profissionais de saúde e com idosos.

## Referências

### Acessibilidade e legislação

1. W3C. **Web Content Accessibility Guidelines (WCAG) 2.2**. World Wide Web Consortium, 2023. Disponível em: <https://www.w3.org/TR/WCAG22/>.
2. W3C. **Understanding SC 1.4.3: Contrast (Minimum)**. Disponível em: <https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html>.
3. W3C. **Understanding SC 1.4.11: Non-text Contrast**. Disponível em: <https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html>.
4. W3C. **Understanding SC 1.4.1: Use of Color**. Disponível em: <https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html>.
5. W3C. **Understanding SC 2.5.8: Target Size (Minimum)**. Disponível em: <https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html>.
6. W3C WAI. **Older Users and Web Accessibility: Meeting the Needs of Ageing Web Users**. Disponível em: <https://www.w3.org/WAI/older-users/>.
7. BRASIL. Ministério do Planejamento, Orçamento e Gestão. **eMAG: Modelo de Acessibilidade em Governo Eletrônico**, versão 3.1. Brasília, 2014. Disponível em: <https://emag.governoeletronico.gov.br/>.
8. BRASIL. **Lei nº 13.146, de 6 de julho de 2015**. Institui a Lei Brasileira de Inclusão da Pessoa com Deficiência (Estatuto da Pessoa com Deficiência). Disponível em: <https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13146.htm>.
9. ANDROID DEVELOPERS. **Make apps more accessible**. Google. Disponível em: <https://developer.android.com/guide/topics/ui/accessibility/apps>.
10. GOOGLE. **Android Accessibility Help: touch target size**. Disponível em: <https://support.google.com/accessibility/android/answer/7101858>.

### Ergonomia, leitura e público idoso

11. INTERNATIONAL ORGANIZATION FOR STANDARDIZATION. **ISO 9241-112:2017**: Ergonomics of human-system interaction — Part 112: Principles for the presentation of information. Genebra: ISO, 2017.
12. INTERNATIONAL ORGANIZATION FOR STANDARDIZATION. **ISO 9241-171:2008**: Ergonomics of human-system interaction — Part 171: Guidance on software accessibility. Genebra: ISO, 2008.
13. TINKER, M. A. **Legibility of Print**. Ames: Iowa State University Press, 1963.
14. NIELSEN, J. **Usability for Senior Citizens: Improved, But Still Lacking**. Nielsen Norman Group, 2013. Disponível em: <https://www.nngroup.com/articles/usability-for-senior-citizens/>.

### Sistema de design, fontes e ícones

15. GOOGLE. **Material Design 3: Color roles**. Disponível em: <https://m3.material.io/styles/color/roles>.
16. GOOGLE. **Material Design 3: Typography**. Disponível em: <https://m3.material.io/styles/typography/overview>.
17. GOOGLE. **Material Design 3: Buttons**. Disponível em: <https://m3.material.io/components/buttons/overview>.
18. GOOGLE. **Material Design 3: Dialogs**. Disponível em: <https://m3.material.io/components/dialogs/overview>.
19. FUENZALIDA, R. **Outfit**. Google Fonts. Disponível em: <https://fonts.google.com/specimen/Outfit>.
20. ANDERSSON, R. **Inter**. Google Fonts. Disponível em: <https://fonts.google.com/specimen/Inter>.
21. PICTOGRAMMERS. **Material Design Icons**. Disponível em: <https://pictogrammers.com/library/mdi/>.
22. EXPO. **Icons (`@expo/vector-icons`)**. Disponível em: <https://docs.expo.dev/guides/icons/>.
23. EXPO. **Fonts**. Disponível em: <https://docs.expo.dev/develop/user-interface/fonts/>.

### Ferramentas usadas na conferência

24. WEBAIM. **Contrast Checker**. Disponível em: <https://webaim.org/resources/contrastchecker/>. Os valores de contraste deste guia foram calculados com a fórmula de luminância relativa da WCAG 2.2.

## Histórico de versões

| Versão | Descrição | Autor | Data | Revisor | Data de revisão |
|---|---|---|---|---|---|
| 1.0 | Criação da identidade visual inicial a partir do questionário do cliente, do protótipo e da paleta fornecida | [Mach1r0](https://github.com/Mach1r0) | 22/09/2026 | [Eduardo Ferreira](https://github.com/eduardoferre) | 23/09/2026 |
| 1.1 | Alinhamento das definições ao protótipo: adoção da fonte Inter, inclusão do Figma e simplificação das seções | [Mach1r0](https://github.com/Mach1r0) | 22/09/2026 | [Eduardo Ferreira](https://github.com/eduardoferre) | 23/09/2026 |
| 1.2 | Remoção da incorporação protegida do Figma e documentação do uso das cores nas telas | [Mach1r0](https://github.com/Mach1r0) | 22/09/2026 | [Eduardo Ferreira](https://github.com/eduardoferre) | 23/09/2026 |
| 2.0 | Guia completo da identidade visual: logotipo, tipografia com Outfit e Inter e escala de texto, paleta, neutros e cores de mensagem com contraste conferido, modo escuro, espaçamento, cantos e sombras, botões, campos, mensagens, ícones, padrões de tela, acessibilidade, tokens para o código, lista de verificação e referências | [Gabriel Lopes de Amorim](https://github.com/BrzGab) | 05/10/2026 | | |
