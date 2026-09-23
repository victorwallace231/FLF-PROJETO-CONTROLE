from flask import Blueprint, request, redirect, session, flash
from banco import conectar_banco

create_categoria = Blueprint('create_categoria', __name__)

@create_categoria.route('/create_categoria', methods = ['POST'])
def create():
    if not session.get("usuario_email"):
        return redirect('/login')

    nome_categoria = request.form.get('nome_categoria', '').strip().lower()
    if not nome_categoria:
        flash("Digite o nome da categoria.", "danger")
        return redirect('/create_item')

    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO categorias (categoria) VALUES (?)", (nome_categoria,))
    conexao.commit()
    conexao.close()

    flash("Categoria criada com sucesso!", "success")
    return redirect('/create_item')
