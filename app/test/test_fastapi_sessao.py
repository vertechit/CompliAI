from fastapi.testclient import TestClient
from api import server
import logging

LOGGER = logging.getLogger(__name__)
client = TestClient(server.app)

def get_bearer_token():
    response = client.post(
        "/token",
        data={"username": "admin", "password": "admin"}
    )
    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert 'token_type' in response.json()
    return response.json()["access_token"]

def test_cria_sessao_sem_titulo():
    """
    Teste para criação sessão dos chats
    O retorno deve ser ResponseChat em branco
    """
    response = client.post(
        "/createSession",
        headers={"Authorization": f"Bearer {get_bearer_token()}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json()['criado'], str)
    assert response.json()['session_id'] == 1
    assert response.json()['titulo'] == None
    assert response.json()['user_id'] == 1
    
def test_lista_sessoes_sem_titulo():
    """
    Teste listar todas as sessões de um usuário
    O retorno deve ser uma lista de sessoes com o texto {'retorno': 'Sessão criada - 1'}
    """
    response = client.get(
        "/listSession",
        headers={"Authorization": f"Bearer {get_bearer_token()}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json()[0]['criado'], str)
    assert response.json()[0]['session_id'] == 1
    assert response.json()[0]['titulo'] == None
    assert response.json()[0]['user_id'] == 1
    
def test_lista_sessao_unica_sem_titulo():
    """
    Teste listar uma unica sessao
    O retorno deve ser uma lista de sessoes com o texto {'retorno': 'Sessão criada - 1'}
    """
    response = client.get(
        "/listSession/1",
        headers={"Authorization": f"Bearer {get_bearer_token()}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json()['criado'], str)
    assert response.json()['session_id'] == 1
    assert response.json()['titulo'] == None
    assert response.json()['user_id'] == 1
    
def test_deleta_sessa_sem_titulo():
    """
    Teste para deletar uma sessao
    O retorno deve ser uma lista de sessoes com o texto {'retorno': 'Sessão criada - 1'}
    """
    response = client.delete(
        "/deleteSession/1",
        headers={"Authorization": f"Bearer {get_bearer_token()}"}
    )
    assert response.status_code == 200
    assert response.json() == {'retorno': 'Sessão deletada'}


def test_cria_sessao_com_titulo():
    """
    Teste para criação sessão dos chats
    O retorno deve ser uma dict com o texto {'retorno': 'Sessão criada - 1'}
    """
    response = client.post(
        "/createSession",
        json={"Pergunta":"Quem é o presidente do brasil?"},
        headers={"Authorization": f"Bearer {get_bearer_token()}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json()['criado'], str)
    assert response.json()['session_id'] == 1
    assert isinstance(response.json()['titulo'], str)
    assert response.json()['user_id'] == 1
    
def test_lista_sessoes_com_titulo():
    """
    Teste listar todas as sessões de um usuário
    O retorno deve ser uma lista de sessoes com o texto {'retorno': 'Sessão criada - 1'}
    """
    response = client.get(
        "/listSession",
        headers={"Authorization": f"Bearer {get_bearer_token()}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json()[0]['criado'], str)
    assert response.json()[0]['session_id'] == 1
    assert isinstance(response.json()[0]['titulo'], str)
    assert response.json()[0]['user_id'] == 1
    
def test_lista_sessao_unica_com_titulo():
    """
    Teste listar uma unica sessao
    O retorno deve ser uma lista de sessoes com o texto {'retorno': 'Sessão criada - 1'}
    """
    response = client.get(
        "/listSession/1",
        headers={"Authorization": f"Bearer {get_bearer_token()}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json()['criado'], str)
    assert response.json()['session_id'] == 1
    assert isinstance(response.json()['titulo'], str)
    assert response.json()['user_id'] == 1
    
def test_lista_historico_com_titulo():
    """
    Teste listar o histórico das interacoes da sessao
    O retorno deve ser uma lista de sessoes com o texto {'retorno': 'Sessão criada - 1'}
    """
    response = client.get(
        "/listHistory/1",
        headers={"Authorization": f"Bearer {get_bearer_token()}"}
    )
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]['chathistory_id'] == 2
    assert isinstance(response.json()[0]['criado'], str)
    assert isinstance(response.json()[0]['mensagem'], str)
    assert response.json()[0]['session_id'] == 1
    assert response.json()[0]['tipo'] == 2
    
def test_deleta_sessa_com_titulo():
    """
    Teste para deletar uma sessao
    O retorno deve ser uma lista de sessoes com o texto {'retorno': 'Sessão criada - 1'}
    """
    response = client.delete(
        "/deleteSession/1",
        headers={"Authorization": f"Bearer {get_bearer_token()}"}
    )
    assert response.status_code == 200
    assert response.json() == {'retorno': 'Sessão deletada'}