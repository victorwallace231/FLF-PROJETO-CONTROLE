from flask import Blueprint, render_template, request, redirect, session, flash
from banco import conectar_banco, listar_icones, icone_valido, resolver_localizacao, ICONE_PADRAO
from auth import role_required

# Definição do Blueprint para as rotas de criação/cadastro de novos equipamentos
route_create_item = Blueprint('create_item', __name__)

@route_create_item.route('/create_item', methods=['GET', 'POST'])
@role_required("admin", "gestor")
def create():
    # Verificação de segurança: redireciona para o login caso o usuário não esteja autenticado
    if not session.get("usuario_email"):
        return redirect('/login')

    # Requisição GET: exibe o formulário de cadastro (categorias + ícones disponíveis)
    if request.method == 'GET':
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM categorias WHERE excluido !=1")
        categorias = cursor.fetchall()
        conexao.close()
        return render_template("createitem.html", categorias=categorias, icones=listar_icones(), icone_padrao=ICONE_PADRAO)

    # Requisição POST: processa o envio das informações para salvar o novo registro no banco
    id_categoria = request.form.get("categoria", "").strip().lower()
    marca = request.form.get("marca", "").strip().lower()
    num_serie = request.form.get("num_serie", "").strip().lower()
    icone = request.form.get("icone", "").strip()
    # Unidade e setor chegam como ID (vêm de <select>); os nomes são buscados no banco
    id_unidade_origem = request.form.get("unidade_origem", "").strip()
    id_setor_origem = request.form.get("setor_origem", "").strip()


    # Segunda barreira de validação (a primeira é feita no navegador, em validacao.js)
    if not (id_categoria and marca and num_serie and id_unidade_origem and id_setor_origem):
        flash("Todos os itens precisam ser preenchidos para cadastrar o equipamento.", "danger")
        return redirect('/create_item')

    conexao = conectar_banco()
    cursor = conexao.cursor()

    # O setor precisa existir E pertencer à unidade escolhida
    local = resolver_localizacao(cursor, id_unidade_origem, id_setor_origem)
    if not local or not local[0]:
        conexao.close()
        flash("Unidade ou setor inválido. Escolha um setor que pertença à unidade selecionada.", "danger")
        return redirect('/create_item')
    nome_unidade, nome_setor = local

    # Todo item novo é cadastrado automaticamente com: disponivel = 1, manutencao = 0 e inativo = 0
    cursor.execute(
        "INSERT INTO perifericos (categoria, marca, num_serie, disponivel, manutencao, inativo, icone, id_unidade_origem, id_setor_origem, unid_atual, setor_atual, transferido) VALUES (?, ?, ?, 1, 0, 0, ?, ?, ?, ?, ?, 0)",
        (id_categoria, marca, num_serie, icone_valido(icone), id_unidade_origem, id_setor_origem, nome_unidade, nome_setor)
    )
    conexao.commit()
    conexao.close()

    flash("Equipamento cadastrado com sucesso!", "success")
    # Recarrega a página de cadastro vazia para permitir o cadastro sequencial de múltiplos itens
    return redirect('/create_item')
