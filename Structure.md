# Entendendo decisões arquiteturais e a estrutura do projeto

## Requisitos para rodar

<h3>Setup de Ambiente:</h3>
  
* [Python 3.14.7](https://www.python.org/downloads/)
* [Flask 3.1.3](https://pypi.org/project/Flask/3.1.3/)
* [Werkzeug 3.1.8](https://pypi.org/project/Werkzeug/)

<h3>Como rodar na minha máquina?</h3>

* Clone o repositório:
   ```bash
   git clone https://github.com/victorwallace231/FLF-PROJETO-CONTROLE.git   

* Criar o ambiente virtual na pasta do projeto
`python -m venv venv`

* Ativar o ambiente virtual(Windows PowerShell)
`.\venv\Scripts\activate`

* Ativar o ambiente virtual (Linux/macOS ou Git Bash)
`source venv/bin/activate`

* Instalar o Flask no ambiente virtual 
`python -m pip install flask`

* 🆗Pronto

## Controle FLF Site

<h3>Estrutura do projeto</h3>

* `./Test` É a pasta que usamos como criação de novas lading pages teste ou a reformulação de uma lading page existente.
* `._pycache` É o local que armazena o cache do arquivo `app.py` e o `banco.py`
* `./routes` Armazena todas as rotas da aplicação.
* `./routes/_pycache_` Armazena o o cache dos arquivos da routas.
* `./static` A pasta que armazena os arquivos estáticos da aplicação, que sao entregue diretamente ao navegador do usuário.
* `./static/css` Local que fica o `CSS` utilizado na pasta `/.templates` contribuindo com a estilização do projeto.
* `./static/img` Pasta que fica as imagens utilizadas no projeto. 
* `./static/js` Contem os arquivos que contribuem para escrever a busca de emprestimos no banco.
* `./templates` É a pasta que contem o `HTML` do projeto.

## Front-end (atualizado na rodada 2)

* `./templates/base_app.html` Layout das telas logadas (sidebar, cabeçalho, pop-ups). As outras telas usam `{% extends "base_app.html" %}`.
* `./templates/base_auth.html` Layout de login, cadastro, recuperar e redefinir senha.
* `./templates/_macros.html` Pedaços reutilizáveis (campo com ícone, badges de status, seletor de ícones).
* `./templates/_feedback.html` Toasts e janela de confirmação (Bootstrap 5).
* `./static/css` Apenas 4 arquivos: `variables.css`, `base.css` (todas as telas), `app.css` (telas logadas) e `animacoes.css`.
* `./static/js` `validacao.js` (erros nos formulários), `feedback.js` (toasts e "tem certeza?"), `modais.js` (janelas reutilizáveis), `icones.js` (adicionar ícones), `historico_item.js` e `animacoes.js`.
* `./Test/_legado` Cópia dos CSS/JS antigos, usada só pelos protótipos de `Test/`.
