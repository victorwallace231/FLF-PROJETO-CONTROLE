from flask import Blueprint, request, redirect, session
from banco import conectar_banco
from datetime import date

# Definição do Blueprint para as rotas relacionadas ao processo de devolução
route_devolucao = Blueprint('devolucao', __name__)

# Rota HTTP POST responsável por registrar a devolução de um equipamento emprestado
@route_devolucao.route('/devolucao', methods=['POST'])
def devolucao():
    # Verificação de segurança: bloqueia o acesso caso o usuário não esteja logado
    if not session.get("usuario_email"):
        return redirect("/login")
    
    # Captura os IDs do empréstimo e do periférico enviados pelo formulário
    id_emprestimo = request.form["id_emprestimo"]
    id_periferico = request.form["id_periferico"]

    # Conecta à base de dados SQLite
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    # Obtém a data atual do sistema (AAAA-MM-DD) para registrar a data de devolução
    data_devolucao = date.today()

    # 1. Atualiza a tabela 'emprestimos': marca como devolvido (1) e salva a data de devolução
    cursor.execute(
        "UPDATE emprestimos SET devolvido = 1, data_devolucao = ? WHERE id_emprestimo = ?", 
        (data_devolucao, id_emprestimo)
    )

    # 2. Atualiza a tabela 'perifericos': torna o equipamento disponível novamente para novos empréstimos
    cursor.execute(
        "UPDATE perifericos SET disponivel = 1 WHERE id_periferico = ?", 
        (id_periferico,)
    )

    # Confirma as transações no banco de dados e encerra a conexão
    conexao.commit()
    conexao.close()

    # Redireciona para a tela de histórico de movimentações atualizada
    return redirect('/verifica_emprestimos')