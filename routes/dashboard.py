from flask import Blueprint, render_template, request ,session, redirect
from banco import conectar_banco

# Blueprint para a rota do dashboard
route_dashboard = Blueprint('dashboard', __name__)
route_equipamentos = Blueprint('equipamentos', __name__)

# Rota do dashboard
@route_dashboard.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get("usuario_email"):
        return redirect ('/login') 
        # Conecta ao banco de dados
    conexao = conectar_banco()
    cursor = conexao.cursor()

    name = session.get('usuario_name')  # Obtém o nome do usuário da sessão
    email = session.get('usuario_email')  # Obtém o email do usuário da sessão
    telefone = session.get('usuario_telefone')  # Obtém o telefone do usuário da sessão
    # Renderiza o template do dashboard com os dados do usuário

    cursor.execute("SELECT * FROM perifericos")
    perifericos = cursor.fetchall()
    total_perifericos = len(perifericos)
    disponiveis = 0
    usados = 0
    manutencao = 0
    for periferico in perifericos:
        if periferico[4] == True:
            disponiveis += 1
        elif periferico[4] == False and periferico[5] == False:
            usados += 1
        elif periferico[4] == False and periferico[5] == True:
            manutencao += 1

    conexao.close()
    return render_template('dashboard.html', name=name, email=email, telefone=telefone, perifericos=perifericos, disponiveis=disponiveis, usados=usados, manutencao=manutencao, total_perifericos=total_perifericos)

@route_equipamentos.route('/equipamentos', methods=['GET', 'POST'])
def equipamentos():
    if not session.get("usuario_email"):
        return redirect('/login')
    if request.method == 'GET':
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM perifericos")
        perifericos = cursor.fetchall()
        conexao.close()
        return render_template("equipamentos.html", perifericos = perifericos)
    if request.method == 'POST':
        conexao = conectar_banco()
        cursor = conexao.cursor()
        categoria = request.form["filtro_categoria"]
        status = request.form ["filtro_status"]
        status_translate = False
        manutencao = False

        if categoria == "todos" and status == "todos":
            cursor.execute("SELECT * FROM perifericos")
        elif status == "todos":
            cursor.execute("SELECT * FROM perifericos WHERE periferico = ?",(categoria,))
        elif status == "manutencao":
            if categoria == "todos":
                cursor.execute("SELECT * FROM perifericos WHERE manutencao = 1")
            else:
                cursor.execute("SELECT * FROM perifericos WHERE periferico = ? AND manutencao = 1", (categoria,))
        else:
            status_translate = 1 if status == "disponivel" else 0
            if categoria == "todos":
                cursor.execute("SELECT * FROM perifericos WHERE disponivel = ? AND manutencao = 0", (status_translate,))
            else:
                cursor.execute("SELECT * FROM perifericos WHERE periferico = ? AND  disponivel = ? AND manutencao = 0", (categoria , status_translate,))
    perifericos = cursor.fetchall()
    conexao.close()
    return render_template("equipamentos.html", perifericos = perifericos)
        
        



        
                

