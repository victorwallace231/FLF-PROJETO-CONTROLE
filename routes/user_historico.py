from flask import Blueprint,redirect,session,request,render_template
from banco import conectar_banco

user_historico = Blueprint('user_historico', __name__)

@user_historico.route('/user_historico', methods = ['GET','POST'])
def historico():
    if not session.get("usuario_email"):
        return redirect('/login')

    if request.method == 'GET':
        conexao = conectar_banco()
        cursor = conexao.cursor()
        id_usuario = session.get("usuario_id")
        cursor.execute("SELECT * FROM emprestimos WHERE id_usuario = ?", (id_usuario,))
        emprestimos = cursor.fetchall()
        conexao.close()
        return render_template("historico.html", emprestimos = emprestimos)