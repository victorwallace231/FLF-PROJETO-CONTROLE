from flask import Blueprint, render_template, request, redirect
from banco import conectar_banco
from werkzeug.security import generate_password_hash, check_password_hash

route_login = Blueprint ('Login', __name__)
@route_login.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='GET':
        return render_template('login.html')
    
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM usuario WHERE email = ?", (email,))
    usuario = cursor.fetchone()
    conexao.close()

    if usuario and check_password_hash(usuario[2], password):
        return redirect('/dashboard')
    else:
        return render_template('login.html', error='Email ou senha incorretos')