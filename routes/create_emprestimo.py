from datetime import datetime  # <--- ALTERADO: Importa datetime em vez de date
import re
from banco import conectar_banco
from flask import Blueprint, flash, redirect, render_template, request, session

# Definição do Blueprint para as rotas de criação e registro de novos empréstimos
create_emprestimo = Blueprint('create_emprestimo', __name__)


@create_emprestimo.route('/create_emprestimo', methods=['GET', 'POST'])
def create():
  # Verificação de segurança: bloqueia o acesso se o usuário não estiver logado
  if not session.get('usuario_email'):
    return redirect('/login')

  # Requisição GET: Carrega o formulário de cadastro de movimentação
  if request.method == 'GET':
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""SELECT p.id_periferico, p.categoria, p.marca, p.num_serie, p.disponivel, p.manutencao, p.inativo, c.categoria, p.icone
        FROM perifericos p JOIN categorias c ON p.categoria = c.id_categoria WHERE p.inativo!= 1 """)
    perifericos = cursor.fetchall()
    conexao.close()

    return render_template(
        'createmov.html',
        perifericos=perifericos,
        name=session.get('usuario_name'),
    )

  # Requisição POST: Processa a criação do novo empréstimo no sistema
  if request.method == 'POST':
    conexao = conectar_banco()
    cursor = conexao.cursor()

    # --- ALTERAÇÃO AQUI: Registra a data e hora atual no formato 'DD/MM/AAAA HH:MM:SS' ---
    agora = datetime.now()
    data_formatada = agora.strftime('%d/%m/%Y %H:%M:%S')

    # Captura as informações digitadas no formulário
    responsavel = request.form['responsavel']
    id_periferico = request.form['id_periferico']
    tel_responsavel = re.sub(r'\D', '', request.form['tel_responsavel'])
    observacao = request.form['observacao']
    setor_dest = request.form.get('setor_dest', '').upper().strip()
    unid_dest = request.form.get('unid_dest', '').upper().strip()
    tipo_transfer = request.form.get('tipo_transfer', '').strip()
    filtro_transfer = tipo_transfer.strip().lower()

    # 1. Atualiza a tabela 'perifericos'
    cursor.execute(
        'UPDATE perifericos SET disponivel = 0 WHERE id_periferico = ?',
        (id_periferico,),
    )

    match filtro_transfer:
      case 'transferencia de unidade' | 'transferência de localização':
        cursor.execute(
            """
                    UPDATE perifericos 
                    SET unid_atual = ?, setor_atual = ?, disponivel = 0, manutencao = 0, inativo = 0, transferido = 1
                    WHERE id_periferico = ?
                """,
            (unid_dest, setor_dest, id_periferico),
        )

      case 'remessa para concerto':
        cursor.execute(
            """
                    UPDATE perifericos 
                    SET unid_atual = ?, setor_atual = ?, disponivel = 0, manutencao = 1, inativo = 0, transferido = 0
                    WHERE id_periferico = ?
                """,
            (unid_dest, setor_dest, id_periferico),
        )

      case 'retorno de concerto':
        cursor.execute(
            """
                    UPDATE perifericos 
                    SET unid_atual = ?, setor_atual = ?, disponivel = 1, manutencao = 0, inativo = 0, transferido = 0
                    WHERE id_periferico = ?
                """,
            (unid_dest, setor_dest, id_periferico),
        )

      case 'baixa por defeito' | 'baixa por fora de uso/obsoleto':
        cursor.execute(
            """
                    UPDATE perifericos 
                    SET unid_atual = ?, setor_atual = ?, disponivel = 0, manutencao = 0, inativo = 1, transferido = 0
                    WHERE id_periferico = ?
                """,
            (unid_dest, setor_dest, id_periferico),
        )

      case 'empréstimo' | 'evento':
        cursor.execute(
            """
                    UPDATE perifericos 
                    SET unid_atual = ?, setor_atual = ?, disponivel = 0, manutencao = 0, inativo = 0, transferido = 0
                    WHERE id_periferico = ?
                """,
            (unid_dest, setor_dest, id_periferico),
        )

      case 'retorno de empréstimo':
        cursor.execute(
            """
                    UPDATE perifericos 
                    SET unid_atual = ?, setor_atual = ?, disponivel = 1, manutencao = 0, inativo = 0, transferido = 0
                    WHERE id_periferico = ?
                """,
            (unid_dest, setor_dest, id_periferico),
        )

      case _:
        cursor.execute(
            """
                    UPDATE perifericos 
                    SET unid_atual = ?, setor_atual = ?, disponivel = 1, manutencao = 0, inativo = 0, transferido = 0
                    WHERE id_periferico = ?
                """,
            (unid_dest, setor_dest, id_periferico),
        )

    # 2. Insere o registro na tabela 'emprestimos' com a data e a hora gravadas na variável 'data_formatada'
    cursor.execute(
        """INSERT INTO emprestimos 
               (responsavel, data_saida, id_periferico, tel_responsavel, id_usuario, observacao, setor_dest, unid_dest, tipo_transfer) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            responsavel,
            data_formatada,
            id_periferico,
            tel_responsavel,
            session.get('usuario_id'),
            observacao,
            setor_dest,
            unid_dest,
            tipo_transfer,
        ),
    )

    conexao.commit()
    conexao.close()

    flash('Empréstimo registrado com sucesso!', 'success')
    return redirect('/verifica_emprestimos')