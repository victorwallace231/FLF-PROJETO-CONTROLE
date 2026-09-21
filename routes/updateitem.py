from flask import Blueprint, render_template, request, redirect, session
from banco import conectar_banco

# Definição do Blueprint para as rotas de atualização de equipamentos
route_updateitem = Blueprint('update_item', __name__)

@route_updateitem.route('/update_item', methods=['POST'])
def update():
    # Verificação de autenticação: se o usuário não estiver logado, redireciona para a tela de login
    if not session.get("usuario_email"):
        return redirect('/login')

    if request.method == 'POST':
        conexao = conectar_banco()
        cursor = conexao.cursor()

        # Início da instrução SQL. O 'SET id_periferico = id_periferico' serve como um "coringa neutro"
        # para permitir que as próximas cláusulas sejam adicionadas com vírgula (Ex: ", marca = ?")
        sql = """UPDATE perifericos SET id_periferico = id_periferico"""

        # Captura os dados enviados no formulário de edição
        item_id = request.form.get('id_periferico')
        item_nome = request.form.get("categoria")
        item_marca = request.form.get('marca')
        item_numero_de_serie = request.form.get('num_serie')
        status = request.form.get('filtro_status')

        paramentros = []

        # Se o campo categoria foi preenchido, adiciona na consulta
        if item_nome:
             sql += ", categoria = ?"
             paramentros.append(item_nome)

        # Se a marca foi preenchida, adiciona na consulta
        if item_marca:
             sql += ", marca = ?"
             paramentros.append(item_marca)

        # Se o número de série foi preenchido, adiciona na consulta
        if item_numero_de_serie:
            sql += ", num_serie = ?"
            paramentros.append(item_numero_de_serie)

        # Mapeamento do status selecionado no formulário para ajustar as 3 colunas de controle do banco
        if status and status != "todos":
            if status == "disponivel":
                sql += ", disponivel = 1, inativo = 0, manutencao = 0"
            elif status == "emuso":
                sql += ", disponivel = 0, inativo = 0, manutencao = 0"
            elif status == "manutencao":
                sql += ", disponivel = 0, manutencao = 1, inativo = 0"
            elif status == "inativo":
                sql += ", disponivel = 0, manutencao = 0, inativo = 1"

        # Adiciona a condição WHERE para aplicar as mudanças apenas ao item específico
        sql += " WHERE id_periferico = ?"
        paramentros.append(item_id)

        # Executa a busca parametrizada evitando SQL Injection
        cursor.execute(sql, paramentros)

        # Confirma as alterações e fecha a conexão com a base de dados
        conexao.commit()
        conexao.close()

        # Redireciona de volta para a tela de gerenciamento de inventário
        return redirect('/equipamentos')