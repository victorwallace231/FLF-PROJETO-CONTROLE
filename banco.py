import sqlite3
def conectar_banco():
    conexao=sqlite.connect("Controle.db")
    return conexao
