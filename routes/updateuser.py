import re
from flask import Blueprint, render_template, request, redirect, session, flash
from banco import conectar_banco
from werkzeug.security import generate_password_hash

# Definição do Blueprint para o módulo de atualização de cadastro de usuário
route_updateuser = Blueprint('updateuser', __name__)
route_updatetoadmin = Blueprint('updatetoadmin', __name__)
route_removeadmin = Blueprint('removeadmin', __name__)
route_update_user_adm = Blueprint('update_user_adm', __name__)

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
@route_update_user_adm.route('/update_user_adm', methods=['POST'])
def update_user_adm():
    # 1. Validação de sessão
    if not session.get("usuario_email"):
        return redirect('/login')

    if str(session.get('usuario_admin')) != '1':
        flash("Acesso negado: apenas administradores podem aceder a esta página.", "danger")
        return redirect('/dashboard')

    # 2. Captura de dados do formulário
    email_ref = request.form.get("email_ref", "").strip().lower()
    novo_nome = request.form.get("nome", "").strip()
    novo_email = request.form.get("novo_email", "").strip().lower()
    novo_telefone = request.form.get("telefone", "").strip()
    nova_senha = request.form.get("senha", "").strip()

    if not email_ref:
        flash("O e-mail de referência do utilizador é obrigatório.", "danger")
        return redirect('/dashboard')

    conexao = conectar_banco()
    cursor = conexao.cursor()

    # 3. Procura o ID do utilizador através do e-mail de referência
    cursor.execute("SELECT id_usuario FROM usuario WHERE email_user = ?", (email_ref,))
    usuario = cursor.fetchone()

    if not usuario:
        conexao.close()
        flash("Utilizador não encontrado.", "danger")
        return redirect('/dashboard')

    id_usuario = usuario[0]

    # 4. Atualiza os campos individualmente utilizando o ID (chave primária)
    if novo_email:
        cursor.execute("UPDATE usuario SET email_user = ? WHERE id_usuario = ?", (novo_email, id_usuario))
    if nova_senha:
        senha_hash = generate_password_hash(nova_senha)
        cursor.execute("UPDATE usuario SET senha_user = ? WHERE id_usuario = ?", (senha_hash, id_usuario))
    if novo_telefone:
        tel_limpo = re.sub(r"\D", "", novo_telefone)
        cursor.execute("UPDATE usuario SET tel_user = ? WHERE id_usuario = ?", (tel_limpo, id_usuario))
    if novo_nome:
        cursor.execute("UPDATE usuario SET name_user = ? WHERE id_usuario = ?", (novo_nome, id_usuario))

    conexao.commit()
    conexao.close()

    flash("Os dados do utilizador foram atualizados com sucesso!", "success")
    return redirect('/dashboard')