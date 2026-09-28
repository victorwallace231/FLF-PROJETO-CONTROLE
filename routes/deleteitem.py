from flask import Blueprint, request, redirect, session, flash
from banco import conectar_banco

# Definição do Blueprint para as rotas de exclusão/desativação de equipamentos
route_deleteitem = Blueprint('deleteitem', __name__)

@route_deleteitem.route('/deleteitem', methods=['POST'])
def delete():
    # Verificação de segurança: redireciona para o login caso o usuário não esteja autenticado
    if not session.get("usuario_email"):
        return redirect('/login')

    conexao = conectar_banco()
    cursor = conexao.cursor()

    # "Exclusão lógica" (soft delete): marca o item como inativo e zera os outros status.
    # Isso preserva o histórico da tabela de empréstimos sem apagar o registro fisicamente.
    cursor.execute(
        "UPDATE perifericos SET inativo = 1, disponivel = 0, manutencao = 0 WHERE id_periferico = ?",
        (request.form['periferico_id'],)
    )
    conexao.commit()
    conexao.close()

    flash("Equipamento excluído com sucesso.", "success")
    return redirect('/equipamentos')
