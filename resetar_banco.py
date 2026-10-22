"""Zera o banco para produção.

Mantém: usuário id 1 (admin), categoria id 1 ("sem categoria") e os ícones.
Apaga: equipamentos, empréstimos, unidades, setores, os demais usuários e as demais categorias.
(Unidades e setores voltam vazios: admin/gestor cadastram pela tela "Unidades e Setores".)

Uso (na pasta do projeto, ao lado do banco.py):
    python resetar_banco.py             -> zera o banco e define a senha do admin
    python resetar_banco.py --so-senha  -> NÃO apaga nada, só troca a senha do admin
"""
import os
import shutil
import sqlite3
import sys
from datetime import datetime

from werkzeug.security import generate_password_hash

from banco import CAMINHO_BANCO, iniciar_banco

def pedir_senha():
    """Pede a senha VISÍVEL (é um script local, de uso único) e exige confirmação."""
    while True:
        s = input("Nova senha do admin (aparece enquanto digita, mín. 6 caracteres): ").strip()
        if len(s) < 6:
            print("  Muito curta, tente de novo.")
            continue
        if input("Digite a senha de novo para confirmar: ").strip() != s:
            print("  As senhas não batem, tente de novo.")
            continue
        return s


def trocar_senha(senha):
    con = sqlite3.connect(CAMINHO_BANCO)
    con.execute("UPDATE usuario SET senha_user = ? WHERE id_usuario = 1",
                (generate_password_hash(senha),))
    con.commit()
    email = con.execute("SELECT email_user FROM usuario WHERE id_usuario = 1").fetchone()[0]
    con.close()
    print(f"Senha do admin trocada. Login: {email}")


if not os.path.exists(CAMINHO_BANCO):
    raise SystemExit(f"Banco não encontrado: {CAMINHO_BANCO}")

print(f"Banco: {CAMINHO_BANCO}")

if "--so-senha" in sys.argv:
    trocar_senha(pedir_senha())
    raise SystemExit
print("Isso APAGA equipamentos, empréstimos, unidades, setores e usuários (menos o admin id 1).")
if input('Digite RESETAR para continuar: ').strip() != "RESETAR":
    raise SystemExit("Cancelado. Nada foi alterado.")

# Backup antes de qualquer coisa
backup = CAMINHO_BANCO.replace(".db", f"_backup_{datetime.now():%Y%m%d-%H%M%S}.db")
shutil.copy2(CAMINHO_BANCO, backup)
print(f"Backup criado: {backup}")

# Garante que o banco já está no formato novo (tabelas unidades/setores) antes de limpar
iniciar_banco()

nova_senha = pedir_senha()

con = sqlite3.connect(CAMINHO_BANCO)
cur = con.cursor()

# Ordem importa: empréstimos dependem de equipamentos e usuários
cur.execute("DELETE FROM emprestimos")
cur.execute("DELETE FROM perifericos")
cur.execute("DELETE FROM setores")      # setores antes das unidades (cada setor aponta para uma unidade)
cur.execute("DELETE FROM unidades")
cur.execute("DELETE FROM usuario WHERE id_usuario != 1")
cur.execute("DELETE FROM categorias WHERE id_categoria != 1")

# Garante que o admin é admin
cur.execute("UPDATE usuario SET role = 'admin', admin = 1 WHERE id_usuario = 1")
cur.execute("UPDATE usuario SET senha_user = ? WHERE id_usuario = 1",
            (generate_password_hash(nova_senha),))

# Faz os próximos ids recomeçarem do começo
cur.execute("DELETE FROM sqlite_sequence WHERE name IN ('emprestimos','perifericos','setores','unidades')")
cur.execute("UPDATE sqlite_sequence SET seq = 1 WHERE name IN ('usuario','categorias')")
con.commit()

# VACUUM remove de vez os dados apagados do arquivo (senão ficam recuperáveis)
con.execute("VACUUM")

for t in ("usuario", "categorias", "icones", "unidades", "setores", "perifericos", "emprestimos"):
    print(f"  {t}: {cur.execute(f'select count(*) from {t}').fetchone()[0]} linha(s)")
con.close()
print("Pronto. Banco zerado.")
