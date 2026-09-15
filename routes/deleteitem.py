from flask import Blueprint, render_template, request, redirect, session
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

    # Executa a "exclusão lógica" (soft delete): marca o item como inativo (1) e zera os outros status.
    # Isso preserva o histórico da tabela de empréstimos sem apagar o registro fisicamente.
    cursor.execute(
        "UPDATE perifericos SET inativo = 1, disponivel = 0, manutencao = 0 WHERE id_periferico = ?", 
        (request.form['periferico_id'],)
    )
    conexao.commit()

    # Busca a lista atualizada contendo apenas os equipamentos que NÃO estão inativos
    # Nota: Ajustado de 'indisponivel' para 'inativo', que é o nome correto da coluna no banco
    cursor.execute("SELECT * FROM perifericos WHERE inativo != 1")
    perifericos = cursor.fetchall()
    conexao.close()

    # Renderiza o template atualizado passando a lista de itens e o nome do usuário ativo na sessão
    return render_template('equipamentos.html', perifericos=perifericos, name=session.get("usuario_name"))