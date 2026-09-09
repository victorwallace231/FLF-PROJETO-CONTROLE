from flask import Blueprint, request, redirect, session
from banco import conectar_banco
from datetime import date

route_devolucao = Blueprint('devolucao', __name__)

@route_devolucao.route('/devolucao', methods= ['POST'])
def devolucao():

        id_emprestimo = request.form.get("id_emprestimo")

        conexao = conectar_banco()
        cursor = conexao.cursor()
        data_devolucao = date.today()
        cursor.execute("UPDATE emprestimos SET devolvido = True, data_devolucao = ? WHERE id_emprestimo = ?", (data_devolucao, id_emprestimo,))
        conexao.commit()
        conexao.close()
        return redirect ('/verifica_emprestimos')
