from flask import Blueprint, render_template, request, redirect, url_for, session
from banco import conectar_banco

recuperar_senha = Blueprint('recuperar_senha', __name__)

@recuperar_senha.route('/recuperar_senha', methods=['GET', 'POST'])
def verificar():
    if request.method == 'GET':
        return render_template('recuperar_senha.html', erro="")

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        telefone = request.form.get('telefone', '').strip()

        conexao = conectar_banco()
        cursor = conexao.cursor()

        # Consulta se existe usuário com o e-mail E o telefone informados
        cursor.execute("SELECT id_usuario FROM usuario WHERE email_user = ? AND tel_user = ?", (email, telefone))
        usuario = cursor.fetchone()
        conexao.close()

        if usuario:
            # Salva o ID na sessão para a próxima etapa
            session['reset_user_id'] = usuario[0]
            return redirect(url_for('redefinir_senha.nova_senha'))
        else:
            return render_template('recuperar_senha.html', erro="E-mail ou telefone incorretos.", email=email, telefone=telefone)