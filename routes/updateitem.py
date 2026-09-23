from flask import Blueprint, request, redirect, session, flash
from banco import conectar_banco, icone_valido

# Definição do Blueprint para as rotas de atualização de equipamentos
route_updateitem = Blueprint('update_item', __name__)

@route_updateitem.route('/update_item', methods=['POST'])
def update():
    # Verificação de autenticação: se o usuário não estiver logado, redireciona para a tela de login
    if not session.get("usuario_email"):
        return redirect('/login')

    conexao = conectar_banco()
    cursor = conexao.cursor()

    # O 'SET id_periferico = id_periferico' serve como um "coringa neutro"
    # para permitir que as próximas cláusulas sejam adicionadas com vírgula (Ex: ", marca = ?")
    sql = "UPDATE perifericos SET id_periferico = id_periferico"

    item_id = request.form.get('id_periferico')
    item_nome = request.form.get("categoria")
    item_marca = request.form.get('marca')
    item_numero_de_serie = request.form.get('num_serie')
    item_icone = request.form.get('icone')
    status = request.form.get('filtro_status')

    paramentros = []

    if item_nome:
        sql += ", categoria = ?"
        paramentros.append(item_nome)

    if item_marca:
        sql += ", marca = ?"
        paramentros.append(item_marca)

    if item_numero_de_serie:
        sql += ", num_serie = ?"
        paramentros.append(item_numero_de_serie)

    if item_icone:
        sql += ", icone = ?"
        paramentros.append(icone_valido(item_icone))

    # "todos" (= "Manter status atual" no formulário) não altera o status
    if status and status != "todos":
        if status == "disponivel":
            sql += ", disponivel = 1, inativo = 0, manutencao = 0"
            cursor.execute("UPDATE emprestimos SET devolvido = 1 WHERE id_periferico = ?", (item_id,))
        elif status == "emuso":
            sql += ", disponivel = 0, inativo = 0, manutencao = 0"
        elif status == "manutencao":
            sql += ", disponivel = 0, manutencao = 1, inativo = 0"
        elif status == "inativo":
            sql += ", disponivel = 0, manutencao = 0, inativo = 1"

    sql += " WHERE id_periferico = ?"
    paramentros.append(item_id)

    cursor.execute(sql, paramentros)
    conexao.commit()
    conexao.close()

    flash("Equipamento atualizado com sucesso!", "success")
    return redirect('/equipamentos')
