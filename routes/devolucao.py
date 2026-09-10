from flask import Blueprint, request, redirect, session
from banco import conectar_banco
from datetime import date

route_devolucao = Blueprint('devolucao', __name__)

@route_devolucao.route('/devolucao', methods= ['POST'])
def devolucao():
        if not session.get("usuario_email"):
                return redirect("/login")
        
        id_emprestimo = request.form["id_emprestimo"]
        id_periferico = request.form["id_periferico"]

        conexao = conectar_banco()
        cursor = conexao.cursor()
        data_devolucao = date.today()
        cursor.execute("UPDATE emprestimos SET devolvido = 1, data_devolucao = ? WHERE id_emprestimo = ?", (data_devolucao, id_emprestimo,))
        cursor.execute("UPDATE perifericos SET disponivel = 1 WHERE id_periferico = ?", (id_periferico,))
        conexao.commit()
        conexao.close()
        return redirect ('/verifica_emprestimos')
