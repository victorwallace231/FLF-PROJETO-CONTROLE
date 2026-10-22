from flask import Blueprint, redirect, render_template, request, session
from banco import conectar_banco, listar_icones

# A consulta mantém os índices já usados pelos templates: origem nos índices 9/10,
# localização atual nos índices 11/12 e IDs de origem nos índices 14/15. Os IDs atuais
# entram no final (16/17), evitando quebrar as janelas existentes.
SELECT_EQUIPAMENTOS = """SELECT
            p.id_periferico, p.categoria, p.marca, p.num_serie,
            p.disponivel, p.manutencao, p.inativo, c.categoria, p.icone,
            uo.nome_unidade, so.nome_setor, ua.nome_unidade, sa.nome_setor,
            p.transferido, p.id_unidade_origem, p.id_setor_origem,
            p.id_unidade_atual, p.id_setor_atual
        FROM perifericos p
        JOIN categorias c ON p.categoria = c.id_categoria
        LEFT JOIN unidades uo ON uo.id_unidade = p.id_unidade_origem
        LEFT JOIN setores so ON so.id_setor = p.id_setor_origem
        LEFT JOIN unidades ua ON ua.id_unidade = p.id_unidade_atual
        LEFT JOIN setores sa ON sa.id_setor = p.id_setor_atual
        WHERE 1=1"""

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
      SELECT
          e.id_emprestimo,
          e.resp_origem,
          e.data_saida,
          e.id_periferico,
          e.tel_resp_origem,
          e.id_usuario,
          e.observacao,
          e.setor_dest,
          e.unid_dest,
          e.tipo_transfer,
          e.resp_dest,
          e.tel_resp_dest,
          c.categoria AS categoria_nome,
          p.num_serie,
          p.id_periferico AS periferico_id,
          u.nome_unidade AS unid_origem,
          s.nome_setor AS setor_origem
      FROM emprestimos e
      JOIN perifericos p ON e.id_periferico = p.id_periferico
      JOIN categorias c ON p.categoria = c.id_categoria
      LEFT JOIN unidades u ON u.id_unidade = p.id_unidade_origem
      LEFT JOIN setores s ON s.id_setor = p.id_setor_origem
      WHERE 1=1
      ORDER BY e.id_emprestimo DESC
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

  is_admin = session.get('usuario_role') == 'admin';
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

  is_admin = session.get('usuario_role') == 'admin'
  template_alvo = 'equipamentos.html' if is_admin else 'user_equipamentos.html'

  conexao = conectar_banco()
  cursor = conexao.cursor()

  categoria = request.form.get('filtro_categoria', 'todos').strip() if request.method == 'POST' else 'todos'
  status = request.form.get('filtro_status', 'todos').strip().lower() if request.method == 'POST' else 'todos'
  marca = request.form.get('filtro_marca', '').strip() if request.method == 'POST' else ''
  unidade_atual = request.form.get('filtro_unidade_atual', '').strip() if request.method == 'POST' else ''
  setor_atual = request.form.get('filtro_setor_atual', '').strip() if request.method == 'POST' else ''

  sql = SELECT_EQUIPAMENTOS
  parametros = []

  if categoria != 'todos':
    sql += ' AND p.categoria = ?'
    parametros.append(categoria)

  if marca:
    sql += " AND (LOWER(COALESCE(p.marca, '')) LIKE '%' || ? || '%' OR LOWER(COALESCE(p.num_serie, '')) LIKE '%' || ? || '%')"
    busca = marca.lower()
    parametros.extend([busca, busca])

  if unidade_atual:
    if unidade_atual.isdigit():
      sql += ' AND p.id_unidade_atual = ?'
      parametros.append(int(unidade_atual))
    else:
      # Valor inesperado enviado manualmente não deve ampliar a consulta.
      sql += ' AND 1 = 0'

  if setor_atual:
    if setor_atual.isdigit():
      sql += ' AND p.id_setor_atual = ?'
      parametros.append(int(setor_atual))
    else:
      sql += ' AND 1 = 0'

  if status == 'disponivel':
    sql += (' AND (p.disponivel = 1 OR p.disponivel = "1") AND'
            ' COALESCE(p.manutencao, 0) NOT IN (1, "1") AND COALESCE(p.inativo, 0) NOT IN (1, "1")')
  elif status == 'emuso':
    sql += (' AND COALESCE(p.disponivel, 0) NOT IN (1, "1") AND'
            ' COALESCE(p.manutencao, 0) NOT IN (1, "1") AND COALESCE(p.inativo, 0) NOT IN (1, "1")')
  elif status == 'manutencao':
    sql += (' AND COALESCE(p.disponivel, 0) NOT IN (1, "1") AND (p.manutencao = 1 OR p.manutencao = "1")'
            ' AND COALESCE(p.inativo, 0) NOT IN (1, "1")')
  elif status == 'inativo':
    sql += ' AND (p.inativo = 1 OR p.inativo = "1")'
  elif status == 'transferido':
    sql += (' AND COALESCE(p.disponivel, 0) NOT IN (1, "1") AND'
            ' COALESCE(p.manutencao, 0) NOT IN (1, "1") AND COALESCE(p.inativo, 0) NOT IN (1, "1")'
            ' AND (p.transferido = 1 OR p.transferido = "1")')

  sql += ' ORDER BY p.id_periferico DESC'
  cursor.execute(sql, parametros)
  perifericos = cursor.fetchall()

  cursor.execute('SELECT * FROM categorias WHERE excluido != 1 ORDER BY categoria COLLATE NOCASE')
  categorias = cursor.fetchall()
  conexao.close()

  return render_template(
      template_alvo,
      perifericos=perifericos,
      categorias=categorias,
      icones=listar_icones(),
      categoria=categoria,
      status=status,
      marca=marca,
      unidade_atual=unidade_atual,
      setor_atual=setor_atual,
      name=session.get('usuario_name'),
  )
