from flask import Blueprint, render_template, request, redirect, session
from banco import conectar_banco

# Blueprint para a rota de criação de itens
route_create_item = Blueprint('create_item', __name__)

@route_create_item.route('/create_item', methods=['GET', 'POST'])
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
        periferico = request.form["categoria"].strip().lower()
        marca = request.form["marca"].strip().lower()
        num_serie = request.form["num_serie"].strip().lower()

        cursor.execute("INSERT INTO perifericos (periferico, marca, num_serie, disponivel, manutencao) VALUES (?, ?, ?,1,0)", (periferico, marca, num_serie))
        conexao.commit()
        conexao.close()
        return redirect('/create_item')