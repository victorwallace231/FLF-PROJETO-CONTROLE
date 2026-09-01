from flask import Blueprint, session, render_template, request, redirect
from banco import  conectar_banco

route_emprestimo = Blueprint('emprestimo', __name__)

@route_emprestimo.route('/emprestimo', methods = ['GET', 'POST'])
def emprestimo():
    if not session.get("usuario_email"):
           return redirect ('/login')
    #Testa se o metodo é GET ou POST para carregar a página ou executar o codigo
    if request.method == 'GET':
        return render_template('emprestimo.html')
    if request.method == 'POST':
        #Conexão com o banco e criação do objeto cursor
        conexao = conectar_banco()
        cursor = conexao.cursor()

        #Captura das informações digitada no front
        responsavel = request.form ["responsavel"]
        data_saida = request.form ["saida"]
        telefone_responsavel = request.form ["telefone"]
        observacao = request.form ["observacao"]

        #Insere no banco de dados os valores digitados do pelo o usuário
        cursor.execute("INSERT INTO emprestimo (responsavel,data_saida,telefone,observacao) VALUES (?,?,?,?)", (responsavel,data_saida,telefone_responsavel,observacao))

        #Salva as informações executadas pelo cursor e fecha a conexão com banco
        conexao.commit()
        conexao.close()

        # Recarrega a página para um novo empréstimo se necessário
        return redirect('/emprestimo')
