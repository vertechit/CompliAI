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

def test_cria_documento_file():
    """
    Teste para criação de um documento passando um arquivo
    O retorno deve ser uma dict com o texto {'retorno': 'Documento criado 1'}
    """
    response = client.post(
        "/createDocument",
        params={"description":"teste"},
        files={"file": ("gympass.pdf", open('app/test/gympass.pdf', "rb"), "application/pdf")},
        headers={"Authorization": f"Bearer {get_bearer_token()}"}
    )
    assert response.status_code == 200
    assert response.json() == {'retorno': 'Documento criado 1'}
    
def test_deleta_documento_file():
    """
    Teste para deletar um documento criado
    O retorno deve ser um json {"retorno": "Deletado"}
    """
    token = get_bearer_token()
    response = client.delete(
        "/deleteDocument/1",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"retorno": "Deletado"}
    
def test_cria_documento_url():
    """
    Teste para criação de um documento passando a URL de alguma página.
    O retorno deve ser uma dict com o texto {'retorno': 'Documento criado 1'}
    """
    response = client.post(
        "/createDocumentUrl",
        json={"titulo":"teste", "description":"teste","url":"https://docs.compliancecapitalhumano.com.br/docs/cor/000_rhgeral"},
        headers={"Authorization": f"Bearer {get_bearer_token()}"}
    )
    assert response.status_code == 200
    assert response.json() == {'retorno': 'Documento criado 1'}
    
def test_cria_documento_ja_existente():
    """
    Teste para tentar criar um documento que já existe usando a URL de uma página
    O retorno deve ser uma dict com o texto {'retorno': 'Documento já existe 1'}
    """
    response = client.post(
        "/createDocumentUrl",
        json={"titulo":"teste", "description":"teste","url":"https://docs.compliancecapitalhumano.com.br/docs/cor/000_rhgeral"},
        headers={"Authorization": f"Bearer {get_bearer_token()}"}
    )
    assert response.status_code == 200
    assert response.json() == {'retorno': 'Documento já existe 1'}
    
def test_lista_unico_documento():
    """
    Teste para retornar um único documento passando {id} como parâmetro
    O retorno de deve ser um JSON com os campos do objeto de documentos
    """
    response = client.get("/listDocument/1",
        headers={"Authorization": f"Bearer {get_bearer_token()}"})
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    resp_obj = response.json()
    dict_keys = resp_obj.keys()
    assert isinstance(resp_obj['documento_id'], int)
    assert isinstance(resp_obj['titulo'], str)
    assert isinstance(resp_obj['descricao'], str)
    assert isinstance(resp_obj['md5'], str)
    assert isinstance(resp_obj['url'], str)
    assert isinstance(resp_obj['chunks'], list)
    
def test_lista_documentos():
    """
    Teste para retorna todos os documentos cadastrados
    O retorno de deve ser um Array com vários JSONs com os campos do objeto de documentos
    """
    response = client.get("/listDocument",
        headers={"Authorization": f"Bearer {get_bearer_token()}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    resp_obj = response.json()[0]
    dict_keys = resp_obj.keys()
    assert isinstance(resp_obj['documento_id'], int)
    assert isinstance(resp_obj['titulo'], str)
    assert isinstance(resp_obj['descricao'], str)
    assert isinstance(resp_obj['md5'], str)
    assert isinstance(resp_obj['url'], str)
    assert isinstance(resp_obj['chunks'], list)
    
def test_deleta_documento_url():
    """
    Teste para deletar um documento criado
    O retorno deve ser um json {"retorno": "Deletado"}
    """
    response = client.delete("/deleteDocument/1",
        headers={"Authorization": f"Bearer {get_bearer_token()}"}
        )
    assert response.status_code == 200
    assert response.json() == {"retorno": "Deletado"}
    