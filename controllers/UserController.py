from models.User import User
import hashlib
import re

def validar_email(email)-> bool:
    regexMail = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
    if re.match(regexMail, email):
        return True
    else:
        raise ValueError("O login precisa ser um email válido")

def login(login: str, password: str)-> int:
    retorno = None
    user = User.select().where((User.login==login.lower()) & (User.senha == hashlib.sha256(password.encode()).hexdigest())).first()
    if user:
        retorno = user.user_id
    return retorno

def create_user(login: str, password: str)-> int:
    retorno = None
    validar_email(login)
    criptoSenha = hashlib.sha256(password.encode()).hexdigest()
    user = User(login=login.lower(), senha=criptoSenha, tipo=0)
    user.save()
    if user:
        retorno = user.user_id
    return retorno