import re
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, session, flash
from banco import conectar_banco

create_emprestimo = Blueprint('create_emprestimo', __name__)

@create_emprestimo.route('/create_emprestimo', methods=['GET', 'POST'])
def create():
    if not session.get("usuario_email"):
        return redirect('/login')

    conexao = conectar_banco()
    cursor = conexao.cursor()

    # 1. PROCESSAMENTO DA CRIAÇÃO DE NOVA MOVIMENTAÇÃO (SUBMISSÃO DO MODAL)
    if request.method == 'POST' and 'id_periferico' in request.form:
        agora = datetime.now()
        data_formatada = agora.strftime('%d/%m/%Y %H:%M:%S')

        responsavel = request.form['responsavel']
        id_periferico = request.form['id_periferico']
        tel_responsavel = re.sub(r"\D", "", request.form['tel_responsavel'])
        observacao = request.form['observacao']
        setor_dest = request.form.get("setor_dest", "").upper().strip()
        unid_dest = request.form.get("unid_dest", "").upper().strip()
        tipo_transfer = request.form.get("tipo_transfer", "").strip()
        filtro_transfer = tipo_transfer.strip().lower()
        responsavel_destino = request.form.get("responsavel_destino", "").strip()
        tel_responsavel_destino = re.sub(r"\D", "", request.form.get("tel_responsavel_destino", ""))

        cursor.execute("UPDATE perifericos SET disponivel = 0 WHERE id_periferico = ?", (id_periferico,))

        match filtro_transfer:
            case 'transferencia de unidade' | 'transferência de localização':
                cursor.execute("""
                    UPDATE perifericos 
                    SET unid_atual = ?, setor_atual = ?, disponivel = 0, manutencao = 0, inativo = 0, transferido = 1
                    WHERE id_periferico = ?
                """, (unid_dest, setor_dest, id_periferico))

            case 'remessa para concerto':
                cursor.execute("""
                    UPDATE perifericos 
                    SET unid_atual = ?, setor_atual = ?, disponivel = 0, manutencao = 1, inativo = 0, transferido = 0
                    WHERE id_periferico = ?
                """, (unid_dest, setor_dest, id_periferico))

            case 'retorno de concerto':
                cursor.execute("""
                    UPDATE perifericos 
                    SET unid_atual = ?, setor_atual = ?, disponivel = 1, manutencao = 0, inativo = 0, transferido = 0
                    WHERE id_periferico = ?
                """, (unid_dest, setor_dest, id_periferico))

            case 'baixa por defeito' | 'baixa por fora de uso/obsoleto':
                cursor.execute("""
                    UPDATE perifericos 
                    SET unid_atual = ?, setor_atual = ?, disponivel = 0, manutencao = 0, inativo = 1, transferido = 0
                    WHERE id_periferico = ?
                """, (unid_dest, setor_dest, id_periferico))

            case 'empréstimo' | 'evento':
                cursor.execute("""
                    UPDATE perifericos 
                    SET unid_atual = ?, setor_atual = ?, disponivel = 0, manutencao = 0, inativo = 0, transferido = 0
                    WHERE id_periferico = ?
                """, (unid_dest, setor_dest, id_periferico))

            case 'retorno de empréstimo':
                cursor.execute("""
                    UPDATE perifericos 
                    SET unid_atual = ?, setor_atual = ?, disponivel = 1, manutencao = 0, inativo = 0, transferido = 0
                    WHERE id_periferico = ?
                """, (unid_dest, setor_dest, id_periferico))

            case _:
                cursor.execute("""
                    UPDATE perifericos 
                    SET unid_atual = ?, setor_atual = ?, disponivel = 1, manutencao = 0, inativo = 0, transferido = 0
                    WHERE id_periferico = ?
                """, (unid_dest, setor_dest, id_periferico))

        cursor.execute("""
            INSERT INTO emprestimos 
            (resp_origem, data_saida, id_periferico, tel_resp_origem, id_usuario, observacao, setor_dest, unid_dest, tipo_transfer, resp_dest, tel_resp_dest) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            responsavel, data_formatada, id_periferico, tel_responsavel,
            session.get('usuario_id'), observacao, setor_dest, unid_dest,
            tipo_transfer, responsavel_destino, tel_responsavel_destino
        ))

        conexao.commit()
        conexao.close()

        flash("Empréstimo registrado com sucesso!", "success")
        return redirect('/verifica_emprestimos')

    # 2. LISTAGEM E FILTRAGEM DOS PERIFÉRICOS PARA MOVIMENTAÇÃO
    cursor.execute("SELECT * FROM categorias WHERE excluido != 1")
    categorias = cursor.fetchall()

    pesquisa = request.form.get("filtro_pesquisa", "").strip().lower() if request.method == 'POST' else ""
    categoria = request.form.get("filtro_categoria", "todos").strip() if request.method == 'POST' else "todos"
    disponibilidade = request.form.get("filtro_disponibilidade", "todos").strip() if request.method == 'POST' else "todos"

    # COALESCE garante a exclusão estrita de equipamentos inativos (1 ou '1') em qualquer situação
    sql = """
        SELECT p.id_periferico, p.categoria, p.marca, p.num_serie, p.disponivel, p.manutencao, p.inativo, c.categoria, p.icone, p.unid_origem, p.setor_origem, p.unid_atual, p.setor_atual, p.transferido
        FROM perifericos p 
        JOIN categorias c ON p.categoria = c.id_categoria 
        WHERE COALESCE(p.inativo, 0) NOT IN (1, '1')
    """
    parametros = []

    if categoria != "todos":
        sql += " AND p.categoria = ?"
        parametros.append(categoria)

    if disponibilidade != "todos":
        if disponibilidade == "disponivel":
            sql += " AND (p.disponivel = 1 OR p.disponivel = '1') AND COALESCE(p.manutencao, 0) NOT IN (1, '1')"
        elif disponibilidade in ["emprestado", "emuso"]:
            sql += " AND COALESCE(p.disponivel, 0) NOT IN (1, '1') AND COALESCE(p.manutencao, 0) NOT IN (1, '1')"
        elif disponibilidade == "manutencao":
            sql += " AND (p.manutencao = 1 OR p.manutencao = '1')"
        elif disponibilidade == "transferido":
            sql += " AND (p.transferido = 1 OR p.transferido = '1')"

    if pesquisa:
        sql += " AND (LOWER(p.num_serie) LIKE '%' || ? || '%' OR LOWER(p.marca) LIKE '%' || ? || '%' OR LOWER(c.categoria) LIKE '%' || ? || '%')"
        parametros.extend([pesquisa, pesquisa, pesquisa])

    sql += " ORDER BY p.id_periferico DESC"

    cursor.execute(sql, parametros)
    perifericos = cursor.fetchall()
    conexao.close()

    return render_template(
        'createmov.html',
        perifericos=perifericos,
        categorias=categorias,
        categoria=categoria,
        pesquisa=pesquisa,
        disponibilidade=disponibilidade,
        name=session.get("usuario_name")
    )