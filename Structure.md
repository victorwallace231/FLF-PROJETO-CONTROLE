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


