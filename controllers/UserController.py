from models.User import User
import hashlib

def login(login: str, password: str)-> int:
    user = User.select().where((User.login==login.lower()) & (User.senha == hashlib.sha256(password.encode()).hexdigest())).first()
    return user

def create_user(login: str, password: str)-> int:
    criptoSenha = hashlib.sha256(password.encode()).hexdigest()
    user = User(login=login.lower(), senha=criptoSenha, tipo=0)
    user.save()
    return user