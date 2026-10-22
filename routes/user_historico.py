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
            SELECT e.*, c.categoria, p.num_serie, p.id_periferico, u.nome_unidade AS unid_origem, s.nome_setor AS setor_origem 
            FROM emprestimos e 
            JOIN perifericos p ON e.id_periferico = p.id_periferico
            JOIN categorias c ON p.categoria = c.id_categoria
            LEFT JOIN unidades u ON u.id_unidade = p.id_unidade_origem
            LEFT JOIN setores s ON s.id_setor = p.id_setor_origem
            WHERE e.id_usuario = ? ORDER BY e.id_emprestimo DESC
        """, (id_usuario,))
        emprestimos = cursor.fetchall()
        conexao.close()
        return render_template("historico.html", emprestimos = emprestimos)