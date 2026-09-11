from flask import Blueprint, render_template, request, redirect, session
from banco import conectar_banco

route_updateitem = Blueprint('update_item', __name__)

@route_updateitem.route('/update_item', methods=['POST'])
def update():
    if not session.get("usuario_email"):
           return redirect ('/login')
    if request.method == 'POST':
        conexao = conectar_banco()
        cursor = conexao.cursor()
        sql = """UPDATE perifericos SET id_periferico = id_periferico"""
        # Captura os dados do formulário de atualização
        item_id = request.form.get('id_periferico')
        item_nome = request.form.get("categoria")
        item_marca = request.form.get('marca')
        item_numero_de_serie = request.form.get('num_serie')
        status = request.form.get('filtro_status')
        paramentros = []

        if item_nome:
             sql+= ", periferico = ?"
             paramentros.append(item_nome)

        if item_marca:
             sql+= ", marca = ?"
             paramentros.append(item_marca)
        if item_numero_de_serie != "":
            sql+= ", num_serie = ?"
            paramentros.append(item_numero_de_serie)
        if status != "":
            if status == "disponivel":
                sql += ", disponivel = 1, inativo = 0, manutencao = 0"
            elif status == "emuso":
                sql += ", disponivel = 0, inativo = 0, manutencao = 0"
            elif status == "manutencao":
                sql += ", disponivel = 0, manutencao = 1, inativo = 0"
            elif status == "inativo":
                sql += ", disponivel = 0, manutencao = 0, inativo = 1"
        if item_numero_de_serie:
            sql += ", num_serie = ?"
            paramentros.append(item_numero_de_serie)

        sql += " WHERE id_periferico = ?"
        paramentros.append(item_id)

        cursor.execute(sql,paramentros)

        conexao.commit()
        conexao.close()
        return redirect('/equipamentos')