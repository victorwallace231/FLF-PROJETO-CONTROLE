from flask import Blueprint, render_template, request, redirect, session
from banco import conectar_banco

create_categoria = Blueprint('create_categoria', __name__)

@create_categoria.route('/create_categoria', methods = ['POST'])
def create():
    if not session.get("usuario_email"):
        return redirect('/login')
    nome_categoria = request.form['nome_categoria'].strip().lower()
    if nome_categoria:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute("INSERT INTO categorias (categoria) VALUES (?)", (nome_categoria,))

        conexao.commit()
        conexao.close()

    return redirect('/create_item')