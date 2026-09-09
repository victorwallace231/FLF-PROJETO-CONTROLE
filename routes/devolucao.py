from flask import Blueprint, request, redirect, session
from banco import conectar_banco

route_devolucao = Blueprint('devolucao', __name__)

@route_devolucao.route('/devolucao', methods= ['PATCH'])
def devolucao():

        id_emprestimo = request.form.get("id_emprestimo")

        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute("UPDATE emprestimos SET devolvido = True WHERE id_emprestimo = ?", (id_emprestimo,))
        conexao.commit()
        conexao.close()
        return redirect ('/verifica_emprestimos')
