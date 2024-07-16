from fastapi.testclient import TestClient
from api import server
from datetime import datetime
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

def test_cria_pasta():
    """
    Teste para criação de uma pasta
    O retorno deve ser um dict {'retorno': 'Pasta {descr} criada com sucesso!'}
    """
    response = client.post(
        "/createFolder",
        params={"path": "/", "descr": "main"},
        headers={"Authorization": f"Bearer {get_bearer_token()}"}
    )
    assert response.status_code == 200
    assert response.json() == {'retorno': 'Pasta main criada com sucesso!'}

def test_cria_pasta_ja_existente():
    """
    Teste para tentar criar uma pasta que já existe usando a mesma descrição
    O retorno deve ser um dict com o texto {'retorno': 'Erro: Já existe uma pasta com o mesmo nome no diretório informado!'}
    """
    response = client.post(
        '/createFolder',
        params={"path": "/", "descr": "main"},
        headers={"Authorization": f"Bearer {get_bearer_token()}"}
    )
    assert response.status_code == 200
    assert response.json() == {'retorno': 'Erro: Já existe uma pasta com o mesmo nome no diretório informado!'}

def test_lista_unica_pasta():
    """
    Teste para retornar o conteúdo de uma única pasta passando {folder_id} como parâmetro
    O retorno deve ser nulo pois a pasta está vazia
    """
    response = client.get(
        '/listFolder/1',
        headers={"Authorization": f"Bearer {get_bearer_token()}"}
    )
    assert response.status_code == 200
    assert response.json() == {'null'}

def test_lista_pastas():
    """
    Teste para retornar todas as pastas que não possuem um ar_folder_id
    O retorno deve ser um Array com vários JSONs com os campos do objeto de pastas
    """
    response = client.get("/listFolder",
        headers={"Authorization": f"Bearer {get_bearer_token()}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    resp_obj = response.json()[0]
    dict_keys = resp_obj.keys()
    assert isinstance(resp_obj['folder_id'], int)
    assert isinstance(resp_obj['path'], str)
    assert isinstance(resp_obj['descr'], str)
    assert isinstance(resp_obj['user_id'], int)
    assert isinstance(resp_obj['created'], datetime)
    assert isinstance(resp_obj['ar_folder_id'], int)

def test_renomeia_pasta():
    """
    Teste para renomear uma única pasta passando {folder_id} como parâmetro
    O retorno deve ser {"retorno": "Nome da pasta alterado de {descr} para {p_descr}"}
    """
    response = client.post(
        '/renameFolder/',
        params={"folder_id": "1", "descr": "main2"},
        headers={"Authorization": f"Bearer {get_bearer_token()}"}
    )
    assert response.status_code == 200
    assert response.json() == {'retorno': 'Nome da pasta alterado de main para main2'}

def test_deleta_pasta():
    """
    Teste para deletar uma pasta criada
    O retorno deve ser um json {"retorno": "Pasta {descr} deletada."}
    """
    token = get_bearer_token()
    response = client.delete(
        "/deleteFolder/1",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"retorno": "Pasta main2 deletada."}