# 📘 README EXTRA — Melhorias de Front-end e Guia de Boas Práticas

> Complementa o `README.md` e o `Structure.md`. Aqui está **o que foi alterado no front-end** (e por quê) e um **guia com dicas para os próximos projetos**.
> Stack deste projeto: **Python + Flask + Jinja2 + Bootstrap 5 + SQLite**.

---

## 1. Resumo do que foi feito

**Escopo combinado:** somente front-end; corrigir botões que eram tag `<a>` (ou o contrário), erros de responsividade e adicionar animações, **sem mudar o design**.

**Não foi tocado:** `app.py`, `banco.py`, `routes/`, banco de dados, `Test/`, `login.html`, `cadastro.html`.

### Arquivos alterados

| Arquivo | O que mudou |
|---|---|
| `templates/dashboard.html`, `equipamentos.html`, `movimentacao.html`, `createitem.html`, `createmov.html` | Classes `app-layout` / `app-content`; logo agora leva ao Início; "Sair" virou `<form POST>` + `<button>`; botão do menu do usuário com `type`, `aria-label`, `aria-expanded`; `<link>` para `responsivo.css` e `animacoes.css` |
| `templates/equipamentos.html`, `movimentacao.html` | `<button><a>` virou `<a class="btn">`; "Filtrar" virou `.btn`; botão ⋮ com `type="button"` e `aria-label`. Em Movimentações o texto foi de "+ Adicionar Equipamento" para "+ Nova Movimentação" (o link vai para a tela de nova movimentação) |
| `templates/createitem.html` | `</form>` que faltava; "Adicionar Categoria" com `type="button"` |
| `templates/historico.html` | Atributos nos botões, classe `main-historico`, novos `<link>` |
| `templates/dashboard.html` | Também carrega `static/js/animacoes.js` |
| `static/js/script.js` | Posição do menu ⋮ corrigida; `aria-expanded` no menu do usuário |
| `static/css/class.css` | `.tabela-container`: `width:auto` e `overflow-x:auto` |
| `static/css/style1.css` | Removida regra morta `.ballons-all { width: 90px }` |
| `static/css/dashboard.css` | `.ballons-all { max-width: 100% }` |

### Arquivos novos

| Arquivo | Função |
|---|---|
| `static/css/responsivo.css` | Todas as correções de responsividade, comentadas bloco a bloco |
| `static/css/animacoes.css` | Animações e transições |
| `static/js/animacoes.js` | Contagem animada dos números do dashboard |
| `README_EXTRA.md` | Este documento |

> 💡 Sugestão: acrescente os arquivos novos à lista de pastas do `Structure.md`.
> Para **desfazer** qualquer parte: remova o `<link>` / `<script>` correspondente nos templates.

---

## 2. Botões: `<a>` ou `<button>`?

**Regra de bolso**

| Se o elemento… | Use | Exemplo neste projeto |
|---|---|---|
| **leva para outra página** (GET) | `<a href>` (pode ter aparência de botão: `class="btn btn-primary"`) | Nova Movimentação, Novo Equipamento |
| **executa uma ação** (envia formulário, altera dados, abre menu) | `<button>` | Sair, Filtrar, Emprestar, ⋮ |
| **nunca** | `<button><a>…</a></button>` ou `<a><button>…</button></a>` (HTML inválido) | — |

### Problemas encontrados e corrigidos

1. **"Sair" da sidebar era `<a>`** → fazia GET, mas a rota `/logout` só aceita POST, resultando em **erro 405**. Agora é `<form method="POST">` com `<button>`, com o mesmo visual. Ao ser corrigido, o logout também encerra a sessão corretamente.
2. **`<button><a>+ Adicionar…</a></button>`** (Equipamentos e Movimentações): só o texto clicava, e o visual saía de link sublinhado sobre fundo cinza. Agora é um `<a class="btn btn-primary">` único.
3. **"Adicionar Categoria" enviava o formulário errado**: o `<form>` acima dele nunca era fechado, então o navegador tratava o botão como parte dele (e, por padrão, `<button>` é `type="submit"`). Corrigido fechando o `</form>` e usando `type="button"`.
4. **Menu ⋮ das tabelas aparecia longe do botão** com a página rolada: o menu é `position: fixed` (coordenadas da janela), mas o JS somava `window.scrollY`. Corrigido, com limite de tela e inversão para cima quando falta espaço embaixo.
5. **"Filtrar" ilegível**: texto branco em fundo cinza. Agora usa o mesmo `.btn-primary` dos outros botões.
6. **Acessibilidade**: `<a href="">` no logo (recarregava a mesma página) agora aponta para o Início; botões só com ícone ganharam `aria-label`; `<i alt="…">` (atributo inválido) virou `aria-hidden`.

> ⚠️ **Sempre defina `type` em `<button>`.** Dentro de um `<form>`, sem `type` ele vira `submit`.

---

## 3. Responsividade

### Causas encontradas → correção

| Problema | Causa | Correção |
|---|---|---|
| Conteúdo cortado à direita em telas ≤ 1000px; colunas **Status** e **Ações** inalcançáveis | `.tabela-container` com `overflow:hidden` + `width:100%` + `margin:20px`; item flex sem `min-width:0`; `body{overflow-x:hidden}` escondia o problema | `overflow-x:auto` (a tabela rola dentro do card), `width:auto`, `min-width:0` |
| No celular a sidebar ocupava ~50% da tela | Largura fixa e `vh-100` em qualquer tamanho | Até 768px vira barra no topo (só CSS) |
| Cabeçalho estourava com nome de usuário longo | `header{height:100px}` fixo | `min-height`, `flex-wrap`, nome com reticências no celular |
| Filtros de busca saíam da tela | `.barra-pesquisa` sem quebra de linha | `flex-wrap` até 768px |
| "Novo Equipamento": segunda coluna cortada | `<main>` flex sem quebra | `flex-wrap` até 992px |
| Cards do dashboard | Regra `width:90px` nunca aplicava (era sobrescrita), mas cortaria o texto se aplicasse | Removida; cards com `max-width:100%` |

**Pontos de quebra usados:** 992px, 768px, 576px.

### Como foi testado
Chromium (Playwright) em **375, 768, 1024 e 1440px** nas 6 páginas internas, medindo elementos que passam da largura da tela: **zero após as correções**. No desktop (1440px), Dashboard, Novo Equipamento e Nova Movimentação ficaram **idênticos pixel a pixel**; Equipamentos, Movimentações e Histórico mudam só nos botões corrigidos e no alinhamento da tabela (antes deslocada 20px).

> ✅ Teste também no seu navegador e num celular real.

### Como testar sozinho
`F12` → botão de dispositivo (`Ctrl+Shift+M`) → teste 375, 768, 1024, 1440. Checklist: sem rolagem horizontal na página · botões clicáveis com o dedo (≥ 44px de altura) · tabela rola dentro do card · textos longos não quebram o layout.

> ⚠️ `overflow-x: hidden` no `body` (em `index.css`) **esconde** bugs de layout em vez de resolvê-los. Use só depois de achar a causa.

---

## 4. Animações

### Já implementadas (`animacoes.css` / `animacoes.js`)

| O quê | Onde | Técnica |
|---|---|---|
| Cards entram em cascata (0,08s entre cada) | Dashboard | `@keyframes` + `animation-delay` |
| Card "levanta" ao passar o mouse | Dashboard | `transition` em `transform` e `box-shadow` |
| Números contam de 0 até o valor | Dashboard | `requestAnimationFrame` com easing (`animacoes.js`) |
| Botões reagem ao hover e ao clique | Todos os `.btn` | `transform` |
| Menus (usuário e ⋮) abrem com fade + leve deslize | Todas as páginas | `opacity` + `visibility` (em vez de `display:none`) |
| Janelas `<dialog>` aparecem com fade | Equipamentos, Movimentações, Nova Movimentação | `dialog[open]` |
| Fade-in da página | Todas | `opacity` |

**Regras seguidas:** animar apenas `transform` e `opacity` (baratos para o navegador) · durações de 150 a 500 ms · respeitar `prefers-reduced-motion` (quem desativa animações no sistema não vê nenhuma).

### Pegadinhas que apareceram (vale guardar)

- **`animation-fill-mode: both/forwards` "trava" o estado final** e o `:hover` deixa de funcionar. Usamos `backwards`.
- **`transform` num ancestral quebra `position: fixed`**: os menus ⋮ são fixos, então a animação da página usa só `opacity`.
- **`display:none` não anima.** Para animar abrir/fechar, alterne `opacity` + `visibility`.
- O `<dialog>` já usa `transform` para centralizar; por isso a animação dele usa a propriedade `scale` (que não conflita).

### Ideias para as próximas versões

1. **Estado de carregamento no botão** ao enviar formulário (evita clique duplo):
   ```js
   form.addEventListener('submit', () => { btn.disabled = true; btn.textContent = 'Enviando…'; });
   ```
2. **Skeleton** (blocos cinzas pulsando) enquanto a tabela carrega, quando os dados passarem a vir via `fetch`.
3. **Feedback de sucesso/erro** com *toast* (Bootstrap `.toast`) que aparece e some sozinho, no lugar de recarregar a página em silêncio.
4. **Barras/gráficos** animados com **Chart.js** para mostrar Disponíveis × Em Uso × Manutenção no dashboard.
5. **Destaque da linha alterada**: após emprestar/devolver, a linha pisca uma cor por 1 segundo.
6. **Transição entre páginas** com a *View Transitions API* (`@view-transition { navigation: auto; }`). O suporte varia por navegador, então use como melhoria opcional.
7. Use o painel **Animations** do DevTools para desacelerar e depurar.

---

## 5. Observações para o backlog (não foram alteradas)

- Em **Movimentações** o badge "Pendente/Devolvido" fica **branco sobre branco**: os `#emuso` / `#disponivel` estão em `equipamentos.css`, que essa página não carrega.
- `createmov.html` **não carrega `class.css`**, então a tabela fica sem estilo.
- `banco.py` abre `Database_Controle.db`, mas o arquivo se chama `database_controle.db`. Funciona no Windows e **quebra no Linux** (diferencia maiúsculas).
- `app.secret_key` está fixa no código. Use variável de ambiente (`os.environ`) e não a publique no GitHub.
- Os botões de POST (logout, excluir, devolver) não têm **token CSRF**. Considere `Flask-WTF` (`CSRFProtect`).
- "Perfil" e "Esqueceu a senha?" ainda não fazem nada.
- O bloco de **sidebar + header está copiado em 5 templates**. Um `base.html` com `{% extends %}` e `{% block content %}` elimina a repetição (e teria evitado o bug do "Sair" em 5 lugares).
- Referências de CSS/JS usam `../static/...`; o ideal é `{{ url_for('static', filename='css/x.css') }}`.
- Ids repetidos em `createitem.html` (`createInput` aparece mais de uma vez) e o título "Dashboad - Moderno" (com erro de digitação) repetido nas páginas internas.

---

## 6. Como documentar: antes, durante e depois

### 🟦 ANTES (planejar em papel)
Uma página basta. Responda:
- **Problema e público**: quem usa (supervisores do N.T.I.), o que precisa resolver.
- **Escopo e fora de escopo**: o que **não** vai ser feito agora (evita o projeto crescer sem controle).
- **Requisitos** em frases curtas, ex.: *"O supervisor consegue registrar a devolução de um equipamento."*
- **Modelo de dados**: um diagrama simples das tabelas (aqui: `usuario`, `perifericos`, `categorias`, `emprestimos`) e como se ligam.
- **Telas**: rascunho no papel ou Figma (mesmo feio) antes de escrever HTML.
- **Combinados da equipe**: padrão de nomes, de branches e de mensagens de commit.
- **Decisões importantes** em 3 linhas cada (*ADR*): "Escolhemos SQLite porque… / Alternativas: … / Consequência: …".

### 🟩 DURANTE (junto com o código)
- **Commits pequenos e claros**, no padrão *Conventional Commits*: `feat: filtro por status`, `fix: logout usa POST`, `docs: explica como rodar`.
- **Comente o "porquê", não o "o quê"**. Ruim: `# soma 1`. Bom: `# fixed usa coordenadas da janela; não somar scrollY`.
- **Docstring em cada rota**: o que faz, método aceito, o que devolve, quem pode acessar.
- **Uma tabela de rotas sempre atualizada** (exemplo):

  | Rota | Métodos | Requer login | Função |
  |---|---|---|---|
  | `/login` | GET, POST | Não | Autentica o supervisor |
  | `/logout` | **POST** | Não (só limpa a sessão) | Encerra a sessão |
  | `/dashboard` | GET, POST | Sim | Totais de equipamentos |
  | `/equipamentos` | GET, POST | Sim | Lista e filtra |
  | `/verifica_emprestimos` | GET, POST | Sim | Lista e filtra movimentações |
  | `/create_emprestimo` | GET, POST | Sim | Registra saída |
  | `/devolucao` | POST | Sim | Registra devolução |

- **Pull Request com "antes e depois"** (prints) e uma linha dizendo *como testar*.
- **`requirements.txt` atualizado** a cada biblioteca nova (`pip freeze > requirements.txt`).
- **`CHANGELOG.md`** curto: o que mudou em cada versão (modelo em keepachangelog.com/pt-BR).
- **Anote bugs e ideias como *Issues*** em vez de guardar na cabeça.
- Regra de ouro: **mudou como roda ou como usa? Atualize o README no mesmo commit.**

### 🟧 DEPOIS (entrega e passagem de bastão)
- **README que funciona do zero**: clone → ambiente virtual → instalar → rodar → login de teste. Peça para alguém seguir só o README e ver se dá certo.
- **Prints ou GIF** das telas principais no README.
- **Manual de uso** de uma página, para o supervisor (não para programador).
- **Guia de implantação**: onde roda, como fazer backup do `.db`, como atualizar.
- **Problemas conhecidos** (como a seção 5 acima) e **próximos passos**.
- **Retrospectiva**: 3 listas curtas: *o que deu certo · o que não deu · o que faríamos diferente*.
- **Tag/versão** (`v1.0.0`) no GitHub marcando a entrega.
- Como o projeto é feito por **estagiários que se revezam**, escreva pensando em quem chega **sem conhecer nada** dele.

---

## 7. Como fazer um front-end legal

Vale para este projeto (Flask) e serve de base para o projeto em **C#** que vem depois.

1. **Consistência vale mais que enfeite.** Defina em um lugar só cores, fontes, espaçamentos e sombras (`variables.css` já faz isso; use **sempre** as variáveis, sem `#hex` solto).
2. **Um layout base e vários filhos.** Em Flask: `base.html` + `{% extends %}`. Em C# (ASP.NET Core): `_Layout.cshtml` + `@RenderBody()`. Repetir header/sidebar em cada página gera bugs em vários lugares.
3. **Pense no celular primeiro** (*mobile-first*): escreva o CSS para tela pequena e use `@media (min-width: …)` para ampliar. Use `flex`/`grid` com `min-width: 0`, `flex-wrap` e `max-width: 100%`.
4. **Componentes reutilizáveis**: card, botão, tabela, badge de status, modal. Em Jinja: `{% macro %}` ou `{% include %}`; em C#: *Partial Views* / *View Components* / Blazor components.
5. **Mostre sempre o estado da tela:** carregando, vazio ("Nenhum equipamento cadastrado"), erro e sucesso. É o que separa "funciona" de "profissional".
6. **Formulários que ajudam:** `label` em todo campo, `required`, `type` correto (`email`, `tel`), mensagem de erro clara, foco no primeiro campo com erro, botão desabilitado ao enviar. **Valide no navegador e também no servidor.**
7. **Acessibilidade básica** (também é qualidade): HTML semântico (`header`, `nav`, `main`), contraste de cor (cuidado com texto claro sobre fundo claro, como os badges), `alt` nas imagens, `aria-label` em botões de ícone, foco visível ao usar `Tab`.
8. **Hierarquia visual:** um título principal por tela, uma ação primária por vez (o botão azul), o restante mais discreto.
9. **Ações destrutivas pedem confirmação** (excluir, devolver) e cor diferente (vermelho).
10. **Performance:** imagens em `.webp` e no tamanho certo (`flflogoshort.png` tem ~660 KB para uma logo pequena), poucas fontes e pesos, scripts com `defer`.
11. **Ferramentas para evoluir:** **Bootstrap** (aprenda a usar antes de sobrescrever), **Bootstrap Icons**, **Chart.js** para gráficos, **DevTools**, **Lighthouse** (Chrome) para medir acessibilidade e performance, **Figma** para protótipo.

### Quando o projeto for em C#
- **ASP.NET Core MVC ou Razor Pages** é o caminho mais parecido com o que você já faz em Flask/Jinja: `Controller` ↔ rota, `View (.cshtml)` ↔ template, *Tag Helpers* (`asp-controller`, `asp-action`) ↔ `url_for`.
- **Mesmas lições deste projeto:** navegação é `<a asp-action>`; ação que altera dados é `<form method="post">` + `<button>` com `[ValidateAntiForgeryToken]` (o token CSRF vem pronto no framework).
- **Blazor** se quiser componentes interativos sem escrever muito JavaScript; **API + React/Angular/Vue** se o front for separado (aí vale aprender consumo de API com `fetch`).
- **Bootstrap** e o CSS que você aprendeu aqui funcionam igual: front-end é o mesmo, muda só quem gera o HTML.

---

## 8. O que estudar para evoluir

**Ordem sugerida** (cada etapa ajuda na seguinte):

1. **Base da web** (o que mais pesa no dia a dia): HTML semântico · CSS moderno (*flexbox, grid, variáveis, media queries*) · JavaScript (DOM, `fetch`, `async/await`, módulos).
2. **Python e Flask a fundo** (você já está usando): funções, classes, ambientes virtuais · Blueprints · sessões e autenticação · **SQL de verdade** (JOIN, índices, transações) · SQLAlchemy.
3. **Git e GitHub:** branch, merge, resolver conflitos, Pull Request, revisão de código.
4. **Testes:** `pytest` para o back-end; noções de teste de interface (Playwright).
5. **Segurança básica:** senhas com hash (já usam `werkzeug.security`), CSRF, SQL Injection (já usam `?` parametrizado), XSS, OWASP Top 10, variáveis de ambiente para segredos.
6. **HTTP e APIs:** métodos (GET/POST/PUT/DELETE), códigos de status (o erro 405 do logout é um exemplo), JSON, REST.
7. **C# e .NET (próximo projeto):** sintaxe e POO · LINQ · `async/await` · injeção de dependência · **ASP.NET Core** · **Entity Framework Core** · testes com xUnit.
8. **Arquitetura e qualidade:** SOLID, separação em camadas (rotas → serviços → banco), *code smells* e refatoração (o `base.html` é um primeiro passo).
9. **Entrega:** Docker, CI/CD com GitHub Actions, noções de nuvem (Azure, se for seguir C#).
10. **Fora do código:** **inglês técnico** (documentação e Stack Overflow estão em inglês), comunicação, estimar prazos, pedir ajuda com um bom exemplo mínimo do problema.

**Como estudar sem se perder**
- Um **projeto pequeno por tema** (ex.: refazer só o dashboard com gráficos) vale mais que dez cursos.
- **Leia código dos outros** e faça code review nos colegas.
- **Monte portfólio:** este projeto, bem documentado, com prints e README, já é um ótimo começo.
- Fontes confiáveis (confira se os links seguem ativos): MDN (`developer.mozilla.org/pt-BR`), web.dev/learn, documentação oficial do Flask e do Bootstrap 5, `learn.microsoft.com/pt-br/dotnet` (C#), `roadmap.sh` (mapas de estudo por carreira).
