from flask import Blueprint, redirect,session,render_template,request
from banco import conectar_banco

route_devolucao = Blueprint('devolucao', __name__)

@route_devolucao.route('/devolucao', methods = ['GET', 'POST'])
def devolucao():
    #testa se o metodo é GET ou POST para carregar a página ou executar o codigo
    if request.method == 'GET':
        return render_template('devolucao.html')
    if request.method == 'POST':
        #Conexão com o banco e criação do objeto cursor
        conexao = conectar_banco()
        cursor = conexao.cursor()

        #Captura das informações digitada no front
        responsavel = request.form["responsavel"]
        telefone = request.form ["telefone"]

        #Busca no banco de Dados e armazenanmento dos dados
        cursor.execute("SELECT * FROM emprestimo WHERE telefone = ?", (telefone,))
        emprestimo=cursor.fetchall()
        conexao.close()

        #Testa se a busca no banco retornou algo, se não recarrega e mostra uma mensgem de erro, se sim um mensagem de sucesso
        if not emprestimo:
            return render_template('devolucao.html', erro="Não foi encontrado nenhum empréstimo no nome de ")
            
        else:
            return render_template('devolucao.html', sucesso="Emprestimos encontrados exibidos abaixo",respondavel=responsavel, emprestimo = emprestimo)

"""
Quando for criado a página html para o processo de devolção escrever o codigo a seguir no arquivo html
{% if erro %}
    <p>{{ erro }} {{ responsavel }}</p>
{% endif %}
{% if sucesso%}
    <p>{{ sucesso }}</p>
{% endif %}

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
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
obs:Local da mensagem decidido pelo front

"""
        