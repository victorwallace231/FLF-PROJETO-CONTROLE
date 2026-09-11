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
        # Captura os dados do formulário de atualização
        item_id = request.form['id_periferico']
        item_nome = request.form['categoria']
        item_marca = request.form['marca']
        item_numero_de_serie = request.form['num_serie']
        status = request.form['filtro_status']

        cursor.execute("UPDATE perifericos SET periferico = ?, marca = ?, num_serie = ? WHERE id_periferico", (item_nome, item_marca, item_numero_de_serie, item_id))
        conexao.commit()
        conexao.close()
        return redirect('/equipamentos')