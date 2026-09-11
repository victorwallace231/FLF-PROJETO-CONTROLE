from flask import Flask,request,redirect,render_template, Blueprint
from banco import conectar_banco
from werkzeug.security import generate_password_hash, check_password_hash

route_cadastro = Blueprint('cadastro', __name__)

@route_cadastro.route("/cadastro", methods=["GET","POST"])
def cadastrar():
    #Carregar o arquivo html para a pagina web
    if request.method == "GET":
        erro= ""
        return render_template("cadastro.html", erro = erro)
    if request.method == "POST":
        #conexão com o banco de dados
        conexao = conectar_banco()
        cursor = conexao.cursor()

        #recebendo do formulario html os valores de cadastro do usuário
        name = request.form ["nome"].strip().lower()
        email = request.form ["email"].strip().lower()
        number = request.form ["telefone"].strip()
        password = request.form ["senha"].strip()
        confirm_password = request.form ["confirmar_senha"].strip()

        if password != confirm_password:
            return render_template("cadastro.html", erro="As senhas não coincidem. Por favor, tente novamente.")

        #convertendo a senha digitada em hash
        password_hash = generate_password_hash(password)

        #salvando os dados do usuário no banco
        cursor.execute("INSERT INTO usuario (name_user, email_user, senha_user, tel_user) VALUES (?, ?, ?, ?)", (name,email,password_hash,number))
        conexao.commit()
        conexao.close()

        #Redireciona para a pagina de login
        return redirect("/login")
