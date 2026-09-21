from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from banco import conectar_banco

redefinir_senha = Blueprint('redefinir_senha', __name__)

@redefinir_senha.route('/redefinir_senha', methods=['GET', 'POST'])
def alterar():
    # Proteção: Garante que só acessa esta página quem passou pela verificação
    user_id = session.get('reset_user_id')
    if not user_id:
        return redirect(url_for('recuperar_senha.verificar'))

    if request.method == 'GET':
        return render_template('redefinir_senha.html', erro="")

    if request.method == 'POST':
        nova_senha = request.form.get('nova_senha').strip()
        confirmar_senha = request.form.get('confirmar_senha').strip()

        # Validação se as senhas coincidem
        if nova_senha != confirmar_senha:
            return render_template('redefinir_senha.html', erro="As senhas não coincidem.")

        if len(nova_senha) < 4:
            return render_template('redefinir_senha.html', erro="A senha deve ter pelo menos 4 caracteres.")

        # Atualiza a senha no banco de dados
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("UPDATE usuarios SET senha = ? WHERE id_usuario = ?", (nova_senha, user_id))
        conexao.commit()
        conexao.close()

        # Limpa a variável de verificação da sessão por segurança
        session.pop('reset_user_id', None)

        # Redireciona para o login após o sucesso
        return redirect(url_for('login.login'))