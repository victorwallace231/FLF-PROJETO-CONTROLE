from flask import Blueprint, redirect,session,render_template,request
from banco import conectar_banco

verifica_emprestimos = Blueprint('verifica_emprestimos', __name__)

@verifica_emprestimos.route('/verifica_emprestimos', methods = ['GET', 'POST'])
def verificar_emprestimos():
    if not session.get("usuario_email"):
            return redirect ('/login')
    #testa se o metodo é GET ou POST para carregar a página ou executar o codigo
    if request.method == 'GET':

        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute("""SELECT e.*, p.periferico, p.num_serie, p.id_periferico FROM emprestimos e 
        JOIN perifericos p ON e.id_periferico = p.id_periferico
        WHERE 1=1 ORDER BY e.id_emprestimo DESC""")

        movimentacoes = cursor.fetchall()
        conexao.close()

        return render_template ("movimentacao.html", movimentacoes = movimentacoes, name = session.get("usuario_name"))
    
    if request.method == 'POST':
        conexao = conectar_banco()
        cursor = conexao.cursor()

        status =  request.form["filtro_status"]
        categoria = request.form ["filtro_categoria"]
        responsavel = request.form["filtro_responsavel"].strip().lower()
        sql = """SELECT e.*, p.periferico, p.num_serie, p.id_periferico FROM emprestimos e 
        JOIN perifericos p ON e.id_periferico = p.id_periferico
        WHERE 1=1 """

        paramentros = []

        if categoria != "todos":
             sql +=  " AND LOWER(p.periferico) LIKE '%' || ? || '%'"
             paramentros.append (categoria)
        if status != "todos":
             status_tranlate = 1 if status == "devolvido" else 0
             sql += " AND e.devolvido = ?"
             paramentros.append (status_tranlate)
        if responsavel:
             sql+= " AND LOWER(e.responsavel) LIKE '%' || ? || '%'"
             paramentros.append(responsavel)

        sql += " ORDER BY e.id_emprestimo DESC"
        cursor.execute (sql,paramentros)
        movimentacoes = cursor.fetchall()
        conexao.close()
        return render_template ("movimentacao.html", movimentacoes = movimentacoes, name = session.get("usuario_name"))
        