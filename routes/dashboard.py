from flask import Blueprint, render_template, request ,session
from banco import conectar_banco

# Blueprint para a rota do dashboard
route_dashboard = Blueprint('dashboard', __name__)

# Rota do dashboard
@route_dashboard.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # Conecta ao banco de dados
    conexao = conectar_banco()
    cursor = conexao.cursor()

    name = session.get('usuario_name')  # Obtém o nome do usuário da sessão
    email = session.get('usuario_email')  # Obtém o email do usuário da sessão
    telefone = session.get('usuario_telefone')  # Obtém o telefone do usuário da sessão
    # Renderiza o template do dashboard com os dados do usuário
    return render_template('dashboard.html', name=name, email=email, telefone=telefone)
