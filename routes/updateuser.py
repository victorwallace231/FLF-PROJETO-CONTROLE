from flask import Blueprint, render_template, request, redirect, session
from banco import conectar_banco

# Definição do Blueprint para o módulo de atualização de cadastro de usuário
route_updateuser = Blueprint('updateuser', __name__)

# Rota que atende tanto o carregamento do formulário (GET) quanto o envio dos dados (POST)
@route_updateuser.route('/updateuser', methods=['GET', 'POST'])
def update():
    # Verificação de segurança: redireciona para a tela de login se não houver usuário ativo na sessão
    if not session.get("usuario_email"):
        return redirect('/login')

    # Requisição GET: apenas renderiza a página do formulário de edição de perfil
    if request.method == 'GET':
        return render_template('update.html')

    # Requisição POST: processa a atualização dos dados no banco e na sessão
    if request.method == 'POST':
        conexao = conectar_banco()
        cursor = conexao.cursor()

        # Captura os novos valores digitados pelo usuário no formulário
        email = request.form['email']
        nome = request.form['nome']
        telefone = request.form['telefone']

        # Executa a atualização no SQLite usando o e-mail atual armazenado na sessão como chave de busca
        # Nota: Ajustado de 'user_email' para 'email_user' para corresponder ao nome real da coluna no banco
        cursor.execute(
            "UPDATE usuario SET name_user = ?, email_user = ?, tel_user = ? WHERE email_user = ?", 
            (nome, email, telefone, session.get('usuario_email'))
        )
        
        # Confirma as alterações na base de dados e fecha a conexão
        conexao.commit()
        conexao.close()

        # Atualiza os dados gravados na sessão com as novas informações para manter a aplicação sincronizada
        session['usuario_name'] = nome
        session['usuario_telefone'] = telefone
        session['usuario_email'] = email

        # Redireciona o usuário de volta para o painel principal após salvar
        return redirect('/dashboard')