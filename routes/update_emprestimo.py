from flask import Blueprint, render_template, request, redirect, session
from banco import conectar_banco

update_emprestimo = Blueprint('update_emprestimo', __name__)

@update_emprestimo.route('/update_emprestimo', methods = ['POST'])
def atuliza_emprestimo():
    if request.method == 'POST':
        conexao = conectar_banco()
        cursor = conexao.cursor()

        responsavel = request.form.get('responsavel')
        id_emprestimo = request.form.get('id_emprestimo')
        tel_responsavel = request.form.get('tel_responsavel')
        parametros = []

        sql = """UPDATE emprestimos SET id_emprestimo = id_emprestimo"""

        if responsavel:
            sql += ", responsavel = ? "
            parametros.append(responsavel)
        if tel_responsavel:
            sql+=", tel_responsavel = ?"
            parametros.append(responsavel)

        sql+=" WHERE id_emprestimo = ?"
        parametros.append(id_emprestimo)

        cursor.execute(sql,parametros)
        conexao.commit()
        conexao.close()

        return redirect('/verifica_emprestimos')