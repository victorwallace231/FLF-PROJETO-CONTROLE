from flask import Blueprint, request, redirect, session, flash
from banco import conectar_banco

delete_categoria = Blueprint('delete_categoria', __name__)

@delete_categoria.route('/delete_categoria', methods = ['POST'])
def delete():
    if not session.get("usuario_email"):
        return redirect('/login')

    id_categoria = request.form.get("id_categoria")

    # A categoria 1 ("sem categoria") é a padrão do sistema e não pode ser excluída
    if id_categoria == '1':
        flash("Você não pode excluir essa categoria.", "danger")
        return redirect('/create_item')

    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("UPDATE categorias SET excluido = 1 WHERE id_categoria = ?", (id_categoria,))
    # Os equipamentos dessa categoria passam para "sem categoria"
    cursor.execute("UPDATE perifericos SET categoria = 1 WHERE categoria = ?", (id_categoria,))
    conexao.commit()
    conexao.close()

    flash("Categoria excluída. Os equipamentos dela foram movidos para \"sem categoria\".", "success")
    return redirect('/create_item')
