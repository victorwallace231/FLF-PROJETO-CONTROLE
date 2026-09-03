from flask import Blueprint, redirect,session,render_template,request
from banco import conectar_banco

verifica_emprestimos = Blueprint('verifica_emprestimos', __name__)

@verifica_emprestimos.route('/verifica_emprestimos', methods = ['GET', 'POST'])
def verificar_emprestimos():
    if not session.get("usuario_email"):
            return redirect ('/login')
    #testa se o metodo é GET ou POST para carregar a página ou executar o codigo
    if request.method == 'GET':
        return render_template('verifica_emprestimo.html')
    if request.method == 'POST':
        conexao = conectar_banco()
        cursor = conexao.cursor()

        responsavel = request.form ["responsavel"]
        telefone = request.form["telefone"]

        cursor.execute("SELECT * FROM emprestimos WHERE tel_responsavel = ? AND devolvido = false", (telefone,))
        emprestimos = cursor.fetchall()
        conexao.close()

        if not emprestimos :
             return render_template ("verifica_emprestimo.html",responsavel = responsavel, erro = "Não foi possivel encontrar emprestimos nesse nome")
        else:
             return render_template ("verifica_emprestimo.html",responsavel = responsavel,emprestimos = emprestimos, sucesso = True)

        

        

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
        