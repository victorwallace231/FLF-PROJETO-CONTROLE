from flask import Flask, request, redirect, render_template
from banco import conectar_banco
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
@app.route("/", methods=["GET","POST"])
def cadastrar():
    #Carregar o arquivo html para a pagina web
    if request.method == "GET":
        return render_template("cadastro.html")

    #conexão com o banco de dados
    conexao = conectar_banco()
    cursor = conexao.cursor()

    #recebendo do formulario html os valores de cadastro do usuário
    name = request.form ["name"]
    email = request.form ["email"]
    number = request.form ["number"]
    password = request.form ["password"]

    #convertendo a senha digitada em hash
    password_hash = generate_password_hash(password)

    #salvando os dados do usuário no banco
    cursor.execute("INSERT INTO usuario (nome, email, telefone, senha) VALUES (?, ?, ?, ?)", (name,email,number,password_hash))
    conexao.commit()

    #Redireciona para a pagina de login
    return redirect("/login")