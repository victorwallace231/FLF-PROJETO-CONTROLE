from flask import Blueprint, request, redirect, session
from banco import conectar_banco

update_categoria = Blueprint('update_categoria', __name__)

@update_categoria.route('/update_categoria', methods = ['POST'])
def delete():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    id_categoria = request.form.get("id_categoria")
    nome_categoria = request.form.get("nome_categoria")

    cursor.execute("""UPDATE categorias SET categoria = ? WHERE id_categoria = ?""", (nome_categoria,id_categoria,))
    conexao.commit()
    conexao.close()

    return redirect('/create_item')