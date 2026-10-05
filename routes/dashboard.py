from flask import Blueprint, redirect, render_template, request, session
from banco import conectar_banco, listar_icones

# Colunas explícitas: [0]id [1]categoria [2]marca [3]nº série [4]disponível [5]manutenção [6]inativo [7]nome da categoria [8]ícone
SELECT_EQUIPAMENTOS = """SELECT p.id_periferico, p.categoria, p.marca, p.num_serie, p.disponivel, p.manutencao, p.inativo, c.categoria, p.icone,p.unid_origem, p.setor_origem,p.unid_atual,p.setor_atual
        FROM perifericos p JOIN categorias c ON p.categoria = c.id_categoria WHERE 1=1"""

# Definição dos Blueprints para o Painel Principal (Dashboard) e Gestão de Equipamentos
route_dashboard = Blueprint('dashboard', __name__)
route_equipamentos = Blueprint('equipamentos', __name__)


# Rota do Dashboard: calcula e exibe as estatísticas gerais do estoque de periféricos
@route_dashboard.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
  # Verificação de segurança: impede o acesso e redireciona para o login caso não haja sessão ativa
  if not session.get('usuario_email'):
    return redirect('/login')

  conexao = conectar_banco()
  cursor = conexao.cursor()

  # Recupera os dados do usuário logado armazenados na sessão
  name = session.get('usuario_name')
  email = session.get('usuario_email')
  telefone = session.get('usuario_telefone')

  # Consulta todos os equipamentos cadastrados no banco de dados
  cursor.execute('SELECT * FROM perifericos')
  perifericos = cursor.fetchall()
  total_perifericos = len(perifericos)

  cursor.execute("""
            SELECT e.*, c.categoria, p.num_serie, p.id_periferico, p.unid_origem, p.setor_origem 
            FROM emprestimos e 
            JOIN perifericos p ON e.id_periferico = p.id_periferico
            JOIN categorias c ON p.categoria = c.id_categoria
            WHERE 1=1 ORDER BY e.id_emprestimo DESC LIMIT 10
        """)
  emprestimos = cursor.fetchall()

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

  # Converte para string para garantir comparação idêntica se o ID for int ou str
  is_admin = str(session.get('usuario_admin')) == '1'
  template_dashboard = 'dashboard.html' if is_admin else 'user_dashboard.html'

  return render_template(
      template_dashboard,
      name=name,
      email=email,
      telefone=telefone,
      total_perifericos=total_perifericos,
      disponiveis=disponiveis,
      usados=usados,
      manutencao=manutencao,
      emprestimos=emprestimos,
  )


# Rota de Equipamentos: gerencia a listagem e os filtros de pesquisa do inventário
@route_equipamentos.route('/equipamentos', methods=['GET', 'POST'])
def equipamentos():
  # Bloqueio de acesso para usuários não autenticados
  if not session.get('usuario_email'):
    return redirect('/login')

  # Seleciona o template dinamicamente prevenindo falhas de tipo (int vs str)
  is_admin = str(session.get('usuario_admin')) == '1'
  template_alvo = (
      'equipamentos.html' if is_admin else 'user_equipamentos.html'
  )

  # Requisição GET: Carregamento padrão listando apenas equipamentos que não estejam inativos
  if request.method == 'GET':
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute(SELECT_EQUIPAMENTOS + ' AND p.inativo != 1')
    perifericos = cursor.fetchall()
    cursor.execute('SELECT * FROM categorias WHERE excluido != 1')
    categorias = cursor.fetchall()
    conexao.close()

    return render_template(
        template_alvo,
        perifericos=perifericos,
        categorias=categorias,
        icones=listar_icones(),
        categoria='todos',
        status='todos',
        name=session.get('usuario_name'),
    )

  # Requisição POST: Aplicação de filtros combinados
  if request.method == 'POST':
    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Normaliza as entradas do formulário com fallback seguro (.get)
    categoria = request.form.get('filtro_categoria', 'todos').strip().lower()
    status = request.form.get('filtro_status', 'todos').strip().lower()
    marca = request.form.get('filtro_marca', '').strip().lower()

    # Estrutura inicial da instrução SQL dinâmica
    sql = SELECT_EQUIPAMENTOS
    paramentros = []

    if categoria != 'todos':
      sql += ' AND p.categoria = ?'
      paramentros.append(categoria)

    if marca != '':
      sql += " AND LOWER(p.marca) LIKE '%' || ? || '%'"
      paramentros.append(marca)

    if status == 'disponivel':
      sql += ' AND p.disponivel = 1'
    elif status == 'emuso':
      sql += ' AND p.disponivel = 0 AND p.manutencao = 0 AND p.inativo = 0'
    elif status == 'manutencao':
      sql += ' AND p.disponivel = 0 AND p.manutencao = 1 AND p.inativo = 0'
    elif status == 'inativo':
      sql += ' AND p.inativo = 1'
    elif status == 'todos':
      sql += ' AND p.inativo != 1'
    elif status == 'transferido':
      sql += (
          ' AND p.disponivel = 0 AND p.manutencao = 0 AND p.inativo = 0 AND'
          ' p.transferido = 1'
      )

    cursor.execute(sql, paramentros)
    perifericos = cursor.fetchall()

    cursor.execute('SELECT * FROM categorias WHERE excluido != 1')
    categorias = cursor.fetchall()
    conexao.close()

    return render_template(
        template_alvo,
        perifericos=perifericos,
        categorias=categorias,
        icones=listar_icones(),
        categoria=categoria,
        status=status,
        name=session.get('usuario_name'),
    )