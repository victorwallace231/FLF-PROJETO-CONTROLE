import re
from flask import Blueprint, render_template, request, redirect, session, flash
from banco import conectar_banco

# Definição do Blueprint para o módulo de atualização de cadastro de usuário
route_updateuser = Blueprint('updateuser', __name__)
route_updatetoadmin = Blueprint('updatetoadmin', __name__)
route_removeadmin = Blueprint('removeadmin', __name__)

# Rota que atende tanto o carregamento do formulário (GET) quanto o envio dos dados (POST)
@route_updateuser.route('/updateuser', methods=['GET', 'POST'])
def update():
    # Verificação de segurança: redireciona para a tela de login se não houver usuário ativo na sessão
    if not session.get("usuario_email"):
        return redirect('/login')

    # Requisição GET: apenas renderiza a página do formulário de edição de perfil
    if request.method == 'GET':
        return render_template('update.html')

    # Requisição POST: processa a atualização dos dados no banco e na sessão
    if request.method == 'POST':
        conexao = conectar_banco()
        cursor = conexao.cursor()

        # Captura os novos valores digitados pelo usuário no formulário
        email = request.form['email']
        nome = request.form['nome']
        # Remove qualquer caractere que não seja dígito antes de gravar no banco
        telefone = re.sub(r"\D", "", request.form['telefone'])

        # Executa a atualização no SQLite usando o e-mail atual armazenado na sessão como chave de busca
        # Nota: Ajustado de 'user_email' para 'email_user' para corresponder ao nome real da coluna no banco
        cursor.execute(
            "UPDATE usuario SET name_user = ?, email_user = ?, tel_user = ? WHERE email_user = ?", 
            (nome, email, telefone, session.get('usuario_email'))
        )
        
        # Confirma as alterações na base de dados e fecha a conexão
        conexao.commit()
        conexao.close()

        # Atualiza os dados gravados na sessão com as novas informações para manter a aplicação sincronizada
        session['usuario_name'] = nome
        session['usuario_telefone'] = telefone
        session['usuario_email'] = email

        flash("Seus dados foram atualizados com sucesso!", "success")
        # Redireciona o usuário de volta para o painel principal após salvar
        return redirect('/dashboard')

@route_updatetoadmin.route('/updatetoadmin', methods=['GET', 'POST'])
def updatetoadmin():
    # Verificação de segurança: redireciona para a tela de login se não houver usuário ativo na sessão
    if not session.get("usuario_email"):
        return redirect('/login')
    if str(session.get('usuario_admin')) != '1':
        flash("Acesso negado: apenas administradores podem acessar esta página.", "danger")
        return redirect('/dashboard')

    # Requisição GET: apenas renderiza a página do formulário de edição de perfil
    if request.method == 'GET':
        return render_template('opcoes_admin.html')

    # Requisição POST: processa a atualização dos dados no banco e na sessão
    if request.method == 'POST':
        conexao = conectar_banco()
        cursor = conexao.cursor()

        email = request.form.get("email").strip()

        cursor.execute(
            "UPDATE usuario SET admin = 1 WHERE email_user = ?", (email,)
        )
        conexao.commit()
        conexao.close()

        flash("O usuário foi atualizado para administrador com sucesso!", "success")
        return redirect('/dashboard')
@route_removeadmin.route('/removeadmin', methods=['POST'])
def removeadmin():

    if str(session.get('usuario_admin')) != '1':
        flash("Acesso negado: apenas administradores podem acessar esta página.", "danger")
        return redirect('/dashboard')

    email = request.form.get("email").strip().lower()

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        "UPDATE usuario SET admin = 0 WHERE email_user = ?", (email,)
    )
    conexao.commit()
    conexao.close()

    flash("Os privilégios de administrador foram removidos com sucesso!", "success")
    return redirect('/dashboard')
