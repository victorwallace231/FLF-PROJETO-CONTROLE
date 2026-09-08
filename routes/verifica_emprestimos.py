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

        cursor.execute("""SELECT e.*, p.periferico FROM emprestimos e 
        JOIN perifericos p ON e.id_periferico = p.id_periferico
        WHERE 1=1 """)

        movimentacoes = cursor.fetchall()
        conexao.close()

        return render_template ("movimentacao.html", movimentacoes = movimentacoes, name = session.get("usuario_name"))
    
    if request.method == 'POST':
        conexao = conectar_banco()
        cursor = conexao.cursor()

        status =  request.form["filtro_status"]
        categoria = request.form ["filtro_categoria"]
        sql = """SELECT e.*, p.periferico FROM emprestimos e 
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

        cursor.execute (sql,paramentros)
        movimentacoes = cursor.fetchall()
        conexao.close()
        return render_template ("movimentacao.html", movimentacoes = movimentacoes, name = session.get("usuario_name"))


        

        

        

"""
Quando for criado a página html para o processo de devolção escrever o codigo a seguir no arquivo html
{% if erro %}
    <p>{{ erro }} {{ responsavel }}</p>
{% endif %}
{% if sucesso%}
    <p>{{ sucesso }}</p>
        <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Responsavel</th>
                        <th>Data de retirada</th>
                        <th>ID_PERIFERICO</th>
                        <th>Telefone</th>
                        <th>Observação</th>
                    </tr>
                </thead>
                <tbody>
                    {% for emprestimo in emprestimos %}
                    <tr>
                        <td><p>{{ emprestimo[0] }}</p></td>
                        <td><p>{{ emprestimo[1] }}</p></td>
                        <td><p>{{ emprestimo[2] }}</p></td>
                        <td><p>{{ emprestimo[4] }}</p></td>
                        <td><p>{{ emprestimo[5] }}</p></td>
                        <td><p>{{ emprestimo[7] }}</p></td>
                        <td><form action="/devolucao" method="POST">
                            <!-- Campo oculto mandando o ID deste empréstimo específico -->
                            <input type="hidden" name="id_emprestimo" value="{{ emprestimo[0] }}">
                            <button type="submit" class="btn-devolver">Devolver</button>
                        </form>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
        </table>
{% endif %}


obs:Local da mensagem decidido pelo front

"""
        