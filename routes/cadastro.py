from flask import Blueprint, render_template, request, redirect
from banco import conectar_banco
from werkzeug.security import generate_password_hash

# Definição do Blueprint para as rotas de cadastro de usuários
route_cadastro = Blueprint('cadastro', __name__)

@route_cadastro.route("/cadastro", methods=["GET", "POST"])
def cadastrar   ():
    # Requisição GET: carrega o formulário HTML inicial com mensagem de erro vazia
    if request.method == "GET":
        erro = ""
        return render_template("cadastro.html", erro=erro)

    # Requisição POST: processa o registro de uma nova conta de usuário
    if request.method == "POST":
        # Captura e higieniza os dados do formulário (remove espaços extras e padroniza e-mail/nome em minúsculas)
        name = request.form["nome"].strip().lower()
        email = request.form["email"].strip().lower()
        number = request.form["telefone"].strip()
        password = request.form["senha"].strip()
        confirm_password = request.form["confirmar_senha"].strip()

        # Validação: interrompe o fluxo e exibe aviso se as senhas informadas forem diferentes
        if password != confirm_password:
            return render_template("cadastro.html", erro="As senhas não coincidem. Por favor, tente novamente.")

        # Transforma a senha digitada em um hash criptográfico seguro usando o Werkzeug
        password_hash = generate_password_hash(password)

        # Conecta ao banco de dados SQLite apenas após validar a senha
        conexao = conectar_banco()
        cursor = conexao.cursor()

        # Insere o novo usuário na tabela 'usuario' protegendo contra SQL Injection
        cursor.execute(
            "INSERT INTO usuario (name_user, email_user, senha_user, tel_user) VALUES (?, ?, ?, ?)", 
            (name, email, password_hash, number)
        )

        # Efetiva a gravação na base de dados e encerra a conexão
        conexao.commit()
        conexao.close()

        # Redireciona o novo usuário para a página de login
        return redirect("/login")