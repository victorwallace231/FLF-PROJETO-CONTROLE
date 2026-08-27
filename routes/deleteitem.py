from flask import  Blueprint ,render_template, request, redirect
from banco import conectar_banco

route_deleteitem = Blueprint('deleteitem', __name__)

@route_deleteitem.route('/deleteitem', methods=['POST'])
def delete():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Deleta o item do banco de dados com base no ID fornecido
    cursor.execute("DELETE FROM perifericos WHERE id = ?", (request.form['item_id'],))
    conexao.commit()
    conexao.close()
    return redirect('/deleteitem')  # Redireciona para a página do dashboard após a exclusão do item