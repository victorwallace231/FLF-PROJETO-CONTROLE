from flask import Blueprint, render_template, request, redirect, session
from banco import conectar_banco

route_updateuser = Blueprint('updateuser', __name__)

@route_updateuser.route('/updateuser', methods=['GET', 'POST'])
def update():
    if not session.get("usuario_email"):
           return redirect ('/login')
    if request.method == 'GET':
        return render_template('update.html')
    if request.method == 'POST':
        conexao = conectar_banco()
        cursor = conexao.cursor()

        email = request.form['email']
        nome = request.form['nome']
        telefone = request.form['telefone']

        cursor.execute("UPDATE usuario SET nome = ?, telefone = ?, email = ? WHERE email = ?", (nome, telefone, email, session.get('usuario_email')))
        conexao.commit()
        conexao.close()

        session['usuario_name'] = nome
        session['usuario_telefone'] = telefone
        session['usuario_email'] = email

        return redirect('/dashboard')