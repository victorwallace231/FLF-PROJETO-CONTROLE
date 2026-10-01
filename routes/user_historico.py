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
        cursor.execute("""
            SELECT e.*, c.categoria, p.num_serie, p.id_periferico, p.unid_origem, p.setor_origem 
            FROM emprestimos e 
            JOIN perifericos p ON e.id_periferico = p.id_periferico
            JOIN categorias c ON p.categoria = c.id_categoria
            WHERE e.id_usuario = ? ORDER BY e.id_emprestimo DESC
        """, (id_usuario,))
        emprestimos = cursor.fetchall()
        conexao.close()
        return render_template("historico.html", emprestimos = emprestimos)