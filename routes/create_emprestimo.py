from flask import Blueprint, render_template, request, redirect, session
from banco import conectar_banco
from datetime import date

create_emprestimo = Blueprint('create_emprestimo', __name__)

@create_emprestimo.route('/create_emprestimo', methods = ['GET', 'POST'])
def create():
    if not session.get("usuario_email"):
        return redirect('/login')
    if request.method == 'GET':
        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute("SELECT * FROM perifericos WHERE disponivel = 1")
        perifericos = cursor.fetchall()
        conexao.close()


        return render_template ("createmov.html",perifericos = perifericos, name = session.get("usuario_name"))
    if request.method == 'POST':
        conexao = conectar_banco()
        cursor = conexao.cursor()
        data_saida = date.today()

        responsavel = request.form["responsavel"]
        id_periferico = request.form["id_periferico"]
        tel_responsavel = request.form["tel_responsavel"]
        observacao = request.form["observacao"]

        cursor.execute("UPDATE perifericos SET disponivel = 0 WHERE id_periferico = ?", (id_periferico,))
        cursor.execute("INSERT INTO emprestimos (responsavel, data_saida, id_periferico, tel_responsavel, id_usuario, observacao) VALUES (?,?,?,?,?,?)", (responsavel, data_saida, id_periferico, tel_responsavel, session.get("usuario_id"), observacao, ))
        conexao.commit()
        conexao.close()
        return redirect ("/verifica_emprestimos")