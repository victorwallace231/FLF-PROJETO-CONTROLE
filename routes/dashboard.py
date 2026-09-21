from flask import Blueprint, render_template, request, session, redirect
from banco import conectar_banco

# Definição dos Blueprints para o Painel Principal (Dashboard) e Gestão de Equipamentos
route_dashboard = Blueprint('dashboard', __name__)
route_equipamentos = Blueprint('equipamentos', __name__)

# Rota do Dashboard: calcula e exibe as estatísticas gerais do estoque de periféricos
@route_dashboard.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # Verificação de segurança: impede o acesso e redireciona para o login caso não haja sessão ativa
    if not session.get("usuario_email"):
        return redirect('/login') 

    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Recupera os dados do usuário logado armazenados na sessão
    name = session.get('usuario_name')
    email = session.get('usuario_email')
    telefone = session.get('usuario_telefone')

    # Consulta todos os equipamentos cadastrados no banco de dados
    cursor.execute("SELECT * FROM perifericos")
    perifericos = cursor.fetchall()
    total_perifericos = len(perifericos)

    # Inicializa os contadores para consolidação dos cards do dashboard
    disponiveis = 0
    usados = 0
    manutencao = 0

    # Percorre a lista avaliando as colunas booleanas: [4] disponivel, [5] manutencao, [6] inativo
    for periferico in perifericos:
        if periferico[4] == True:
            disponiveis += 1
        elif periferico[4] == False and periferico[5] == False and periferico[6] == 0:
            usados += 1
        elif periferico[4] == False and periferico[5] == True and periferico[6] == 0:
            manutencao += 1

    conexao.close()

    # Renderiza o painel passando o usuário e as métricas calculadas
    return render_template(
        'dashboard.html', 
        name=name, 
        email=email, 
        telefone=telefone, 
        perifericos=perifericos, 
        disponiveis=disponiveis, 
        usados=usados, 
        manutencao=manutencao, 
        total_perifericos=total_perifericos
    )

# Rota de Equipamentos: gerencia a listagem e os filtros de pesquisa do inventário
@route_equipamentos.route('/equipamentos', methods=['GET', 'POST'])
def equipamentos():
    # Bloqueio de acesso para usuários não autenticados
    if not session.get("usuario_email"):
        return redirect('/login')

    # Requisição GET: Carregamento padrão listando apenas equipamentos que não estejam inativos (inativo != 1)
    if request.method == 'GET':
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("""SELECT p.*, c.* FROM perifericos p
        JOIN categorias c ON p.categoria = c.id_categoria WHERE 1=1 AND p.inativo != 1""")
        perifericos = cursor.fetchall()
        cursor.execute("SELECT * FROM categorias")
        categorias = cursor.fetchall()
        conexao.close()
        return render_template("equipamentos.html", perifericos=perifericos, categorias=categorias, name=session.get("usuario_name"))

    # Requisição POST: Aplicação de filtros combinados (categoria, marca/modelo e status)
    if request.method == 'POST':
        conexao = conectar_banco()
        cursor = conexao.cursor()

        # Normaliza as entradas do formulário
        categoria = request.form["filtro_categoria"].strip().lower()
        status = request.form["filtro_status"].strip().lower()
        marca = request.form["filtro_marca"].strip().lower()

        # Estrutura inicial da instrução SQL dinâmica
        sql = """SELECT p.*, c.* FROM perifericos p
        JOIN categorias c ON p.categoria = c.id_categoria WHERE 1=1"""
        paramentros = []

        # Adiciona cláusula para filtro por categoria
        if categoria != "todos":
            sql += " AND p.categoria = ?"
            paramentros.append(categoria)

        # Adiciona cláusula para busca por texto de marca/modelo
        if marca != "":
            sql += " AND LOWER(p.marca) LIKE '%' || ? || '%'"
            paramentros.append(marca)

        # Mapeia as combinações lógicas das colunas para os status selecionados
        if status == "disponivel":
            sql += " AND p.disponivel = 1"
        elif status == "emuso":
            sql += " AND p.disponivel = 0 AND p.manutencao = 0 AND p.inativo = 0"
        elif status == "manutencao":
            sql += " AND p.disponivel = 0 AND p.manutencao = 1 AND p.inativo = 0"
        elif status == "inativo":
            sql += " AND p.inativo = 1"
            
        # Executa a busca parametrizada evitando SQL Injection
        cursor.execute(sql, paramentros)
        perifericos = cursor.fetchall()

        cursor.execute ("SELECT * FROM categorias")
        categorias = cursor.fetchall()
        
        conexao.close()

        # Recarrega a página exibindo a tabela refinada pelos filtros
        return render_template("equipamentos.html", perifericos=perifericos, categorias=categorias, categoria = categoria, status = status,name=session.get("usuario_name"))