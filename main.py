from fastapi import Body, FastAPI, UploadFile
from pydantic import BaseModel, Field
from genie.genie import main
from llm.llm import chain, chainWithHistory, chainPiada, chainRetriever, chainRetrieverWithHistory, chainRetrieverWithHistoryTitle
from controllers.DocumentsController import saveDocument, deleteDocumento, listDocumentos
from controllers.ChatSessionController import deleteSessao
from typing import List
import tempfile
import os

from models import ChatHistory, Documentos, ChatSession
from vectors import vectorStore

tags_metadata = [
    {"name": "LLMs", "description": "Chamadas para as LLMs"},
    {"name": "Documentos", "description": "Cadastros de documentos"},
]
app = FastAPI(openapi_tags=tags_metadata)

class InputChat(BaseModel):
    SystemMessage: str | None = Field(default=None, examples=["Responde de forma educada"])
    HumamMessage: str = Field(examples=["Quem é o presidente do Brasil?"])
    
class ResponseChat(BaseModel):
    AiMessage: str = Field(examples=["Presidente do brasil é o Lula"])

class ChunkObj(BaseModel):
    chunks_id: int
    id_vector: str
    md5: str
        
class DocumentoObj(BaseModel):
    documento_id: int
    titulo: str
    descricao: str
    md5: str
    chunks: List[ChunkObj]

#CompliAi - Issue 7
class SessaoObj(BaseModel):
    session_id: int
    titulo: str
    criado: str

def destroyDatabases():
    vectorStore.dropCollection()
    if ChatHistory.ChatHistory.table_exists():
        ChatHistory.ChatHistory.drop_table()
    if Documentos.Documentos.table_exists():
        Documentos.Documentos.drop_table()
    if Documentos.Chunks.table_exists():
        Documentos.Chunks.drop_table()
    if ChatSession.ChatSession.table_exists():
        ChatSession.ChatSession.drop_table()

def initDatabases():
    vectorStore.createCollection()
    if not ChatHistory.ChatHistory.table_exists():
        ChatHistory.ChatHistory.create_table()
    if not Documentos.Documentos.table_exists():
        Documentos.Documentos.create_table()
    if not Documentos.Chunks.table_exists():
        Documentos.Chunks.create_table()

if os.getenv("RECREATE_DB", 0) == 1:
    destroyDatabases()
initDatabases()

@app.post("/piada", tags=["LLMs"])
def retornaMensagem(mensagem=Body()):
    return {"retorno": chainPiada(mensagem)}

@app.post("/chain", tags=["LLMs"])
def retornaMensagem(chat: InputChat)-> ResponseChat:
    ret = chain(chat.HumamMessage)
    response = ResponseChat(AiMessage=ret)
    return response

@app.post("/chainHistory/{sessionId}", tags=["LLMs"])
def retornaMensagem(sessionId: int, chat: InputChat)-> ResponseChat:
    ret = chainWithHistory(chat.HumamMessage, sessionId)
    response = ResponseChat(AiMessage=ret)
    return response

@app.post("/chainRetriever", tags=["LLMs"])
def retornaMensagem(sessionId: int, chat: InputChat)-> ResponseChat:
    ret = chainRetriever(chat.HumamMessage)
    response = ResponseChat(AiMessage=ret)
    return response

@app.post("/chainRetrieverHistory/{sessionId}", tags=["LLMs"])
def retornaMensagem(sessionId: int, chat: InputChat)-> ResponseChat:
    ret = chainRetrieverWithHistory(chat.HumamMessage, sessionId)
    response = ResponseChat(AiMessage=ret)
    return response

#CompliAi - Issue 7
@app.post("/chainRetrieverHistoryTitle/{sessionId}", tags=["LLMs"])
def retornaMensagem(sessionId: int, chat: InputChat)-> ResponseChat:
    ret = chainRetrieverWithHistoryTitle(chat.HumamMessage, sessionId)
    response = ResponseChat(AiMessage=ret)
    return response

@app.get("/listDocument", tags=["Documentos"])
def listaDocumento()-> List[DocumentoObj] | None:
    ret: List[DocumentoObj] = []
    documentos = listDocumentos(None)
    if len(documentos) == 0:
        return None
    for doc in documentos:
        chunk = [ChunkObj(chunks_id=chunkLoop[0], id_vector=chunkLoop[1], md5=chunkLoop[2]) for chunkLoop in doc[4]]
        ret.append(DocumentoObj(documento_id=doc[0], titulo=doc[1], descricao=doc[2], md5=doc[3], chunks=chunk))
    return ret

@app.get("/listDocument/{documento_id}", tags=["Documentos"])
def listaDocumento(documento_id: int = None)-> DocumentoObj | None:
    ret: DocumentoObj = None
    documentos = listDocumentos(documento_id)
    if len(documentos) == 0:
        return None
    for doc in documentos:
        chunk = [ChunkObj(chunks_id=chunkLoop[0], id_vector=chunkLoop[1], md5=chunkLoop[2]) for chunkLoop in doc[4]]
        ret = DocumentoObj(documento_id=doc[0], titulo=doc[1], descricao=doc[2], md5=doc[3], chunks=chunk)
    return ret

#CompliAi - Issue 7
@app.get("/listSession/{session_id}", tags=["ChatSession"])
def listaSessao(session_id: int = None)-> SessaoObj | None:
    ret: SessaoObj = None
    sessoes = listaSessao(session_id)
    if len(sessoes) == 0:
        return None
    for sessao in sessoes:
        ret = SessaoObj(session_id=sessao[0], titulo=sessao[1], criado=sessao[2])
    return ret

@app.post("/createDocument/", tags=["Documentos"])
async def uploadFile(file: UploadFile | None, filename: str, description: str):
    contents = await file.read()
    arquivoTemp = tempfile.gettempdir()+"/"+file.filename
    print(tempfile.gettempdir())
    with open(arquivoTemp, "wb") as f:
        f.write(contents)
    documento = saveDocument(arquivoTemp, filename, description)
    return {"retorno": documento}

@app.delete("/deleteDocument/{documento_id}", tags=["Documentos"])
def deletaDocumento(documento_id: int):
    deleteDocumento(documento_id)
    return {"retorno": "Deletado"}

#CompliAi - Issue 7
@app.delete("/deleteSession/{session_id}", tags=["ChatSession"])
def deletaSessao(session_id: int):
    deleteSessao(session_id)
    return {"retorno": "Sessão Deletada"}

if __name__ == "__main__":
    main()