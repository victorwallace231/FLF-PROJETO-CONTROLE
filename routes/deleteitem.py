from flask import  Blueprint ,render_template, request, redirect, session
from banco import conectar_banco

route_deleteitem = Blueprint('deleteitem', __name__)

@route_deleteitem.route('/deleteitem', methods=['POST'])
def delete():
    if not session.get("usuario_email"):
           return redirect ('/login')
    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Deleta o item do banco de dados com base no ID fornecido
    cursor.execute("DELETE FROM perifericos WHERE id_periferico = ?", (request.form['periferico_id'],))
    conexao.commit()
    cursor.execute("SELECT * FROM perifericos")
    perifericos = cursor.fetchall()  # Atualiza a lista de periféricos após a exclusão
    conexao.close()
    return render_template('equipamentos.html', perifericos=perifericos)  # Redireciona para a página do dashboard após a exclusão do item