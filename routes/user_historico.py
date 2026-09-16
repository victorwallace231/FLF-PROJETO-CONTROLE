from flask import Blueprint,redirect,session,request,render_template
from banco import conectar_banco

user_historico = Blueprint('user_historico', __name__)

@user_historico.route('/user_historico', methods = ['POST'])
def actvation():
    if request.method == 'POST':
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM emprestimos WHERE id_usuario = ?", (session.get("usuario_id")))
        emprestimos = cursor.fetchall()
        conexao.close()
        return render_template("historico.html", emprestimos = emprestimos)