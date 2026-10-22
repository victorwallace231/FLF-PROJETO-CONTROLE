import sqlite3
from flask import Blueprint, render_template, request, redirect, session, flash
from banco import conectar_banco
from auth import role_required

# Unidades e setores: só admin e gestor mexem. Cada setor pertence a UMA unidade,
# então unidades diferentes podem ter setores com o mesmo nome (ex.: "Administração").
#
# Exclusão LÓGICA (igual à das categorias): o registro continua no banco com excluido = 1,
# some das listas e não pode ser escolhido de novo. Os equipamentos que tinham essa origem
# continuam apontando para ela, então nada do histórico se perde.
route_localizacoes = Blueprint('localizacoes', __name__)

PAGINA = '/unidades_setores'


def _texto(campo):
    """Texto do formulário sem espaços sobrando (inclusive os repetidos no meio)."""
    return " ".join(request.form.get(campo, "").split())


@route_localizacoes.route(PAGINA, methods=['GET'])
@role_required("admin", "gestor")
def listar():
    conexao = conectar_banco()
    unidades = conexao.execute(
        """SELECT u.id_unidade, u.nome_unidade,
                  (SELECT COUNT(*) FROM setores s
                    WHERE s.id_unidade = u.id_unidade AND s.excluido = 0) AS total_setores,
                  (SELECT COUNT(*) FROM perifericos p
                    WHERE p.id_unidade_atual = u.id_unidade AND p.inativo = 0) AS total_equipamentos
           FROM unidades u WHERE u.excluido = 0
           ORDER BY u.nome_unidade COLLATE NOCASE"""
    ).fetchall()
    setores = conexao.execute(
        """SELECT s.id_setor, s.nome_setor, s.id_unidade, u.nome_unidade,
                  (SELECT COUNT(*) FROM perifericos p
                    WHERE p.id_setor_atual = s.id_setor AND p.inativo = 0) AS total_equipamentos
           FROM setores s JOIN unidades u ON u.id_unidade = s.id_unidade
           WHERE s.excluido = 0 AND u.excluido = 0
           ORDER BY u.nome_unidade COLLATE NOCASE, s.nome_setor COLLATE NOCASE"""
    ).fetchall()
    conexao.close()
    return render_template('unidades_setores.html', unidades=unidades, setores=setores,
                           name=session.get("usuario_name"))


# ------------------------------------------------------------------ unidades
@route_localizacoes.route('/create_unidade', methods=['POST'])
@role_required("admin", "gestor")
def create_unidade():
    nome = _texto('nome_unidade')
    if not nome:
        flash("Digite o nome da unidade.", "danger")
        return redirect(PAGINA)

    conexao = conectar_banco()
    try:
        existente = conexao.execute(
            "SELECT id_unidade, nome_unidade, excluido FROM unidades WHERE nome_unidade = ?", (nome,)
        ).fetchone()

        if existente and not existente["excluido"]:
            flash("Já existe uma unidade com esse nome.", "danger")
        elif existente:
            # Já existiu e foi excluída: volta com o MESMO id (os equipamentos continuam ligados a ela)
            conexao.execute("UPDATE unidades SET excluido = 0, nome_unidade = ? WHERE id_unidade = ?",
                            (nome, existente["id_unidade"]))
            conexao.commit()
            flash("Unidade reativada: ela já existia e tinha sido excluída. Os setores dela continuam "
                  "excluídos; adicione-os de novo para reativá-los.", "success")
        else:
            conexao.execute("INSERT INTO unidades (nome_unidade) VALUES (?)", (nome,))
            conexao.commit()
            flash("Unidade criada com sucesso!", "success")
    except sqlite3.IntegrityError:
        conexao.rollback()
        flash("Já existe uma unidade com esse nome.", "danger")
    finally:
        conexao.close()
    return redirect(PAGINA)


@route_localizacoes.route('/update_unidade', methods=['POST'])
@role_required("admin", "gestor")
def update_unidade():
    id_unidade = request.form.get('id_unidade', '')
    nome = _texto('nome_unidade')
    if not nome:
        flash("Digite o novo nome da unidade.", "danger")
        return redirect(PAGINA)

    conexao = conectar_banco()
    try:
        antiga = conexao.execute(
            "SELECT nome_unidade FROM unidades WHERE id_unidade = ? AND excluido = 0", (id_unidade,)
        ).fetchone()
        if not antiga:
            flash("Unidade não encontrada.", "danger")
            return redirect(PAGINA)

        conflito = conexao.execute(
            "SELECT excluido FROM unidades WHERE nome_unidade = ? AND id_unidade != ?", (nome, id_unidade)
        ).fetchone()
        if conflito:
            flash("Existe uma unidade excluída com esse nome. Escolha outro nome ou adicione uma unidade "
                  "com esse nome para reativá-la." if conflito["excluido"]
                  else "Já existe uma unidade com esse nome.", "danger")
            return redirect(PAGINA)

        conexao.execute("UPDATE unidades SET nome_unidade = ? WHERE id_unidade = ?", (nome, id_unidade))
        # Os equipamentos apontam para o ID da unidade; o nome atualizado aparece via JOIN.
        # O histórico de movimentações continua guardando o nome da época.
        conexao.commit()
        flash("Unidade renomeada com sucesso!", "success")
    except sqlite3.IntegrityError:
        conexao.rollback()
        flash("Já existe uma unidade com esse nome.", "danger")
    finally:
        conexao.close()
    return redirect(PAGINA)


@route_localizacoes.route('/delete_unidade', methods=['POST'])
@role_required("admin", "gestor")
def delete_unidade():
    id_unidade = request.form.get('id_unidade', '')

    conexao = conectar_banco()
    try:
        if not conexao.execute(
            "SELECT 1 FROM unidades WHERE id_unidade = ? AND excluido = 0", (id_unidade,)
        ).fetchone():
            flash("Unidade não encontrada.", "danger")
            return redirect(PAGINA)

        # Os setores de uma unidade excluída também saem das listas
        setores = conexao.execute(
            "UPDATE setores SET excluido = 1 WHERE id_unidade = ? AND excluido = 0", (id_unidade,)
        ).rowcount
        conexao.execute("UPDATE unidades SET excluido = 1 WHERE id_unidade = ?", (id_unidade,))
        equipamentos = conexao.execute(
            "SELECT COUNT(*) FROM perifericos WHERE id_unidade_origem = ? AND inativo = 0", (id_unidade,)
        ).fetchone()[0]
        conexao.commit()
        flash(f"Unidade excluída. {setores} setor(es) dela também foram excluídos. "
              f"{equipamentos} equipamento(s) continuam cadastrados com essa origem.", "success")
    finally:
        conexao.close()
    return redirect(PAGINA)


# ------------------------------------------------------------------- setores
@route_localizacoes.route('/create_setor', methods=['POST'])
@role_required("admin", "gestor")
def create_setor():
    id_unidade = request.form.get('id_unidade', '')
    nome = _texto('nome_setor')
    if not nome or not id_unidade:
        flash("Escolha a unidade e digite o nome do setor.", "danger")
        return redirect(PAGINA)

    conexao = conectar_banco()
    try:
        unidade = conexao.execute(
            "SELECT nome_unidade FROM unidades WHERE id_unidade = ? AND excluido = 0", (id_unidade,)
        ).fetchone()
        if not unidade:
            flash("Unidade não encontrada.", "danger")
            return redirect(PAGINA)

        existente = conexao.execute(
            "SELECT id_setor, nome_setor, excluido FROM setores WHERE id_unidade = ? AND nome_setor = ?",
            (id_unidade, nome),
        ).fetchone()

        if existente and not existente["excluido"]:
            flash("Essa unidade já tem um setor com esse nome.", "danger")
        elif existente:
            # Já existiu nesta unidade e foi excluído: volta com o MESMO id
            conexao.execute("UPDATE setores SET excluido = 0, nome_setor = ? WHERE id_setor = ?",
                            (nome, existente["id_setor"]))
            conexao.commit()
            flash("Setor reativado: ele já existia nesta unidade e tinha sido excluído.", "success")
        else:
            conexao.execute("INSERT INTO setores (nome_setor, id_unidade) VALUES (?, ?)", (nome, id_unidade))
            conexao.commit()
            flash("Setor criado com sucesso!", "success")
    except sqlite3.IntegrityError:
        conexao.rollback()
        flash("Essa unidade já tem um setor com esse nome.", "danger")
    finally:
        conexao.close()
    return redirect(PAGINA)


@route_localizacoes.route('/update_setor', methods=['POST'])
@role_required("admin", "gestor")
def update_setor():
    id_setor = request.form.get('id_setor', '')
    nome = _texto('nome_setor')
    novo_id_unidade = request.form.get('id_unidade', '').strip()   # em branco = continua na mesma unidade
    if not nome:
        flash("Digite o novo nome do setor.", "danger")
        return redirect(PAGINA)

    conexao = conectar_banco()
    try:
        antigo = conexao.execute(
            """SELECT s.nome_setor, s.id_unidade, u.nome_unidade
               FROM setores s JOIN unidades u ON u.id_unidade = s.id_unidade
               WHERE s.id_setor = ? AND s.excluido = 0""", (id_setor,)
        ).fetchone()
        if not antigo:
            flash("Setor não encontrado.", "danger")
            return redirect(PAGINA)

        # Unidade de destino (a mesma, se o formulário não mandou outra)
        if novo_id_unidade and novo_id_unidade != str(antigo["id_unidade"]):
            destino = conexao.execute(
                "SELECT id_unidade, nome_unidade FROM unidades WHERE id_unidade = ? AND excluido = 0",
                (novo_id_unidade,),
            ).fetchone()
            if not destino:
                flash("Unidade não encontrada.", "danger")
                return redirect(PAGINA)
        else:
            destino = {"id_unidade": antigo["id_unidade"], "nome_unidade": antigo["nome_unidade"]}
        mudou_unidade = destino["id_unidade"] != antigo["id_unidade"]

        conflito = conexao.execute(
            "SELECT excluido FROM setores WHERE id_unidade = ? AND nome_setor = ? AND id_setor != ?",
            (destino["id_unidade"], nome, id_setor),
        ).fetchone()
        if conflito:
            flash("Existe um setor excluído com esse nome na unidade escolhida. Escolha outro nome ou "
                  "adicione um setor com esse nome para reativá-lo." if conflito["excluido"]
                  else "A unidade escolhida já tem um setor com esse nome.", "danger")
            return redirect(PAGINA)

        conexao.execute(
            "UPDATE setores SET nome_setor = ?, id_unidade = ? WHERE id_setor = ?",
            (nome, destino["id_unidade"], id_setor),
        )
        acompanharam = 0
        atuais_atualizados = 0
        if mudou_unidade:
            # A origem do equipamento é o setor: quem era deste setor passa para a nova unidade.
            acompanharam = conexao.execute(
                "UPDATE perifericos SET id_unidade_origem = ? WHERE id_setor_origem = ?",
                (destino["id_unidade"], id_setor),
            ).rowcount
            # Equipamentos atualmente neste setor acompanham a unidade nova pelo ID.
            atuais_atualizados = conexao.execute(
                "UPDATE perifericos SET id_unidade_atual = ? WHERE id_setor_atual = ?",
                (destino["id_unidade"], id_setor),
            ).rowcount
        conexao.commit()

        if mudou_unidade:
            flash(f"Setor movido para a unidade {destino['nome_unidade']}. "
                  f"{acompanharam} equipamento(s) de origem e {atuais_atualizados} equipamento(s) "
                  "na localização atual acompanharam a mudança.", "success")
        else:
            flash("Setor renomeado com sucesso!", "success")
    except sqlite3.IntegrityError:
        conexao.rollback()
        flash("A unidade escolhida já tem um setor com esse nome.", "danger")
    finally:
        conexao.close()
    return redirect(PAGINA)


@route_localizacoes.route('/delete_setor', methods=['POST'])
@role_required("admin", "gestor")
def delete_setor():
    id_setor = request.form.get('id_setor', '')

    conexao = conectar_banco()
    try:
        if not conexao.execute(
            "SELECT 1 FROM setores WHERE id_setor = ? AND excluido = 0", (id_setor,)
        ).fetchone():
            flash("Setor não encontrado.", "danger")
            return redirect(PAGINA)

        conexao.execute("UPDATE setores SET excluido = 1 WHERE id_setor = ?", (id_setor,))
        equipamentos = conexao.execute(
            "SELECT COUNT(*) FROM perifericos WHERE id_setor_origem = ? AND inativo = 0", (id_setor,)
        ).fetchone()[0]
        conexao.commit()
        flash(f"Setor excluído. {equipamentos} equipamento(s) continuam cadastrados com essa origem.", "success")
    finally:
        conexao.close()
    return redirect(PAGINA)
