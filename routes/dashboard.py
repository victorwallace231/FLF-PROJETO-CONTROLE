from flask import Blueprint, render_template, request
from banco import conectar_banco

route_dashboard = Blueprint('dashboard', __name__)
@route_dashboard.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM usuario")
    usuario = cursor.fetchall()
    conexao.close()

    return render_template('dashboard.html', usuarios=usuario)