from functools import wraps
from flask import session, redirect, flash

def role_required(*roles):
    """"Só deixa passar aqueles que estiverem logados e com alguma papel definido."""
    def decorator(funcao):
        @wraps(funcao)
        def wrapper(*arg,**kwargs):
            if not session.get("usuario_email"):
                return redirect("/login")
            if session.get("usuario_role") not in roles:
                flash("Acesso negado: você não tem para isso.", "danger")
                return redirect("/dashboard")
            return funcao(*arg, **kwargs)
        return wrapper
    return decorator