from models.User import User
import hashlib
import re

def validar_email(email)-> bool:
    regexMail = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
    if re.match(regexMail, email):
        return True
    else:
        raise ValueError("O login precisa ser um email válido")

def login(login: str, password: str)-> dict:
    retorno = {}
    user = User.select().where((User.login==login.lower()) & (User.senha == hashlib.sha256(password.encode()).hexdigest())).first()
    if user:
        retorno = {
            "user_id": user.user_id,
            "login": user.login,
            "tipo": user.tipo
        }
    return retorno

def create_user(login: str, password: str)-> int:
    retorno = {}
    validar_email(login)
    criptoSenha = hashlib.sha256(password.encode()).hexdigest()
    user = User(login=login.lower(), senha=criptoSenha, tipo=0)
    user.save()
    if user:
        retorno = {
            "user_id": user.user_id,
            "login": user.login,
            "tipo": user.tipo
        }
    return retorno

def delete_user(username: str)-> int:
    user = User.delete().where(User.login==username.lower()).execute()
    return user