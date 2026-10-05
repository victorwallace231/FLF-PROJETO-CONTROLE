from flask import Blueprint, redirect, render_template, request, session
from banco import conectar_banco, listar_icones

# AQUI ESTÁ A CORREÇÃO PRINCIPAL: p.transferido foi adicionado no final do SELECT
SELECT_EQUIPAMENTOS = """SELECT p.id_periferico, p.categoria, p.marca, p.num_serie, p.disponivel, p.manutencao, p.inativo, c.categoria, p.icone, p.unid_origem, p.setor_origem, p.unid_atual, p.setor_atual, p.transferido
        FROM perifericos p JOIN categorias c ON p.categoria = c.id_categoria WHERE 1=1"""

route_dashboard = Blueprint('dashboard', __name__)
route_equipamentos = Blueprint('equipamentos', __name__)


@route_dashboard.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
  if not session.get('usuario_email'):
    return redirect('/login')

  conexao = conectar_banco()
  cursor = conexao.cursor()

  name = session.get('usuario_name')
  email = session.get('usuario_email')
  telefone = session.get('usuario_telefone')

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

  disponiveis = 0
  usados = 0
  manutencao = 0

  for periferico in perifericos:
    if periferico[4] == True:
      disponiveis += 1
    elif periferico[4] == False and periferico[5] == False and periferico[6] == 0:
      usados += 1
    elif periferico[4] == False and periferico[5] == True and periferico[6] == 0:
      manutencao += 1

  conexao.close()

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


@route_equipamentos.route('/equipamentos', methods=['GET', 'POST'])
def equipamentos():
  if not session.get('usuario_email'):
    return redirect('/login')

  is_admin = str(session.get('usuario_admin')) == '1'
  template_alvo = (
      'equipamentos.html' if is_admin else 'user_equipamentos.html'
  )

  if request.method == 'GET':
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute(SELECT_EQUIPAMENTOS)
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

  if request.method == 'POST':
    conexao = conectar_banco()
    cursor = conexao.cursor()

    categoria = request.form.get('filtro_categoria', 'todos').strip().lower()
    status = request.form.get('filtro_status', 'todos').strip().lower()
    marca = request.form.get('filtro_marca', '').strip().lower()

    sql = SELECT_EQUIPAMENTOS
    paramentros = []

    if categoria != 'todos':
      sql += ' AND p.categoria = ?'
      paramentros.append(categoria)

    if marca != '':
      sql += " AND LOWER(p.marca) LIKE '%' || ? || '%'"
      paramentros.append(marca)

    if status == 'disponivel':
      sql += (
          ' AND (p.disponivel = 1 OR p.disponivel = "1") AND'
          ' COALESCE(p.manutencao, 0) NOT IN (1, "1") AND COALESCE(p.inativo, 0)'
          ' NOT IN (1, "1")'
      )
    elif status == 'emuso':
      sql += (
          ' AND COALESCE(p.disponivel, 0) NOT IN (1, "1") AND'
          ' COALESCE(p.manutencao, 0) NOT IN (1, "1") AND COALESCE(p.inativo, 0)'
          ' NOT IN (1, "1")'
      )
    elif status == 'manutencao':
      sql += (
          ' AND COALESCE(p.disponivel, 0) NOT IN (1, "1") AND (p.manutencao ='
          ' 1 OR p.manutencao = "1") AND COALESCE(p.inativo, 0) NOT IN (1, "1")'
      )
    elif status == 'inativo':
      sql += ' AND (p.inativo = 1 OR p.inativo = "1")'
    elif status == 'transferido':
      sql += (
          ' AND COALESCE(p.disponivel, 0) NOT IN (1, "1") AND'
          ' COALESCE(p.manutencao, 0) NOT IN (1, "1") AND COALESCE(p.inativo, 0)'
          ' NOT IN (1, "1") AND (p.transferido = 1 OR p.transferido = "1")'
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