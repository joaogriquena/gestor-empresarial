from flask import session, redirect, url_for, flash
from functools import wraps

def verificar_permissao(area_restrita):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            tipo_usuario = session.get('tipo')
            if tipo_usuario == 'admin' or tipo_usuario == area_restrita:
                return f(*args, **kwargs)
            flash('Acesso não permitido para esta área.')
            return redirect(url_for('login.selecao_area'))
        return decorated_function
    return decorator
