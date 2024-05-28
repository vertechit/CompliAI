try:
    import sys
    import os
    
    sys.path.append(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '..'
            )
        )
    )

except:
    raise

import pytest
from fastapi.testclient import TestClient
from api import server
from utils.utils import destroyDatabases, initDatabases
import os
import logging
from dotenv import load_dotenv

LOGGER = logging.getLogger(__name__)
client = TestClient(server.app)

@pytest.fixture
def test_start_database():
    load_dotenv()
    if 'POSTGRES_HOST' in os.environ:
        del os.environ["POSTGRES_HOST"]
    if 'VECTORDB' in os.environ:
        del os.environ["VECTORDB"]
    os.environ["RECREATE_DB"] = "1"
    destroyDatabases()
    initDatabases()

def test_delete_usuario_inexistente():
    """
    Deleta um usuário
    """
    response = client.post(
        "/deleteUsers",
        json={"username":"teste@teste.com"}
    )
    assert response.status_code == 200
    assert response.json() == {'usuario_id': 0}
    
def test_cria_usuario():
    """
    Cria um usuário
    """
    response = client.post(
        "/createUsers",
        json={"username":"teste@teste.com", "password":"teste"}
    )
    assert response.status_code == 200
    assert response.json() == {'login': 'teste@teste.com', 'tipo': 0, 'user_id': 1}
    
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
    
def test_delete_usuario_existente():
    """
    Deleta um usuário
    """
    response = client.post(
        "/deleteUsers",
        json={"username":"teste@teste.com"}
    )
    assert response.status_code == 200
    assert response.json() == {'usuario_id': 1}