from flask import Blueprint, render_template, request, redirect, session, flash
from banco import conectar_banco
from werkzeug.security import check_password_hash

# Definição dos Blueprints para rotas de autenticação e encerramento de sessão
route_login = Blueprint('login', __name__)
route_logout = Blueprint('logout', __name__)


# Rota responsável por exibir o formulário e autenticar o usuário
@route_login.route('/login', methods=['GET', 'POST'])
def login():

    # Requisição GET: Renderiza a página inicial de login enviando mensagem de erro vazia
    if request.method == 'GET':
        erro = ""
        return render_template('login.html', erro=erro)

    # Requisição POST: Processa a tentativa de login enviada pelo formulário
    if request.method == 'POST':
        # Captura os dados do formulário, removendo espaços extras e padronizando o e-mail em minúsculas
        email = request.form['email'].strip().lower()
        password = request.form['senha'].strip()

        # Conecta ao banco de dados para buscar o usuário pelo e-mail
        conexao = conectar_banco()
        cursor = conexao.cursor()

        # Busca os dados do usuário correspondente ao e-mail informado
        cursor.execute("SELECT * FROM usuario WHERE email_user = ?", (email,))
        usuario = cursor.fetchone()
        conexao.close()

        # Validação: verifica se o usuário foi encontrado e compara o hash da senha armazenada
        # Ordem das colunas da tabela 'usuario': 0=name_user, 1=email_user, 2=senha_user, 3=tel_user, 4=id_usuario
        if usuario and check_password_hash(usuario[2], password):
            # Armazena os dados do usuário na sessão do Flask
            session['usuario_name'] = usuario[0]
            session['usuario_email'] = usuario[1]
            session['usuario_telefone'] = usuario[3]
            session["usuario_id"] = usuario[4]

            # Configura a duração da sessão de acordo com a checkbox "Lembrar-me"
            if request.form.get('lembrar'):
                session.permanent = True  # Mantém a sessão ativa por mais tempo
            else:
                session.permanent = False # Encerra a sessão ao fechar o navegador

            # Redireciona para o painel principal do sistema após sucesso
            return redirect('/dashboard')
        else:
            # Em caso de erro na autenticação, recarrega o formulário exibindo o aviso
            return render_template("login.html", erro='Email ou senha incorretos')


# Rota para encerrar a sessão do usuário
@route_logout.route('/logout', methods=['POST'])
def logout():
    # Limpa todas as variáveis armazenadas na sessão ativa
    session.clear()
    flash("Você saiu da conta com sucesso.", "success")

    # Redireciona o usuário de volta para a tela de login
    return redirect('/login')