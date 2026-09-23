from flask import Blueprint, request, redirect, session, render_template
from banco import conectar_banco

update_categoria = Blueprint('update_categoria', __name__)

@update_categoria.route('/update_categoria', methods = ['POST'])
def update():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    erro = ""

    id_categoria = request.form.get("id_categoria")
    nome_categoria = request.form.get("nome_categoria")

    if id_categoria == '1':
        cursor.execute("SELECT id_categoria, categoria, excluido FROM categorias WHERE excluido = 0 OR excluido IS NULL")
        categorias = cursor.fetchall()
        conexao.close()
        erro = "Você não pode alterar essa categoria"
        return render_template("createitem.html", erro = erro, categorias=categorias)
    else:
        cursor.execute("""UPDATE categorias SET categoria = ? WHERE id_categoria = ?""", (nome_categoria,id_categoria,))
        conexao.commit()

    conexao.close()

    return redirect('/create_item')