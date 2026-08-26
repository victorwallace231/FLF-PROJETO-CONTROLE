import sqlite3
def conectar_banco():
    conexao= sqlite3.connect("Controle.db")
    return conexao
