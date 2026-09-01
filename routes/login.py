from flask import Blueprint, render_template, request, redirect, session
from banco import conectar_banco
# Importando funções de segurança para hash de senha
from werkzeug.security import check_password_hash

# Blueprint para a rota de login
route_login = Blueprint ('login', __name__)

# Rota de login
@route_login.route('/login', methods=['GET','POST'])
def login():

    # Renderiza o template de login para requisições GET
        if request.method == 'GET':
            return render_template('login.html')
        if request.method == 'POST':
            # Captura os dados do formulário de login
            email = request.form['email']
            password = request.form['senha']

            # Conecta ao banco de dados e verifica se o usuário existe
            conexao = conectar_banco()
            # cria um cursor para executar comandos SQL
            cursor = conexao.cursor()
            # executa uma consulta SQL para buscar o usuário pelo email fornecido
            cursor.execute("SELECT * FROM usuario WHERE email_user = ?", (email,))
            # busca o primeiro resultado da consulta
            usuario = cursor.fetchone()
            conexao.close()

            # Verifica se o usuário existe e se a senha fornecida corresponde à senha armazenada no banco de dados
            # A função check_password_hash é usada para comparar a senha fornecida com a senha armazenada de forma segura (hash)
            
            if usuario and check_password_hash(usuario[2], password):
                # Redireciona para a página do dashboard se o login for bem-sucedido
                session['usuario_name'] = usuario[0]  # Armazena o nome do usuário na sessão
                session['usuario_email'] = usuario[1]  # Armazena o email do usuário na sessão
                session['usuario_telefone'] = usuario[3]  # Armazena o telefone do usuário na sessão

            return redirect('/dashboard')
        else:
            # Renderiza o template de login novamente com uma mensagem de erro se o login falhar
            return render_template('login.html', error='Email ou senha incorretos')
            #cONFIGURAR MENSAGEM DE ERRO PARA O USUÁRIO, CASO O LOGIN FALHE OBS: NÃO ESTÁ FUNCIONANDO A MENSAGEM DE ERRO, POIS O TEMPLATE NÃO ESTÁ CONFIGURADO PARA RECEBER A VARIÁVEL ERROR.