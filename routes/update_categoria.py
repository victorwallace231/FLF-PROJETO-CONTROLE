from flask import Blueprint, request, redirect, session, flash
from banco import conectar_banco

update_categoria = Blueprint('update_categoria', __name__)

@update_categoria.route('/update_categoria', methods = ['POST'])
def update():
    if not session.get("usuario_email"):
        return redirect('/login')

    id_categoria = request.form.get("id_categoria")
    nome_categoria = request.form.get("nome_categoria", "").strip().lower()

    # A categoria 1 ("sem categoria") é a padrão do sistema e não pode ser alterada
    if id_categoria == '1':
        flash("Você não pode alterar essa categoria.", "danger")
        return redirect('/create_item')

    if not nome_categoria:
        flash("Digite o novo nome da categoria.", "danger")
        return redirect('/create_item')

    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("UPDATE categorias SET categoria = ? WHERE id_categoria = ?", (nome_categoria, id_categoria))
    conexao.commit()
    conexao.close()

    flash("Categoria renomeada com sucesso!", "success")
    return redirect('/create_item')
