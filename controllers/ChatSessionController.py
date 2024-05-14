#CompliAi - Issue 7
from models.ChatSession import ChatSession
from typing import List
from llm.llm import chainTitulo


def saveSessao(pergunta: str, session_id: int):
    session = None
    session = ChatSession.select().where(ChatSession.session_id == session_id)
    if session == None:
        titulo = chainTitulo(pergunta)
        session = ChatSession(session_id=session_id, titulo=titulo)
        session.save()
    else:
        pass

def deleteSessao(session_id: int)-> str:
    session = ChatSession.select().where(ChatSession.session_id == session_id).first()
    if session == None:
        return "Sessão não encontrada"
    else:
        ChatSession.delete().where(ChatSession.session_id == session_id).execute()
        return "Sessão deletada"

def listSessao(session_id: int = None)-> List[ChatSession]:
    sessions = None
    array = []
    if session_id == None:
        sessions = ChatSession.select()
    else:
        sessions = ChatSession.select().where(ChatSession.session_id == session_id)
    for session in sessions:
        newSession = (session.session_id, session.titulo, session.criado)
        array.append(newSession)
    return array

    