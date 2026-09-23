import re
from flask import Blueprint, render_template, request, redirect, session, flash
from banco import conectar_banco
from datetime import date

# Definição do Blueprint para as rotas de criação e registro de novos empréstimos
create_emprestimo = Blueprint('create_emprestimo', __name__)

@create_emprestimo.route('/create_emprestimo', methods=['GET', 'POST'])
def create():
    # Verificação de segurança: bloqueia o acesso se o usuário não estiver logado
    if not session.get("usuario_email"):
        return redirect('/login')

    # Requisição GET: Carrega o formulário de cadastro de movimentação
    if request.method == 'GET':
        conexao = conectar_banco()
        cursor = conexao.cursor()

        # Busca apenas os equipamentos que estão atualmente disponíveis (disponivel = 1)
        # para preencher a caixa de seleção (select) no formulário
        # Colunas explícitas: [0]id [1]categoria [2]marca [3]nº série [4]disponível [5]manutenção [6]inativo [7]nome da categoria [8]ícone
        cursor.execute("""SELECT p.id_periferico, p.categoria, p.marca, p.num_serie, p.disponivel, p.manutencao, p.inativo, c.categoria, p.icone
        FROM perifericos p JOIN categorias c ON p.categoria = c.id_categoria WHERE p.disponivel = 1""")
        perifericos = cursor.fetchall()
        conexao.close()

        # Renderiza a página passando a lista de itens disponíveis e o nome do usuário na sessão
        return render_template("createmov.html", perifericos=perifericos, name=session.get("usuario_name"))

    # Requisição POST: Processa a criação do novo empréstimo no sistema
    if request.method == 'POST':
        conexao = conectar_banco()
        cursor = conexao.cursor()

        # Registra automaticamente a data atual do sistema como data de saída
        data_saida = date.today()
        data_formatada = data_saida.strftime('%d/%m/%Y')

        # Captura as informações digitadas no formulário
        responsavel = request.form["responsavel"]
        id_periferico = request.form["id_periferico"]
        # Remove qualquer caractere que não seja dígito antes de gravar no banco
        tel_responsavel = re.sub(r"\D", "", request.form["tel_responsavel"])
        observacao = request.form["observacao"]

        # 1. Atualiza a tabela 'perifericos': altera o status do equipamento para indisponível (disponivel = 0)
        cursor.execute(
            "UPDATE perifericos SET disponivel = 0 WHERE id_periferico = ?", 
            (id_periferico,)
        )

        # 2. Insere o registro na tabela 'emprestimos', vinculando ao ID do usuário autenticado na sessão
        cursor.execute(
            """INSERT INTO emprestimos 
               (responsavel, data_saida, id_periferico, tel_responsavel, id_usuario, observacao) 
               VALUES (?, ?, ?, ?, ?, ?)""", 
            (responsavel, data_formatada, id_periferico, tel_responsavel, session.get("usuario_id"), observacao)
        )

        # Efetiva a gravação da transação no banco de dados e fecha a conexão
        conexao.commit()
        conexao.close()

        flash("Empréstimo registrado com sucesso!", "success")
        # Redireciona o usuário de volta para a lista geral de movimentações
        return redirect("/verifica_emprestimos")