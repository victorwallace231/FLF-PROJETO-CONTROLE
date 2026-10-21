"""Zera o banco para produção.

Mantém: usuário id 1 (admin), categoria id 1 ("sem categoria") e os ícones.
Apaga: equipamentos, empréstimos, os demais usuários e as demais categorias.

Uso (na pasta do projeto, ao lado do banco.py):  python resetar_banco.py
"""
import os
import shutil
import sqlite3
from datetime import datetime
from getpass import getpass

from werkzeug.security import generate_password_hash

from banco import CAMINHO_BANCO

if not os.path.exists(CAMINHO_BANCO):
    raise SystemExit(f"Banco não encontrado: {CAMINHO_BANCO}")

print(f"Banco: {CAMINHO_BANCO}")
print("Isso APAGA todos os equipamentos, empréstimos e usuários (menos o admin id 1).")
if input('Digite RESETAR para continuar: ').strip() != "RESETAR":
    raise SystemExit("Cancelado. Nada foi alterado.")

# Backup antes de qualquer coisa
backup = CAMINHO_BANCO.replace(".db", f"_backup_{datetime.now():%Y%m%d-%H%M%S}.db")
shutil.copy2(CAMINHO_BANCO, backup)
print(f"Backup criado: {backup}")

nova_senha = getpass("Nova senha do admin (Enter para manter a atual): ").strip()

con = sqlite3.connect(CAMINHO_BANCO)
cur = con.cursor()

# Ordem importa: empréstimos dependem de equipamentos e usuários
cur.execute("DELETE FROM emprestimos")
cur.execute("DELETE FROM perifericos")
cur.execute("DELETE FROM usuario WHERE id_usuario != 1")
cur.execute("DELETE FROM categorias WHERE id_categoria != 1")

# Garante que o admin é admin
cur.execute("UPDATE usuario SET role = 'admin', admin = 1 WHERE id_usuario = 1")
if nova_senha:
    cur.execute("UPDATE usuario SET senha_user = ? WHERE id_usuario = 1",
                (generate_password_hash(nova_senha),))

# Faz os próximos ids recomeçarem do começo
cur.execute("DELETE FROM sqlite_sequence WHERE name IN ('emprestimos','perifericos')")
cur.execute("UPDATE sqlite_sequence SET seq = 1 WHERE name IN ('usuario','categorias')")
con.commit()

# VACUUM remove de vez os dados apagados do arquivo (senão ficam recuperáveis)
con.execute("VACUUM")

for t in ("usuario", "categorias", "icones", "perifericos", "emprestimos"):
    print(f"  {t}: {cur.execute(f'select count(*) from {t}').fetchone()[0]} linha(s)")
con.close()
print("Pronto. Banco zerado.")
