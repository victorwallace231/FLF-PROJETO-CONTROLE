from flask import Blueprint, request, redirect, session
from banco import conectar_banco

delete_categoria = Blueprint('delete_categoria', __name__)

@delete_categoria.route('/delete_categoria', methods = ['POST'])
def delete():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    id_categoria = request.form.get("id_categoria")

    cursor.execute("""UPDATE categorias SET excluido = 1 WHERE id_categoria = ?""", (id_categoria,))
    cursor.execute("UPDATE perifericos SET categoria = 3 WHERE categoria = ?", (id_categoria,))
    conexao.commit()
    conexao.close()

    return redirect('/create_item')