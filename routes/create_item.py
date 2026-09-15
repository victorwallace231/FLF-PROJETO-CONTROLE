from flask import Blueprint, render_template, request, redirect, session
from banco import conectar_banco

# Definição do Blueprint para as rotas de criação/cadastro de novos equipamentos
route_create_item = Blueprint('create_item', __name__)

@route_create_item.route('/create_item', methods=['GET', 'POST'])
def create():
    # Verificação de segurança: redireciona para o login caso o usuário não esteja autenticado
    if not session.get("usuario_email"):
        return redirect('/login')

    # Requisição GET: apenas exibe a página do formulário de cadastro de equipamentos
    if request.method == 'GET':
        return render_template("createitem.html")

    # Requisição POST: processa o envio das informações para salvar o novo registro no banco
    if request.method == 'POST':
        conexao = conectar_banco()
        cursor = conexao.cursor()

        # Captura e higieniza os campos enviados pelo formulário (remove espaços extras e coloca em minúsculas)
        periferico = request.form["categoria"].strip().lower()
        marca = request.form["marca"].strip().lower()
        num_serie = request.form["num_serie"].strip().lower()

        # Insere o novo equipamento no banco de dados
        # Todo item novo é cadastrado automaticamente com: disponivel = 1, manutencao = 0 e inativo = 0
        cursor.execute(
            "INSERT INTO perifericos (periferico, marca, num_serie, disponivel, manutencao, inativo) VALUES (?, ?, ?, 1, 0, 0)", 
            (periferico, marca, num_serie)
        )

        # Efetiva a gravação no SQLite e fecha a conexão
        conexao.commit()
        conexao.close()

        # Recarrega a página de cadastro vazia para permitir o cadastro sequencial de múltiplos itens
        return redirect('/create_item')