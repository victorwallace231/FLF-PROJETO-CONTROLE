import sqlite3
from flask import Blueprint, redirect, session, render_template, request, jsonify
from banco import conectar_banco

# Configuração dos Blueprints para separar a estrutura de rotas do Flask
verifica_emprestimos = Blueprint('verifica_emprestimos', __name__)
verifica_1emprestimo = Blueprint('verifica_1emprestimo', __name__)

# Rota responsável por carregar a página de movimentações e filtrar os registros gerais
@verifica_emprestimos.route('/verifica_emprestimos', methods=['GET', 'POST'])
def verificar_emprestimos():
    # Controle de acesso: redireciona para o login caso o usuário não esteja autenticado
    if not session.get("usuario_email"):
        return redirect('/login')

    # Requisição GET: Carregamento inicial da página com todos os registros
    if request.method == 'GET':
        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute("""SELECT * FROM categorias WHERE excluido !=1""")
        categorias = cursor.fetchall()
        # Consulta com JOIN para combinar dados do empréstimo aos detalhes do periférico
        cursor.execute("""
            SELECT e.*, c.categoria, p.num_serie, p.id_periferico 
            FROM emprestimos e 
            JOIN perifericos p ON e.id_periferico = p.id_periferico
            JOIN categorias c ON p.categoria = c.id_categoria
            WHERE 1=1 ORDER BY e.id_emprestimo DESC
        """)

        movimentacoes = cursor.fetchall()
        conexao.close()
        
        # Renderiza o HTML passando a lista completa e o nome da sessão do usuário
        return render_template("movimentacao.html", movimentacoes=movimentacoes, categorias = categorias,name=session.get("usuario_name"))

    # Requisição POST: Processa os filtros de busca enviados pelo formulário
    if request.method == 'POST':
        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute("""SELECT * FROM categorias WHERE excluido !=1""")
        categorias = cursor.fetchall()
        
        # Captura os campos de filtro do formulário HTML
        status = request.form["filtro_status"].strip()
        categoria = request.form["filtro_categoria"].strip()
        responsavel = request.form["filtro_responsavel"].strip().lower()

        # Estrutura base da query SQL
        sql = """
            SELECT e.*, c.categoria, p.num_serie, p.id_periferico 
            FROM emprestimos e 
            JOIN perifericos p ON e.id_periferico = p.id_periferico
            JOIN categorias c ON p.categoria = c.id_categoria
            WHERE 1=1
        """

        paramentros = []

        # Concatena condição SQL se uma categoria específica for selecionada
        if categoria != "todos":
             sql += " AND p.categoria = ?"
             paramentros.append(categoria)

        # Concatena condição SQL se o status for filtrado (1 = devolvido, 0 = em uso)
        if status != "todos":
             status_tranlate = 1 if status == "devolvido" else 0
             sql += " AND e.devolvido = ?"
             paramentros.append(status_tranlate)

        # Concatena condição SQL se houver busca por nome do responsável
        if responsavel:
             sql += " AND LOWER(e.responsavel) LIKE '%' || ? || '%'"
             paramentros.append(responsavel)

        # Define ordenação decrescente (mais recentes primeiro)
        sql += " ORDER BY e.id_emprestimo DESC"

        # Executa a busca parametrizada evitando vulnerabilidades de SQL Injection


        cursor.execute(sql, paramentros)
        movimentacoes = cursor.fetchall()
        conexao.close()

        # Recarrega a página exibindo apenas os resultados filtrados
        return render_template("movimentacao.html", movimentacoes = movimentacoes, categorias=categorias, categoria = categoria, status = status,name=session.get("usuario_name"))


# Rota da API (endpoint JSON) para consulta do histórico de um periférico individual
@verifica_1emprestimo.route('/verifica_1emprestimo', methods=['POST'])
def verifica():
     if request.method == 'POST':
          conexao = conectar_banco()
          # Configura o SQLite para associar os nomes das colunas aos valores trazidos
          conexao.row_factory = sqlite3.Row
          cursor = conexao.cursor()

          # Captura o ID do equipamento enviado assincronamente pelo JavaScript
          id_periferico = request.form.get("id_periferico")

          # Seleciona todo o histórico de empréstimos do periférico informado
          cursor.execute("SELECT * FROM emprestimos WHERE id_periferico = ? ORDER BY id_emprestimo DESC", (id_periferico,))
          emprestimos = cursor.fetchall()

          # Converte a lista de objetos sqlite3.Row em uma lista de dicionários padrão do Python
          lista_emprestimos = [dict(emprestimo) for emprestimo in emprestimos]
          conexao.close()

          # Retorna a lista de registros formatada em JSON para a chamada do fetch() no front-end
          return jsonify(lista_emprestimos)