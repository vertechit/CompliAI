from fastapi.testclient import TestClient
from api import server
import logging

LOGGER = logging.getLogger(__name__)
client = TestClient(server.app)

def get_bearer_token(user: str | None = None, password: str | None = None):
    response = client.post(
        "/token",
        data={"username": user if user != None else "admin", "password": password if password != None else "admin"}
    )
    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert 'token_type' in response.json()
    return response.json()["access_token"]

def test_delete_usuario_inexistente():
    """
    Tenta deletar um usuário inexistente
    """
    response = client.post(
        "/deleteUsers",
        json={"username":"teste@teste.com"},
        headers={"Authorization": f"Bearer {get_bearer_token()}"}
    )
    assert response.status_code == 200
    assert response.json() == {'usuario_id': 0}
    
def test_cria_usuario():
    """
    Cria um usuário
    """
    token = get_bearer_token()
    response = client.post(
        "/createUsers",
        json={"username":"teste@teste.com", "password":"teste"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == {'login': 'teste@teste.com', 'tipo': 0, 'user_id': 2}
    
def test_login_com_sucesso():
    """
    Teste para realizar o login de um usuário criado
    """
    response = client.post(
        "/token",
        data={"username":"teste@teste.com", "password":"teste"}
    )
    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert 'token_type' in response.json()
    
def test_login_com_erro():
    """
    Teste para realizar o login de um usuário criado
    """
    response = client.post(
        "/login",
        data={"username":"teste@teste.com", "password":"senhaerrada"}
    )
    assert response.status_code == 404
    
def test_cria_usuario_sem_ser_admin():
    """
    Tenta criar um usuário sem ser um usuário ADMIN
    """
    token = get_bearer_token("teste@teste.com", "teste")
    response = client.post(
        "/createUsers",
        json={"username":"teste2@teste.com", "password":"teste2"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401
    
def test_deleta_usuario_sem_ser_admin():
    """
    Tenta deletar um usuário sem ser um usuário ADMIN
    """
    token = get_bearer_token("teste@teste.com", "teste")
    response = client.post(
        "/deleteUsers",
        json={"username":"teste@teste.com"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401
    
def test_delete_usuario_existente():
    """
    Deleta um usuário
    """
    token = get_bearer_token()
    response = client.post(
        "/deleteUsers",
        json={"username":"teste@teste.com"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == {'usuario_id': 1}