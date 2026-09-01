from flask import Blueprint, render_template, request, redirect, session
from banco import conectar_banco

# Blueprint para a rota de criação de itens
route_createitem = Blueprint('createitem', __name__)

@route_createitem.route('/createitem', methods=['GET', 'POST'])
def create():
    if not session.get("usuario_email"):
            return redirect ('/login')
    if request.method == 'GET':
        return render_template("createitem.html")
    if request.method == 'POST':
        # Conexão com o banco de dados
        conexao = conectar_banco()
        cursor = conexao.cursor()

            # Captura os dados do formulário de criação
        item_name = request.form["item_name"]
        item_marca = request.form["item_marca"]
        item_numero_de_serie = request.form["item_numero_de_serie"]

        cursor.execute("INSERT INTO perifericos (periferico, Marca, Número de série) VALUES (?, ?, ?)", (item_name, item_marca, item_numero_de_serie))
        conexao.commit()
        conexao.close()
        return redirect('/createitem')