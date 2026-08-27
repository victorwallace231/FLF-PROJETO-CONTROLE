from flask import Blueprint, render_template, request, redirect
from banco import conectar_banco

# Blueprint para a rota de criação de itens
route_createitem = Blueprint('createitem', __name__)

@route_createitem.route('/createitem', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('createitem.html')
    if request.method == 'POST':
        conexao = conectar_banco()
        cursor = conexao.cursor()

        # Captura os dados do formulário de criação
        item_name = request.form['item_name']
        item_marca = request.form['item_marca']
        item_numero_de_serie = request.form['item_numero_de_serie']
        item_description = request.form['item_description']

        cursor.execute("INSERT INTO perifericos (item_name, item_marca, item_numero_de_serie, item_description) VALUES (?, ?, ?, ?)", (item_name, item_marca, item_numero_de_serie, item_description))
        conexao.commit()
        conexao.close()
        return redirect('/createitem')