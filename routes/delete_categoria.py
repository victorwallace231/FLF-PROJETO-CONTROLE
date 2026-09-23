from flask import Blueprint, request, redirect, session, render_template
from banco import conectar_banco

delete_categoria = Blueprint('delete_categoria', __name__)

@delete_categoria.route('/delete_categoria', methods = ['POST'])
def delete():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    erro = ""

    id_categoria = request.form.get("id_categoria")
    nome_categoria = request.form.get("nome_categoria")

    if id_categoria == '1':
        cursor.execute("SELECT id_categoria, categoria, excluido FROM categorias WHERE excluido = 0 OR excluido IS NULL")
        categorias = cursor.fetchall()
        conexao.close()
        erro = "Você não pode excluir essa categoria"
        return render_template("createitem.html", erro = erro, categorias=categorias)
    else:
        cursor.execute("""UPDATE categorias SET excluido = 1 WHERE id_categoria = ?""", (id_categoria,))
        cursor.execute("""UPDATE perifericos SET categoria = 1 WHERE categoria = ?""", (id_categoria,))
    
    conexao.commit()
    conexao.close()

    return redirect('/create_item')