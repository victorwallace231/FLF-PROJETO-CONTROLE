from flask import Blueprint, render_template, request, redirect, session
from banco import conectar_banco

route_deleteuser = Blueprint('deleteuser', __name__)

@route_deleteuser.route('/deleteuser', methods=['POST'])
def delete():
    if not session.get("usuario_email"):
            return redirect ('/login')
    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Deleta o usuário do banco de dados com base no email fornecido
    cursor.execute("DELETE FROM usuario WHERE user_email = ?", (session.get('usuario_email'),))
    conexao.commit()
    conexao.close()
    session.clear()  # Limpa a sessão do usuário após a exclusão
    return redirect('/login')  # Redireciona para a página de login após a exclusão do usuário