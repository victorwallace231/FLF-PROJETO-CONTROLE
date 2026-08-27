from flask import Blueprint, render_template, request, redirect
from banco import conectar_banco

route_updateitem = Blueprint('updateitem', __name__)

@route_updateitem.route('/updateitem', methods=['GET', 'POST'])
def update():
    if request.method =='GET':
        return render_template('updateitem.html')
    if request.method == 'POST':
        conexao = conectar_banco()
        cursor = conexao.cursor()
        # Captura os dados do formulário de atualização
        item_id = request.form['item_id']
        item_nome = request.form['item_nome']
        item_marca = request.form['item_marca']
        item_numero_de_serie = request.form['item_numero_de_serie']
        item_descricao = request.form['item_descricao']

        cursor.execute("UPDATE perifericos SET item_nome = ?, item_marca = ?, item_numero_de_serie = ?, item_descricao = ? WHERE id = ?", (item_nome, item_marca, item_numero_de_serie, item_descricao, item_id))
        conexao.commit()
        conexao.close()
        return redirect('/dashboard')