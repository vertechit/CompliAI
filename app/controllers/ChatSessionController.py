#CompliAi - Issue 7
from models.ChatHistory import ChatSession
from typing import List
from llm import llm
from peewee import fn

def create_sessao(pergunta: str = None) -> int:
    session = None
    if pergunta != None:
        titulo = llm.chain_titulo(pergunta)
        session = ChatSession(titulo=titulo)
        session.save()
        return session.session_id
    else:
        session = ChatSession()
        session.save()
        return session.session_id

def save_sessao(pergunta: str, session_id: int):
    session = None
    session = ChatSession.select().where(ChatSession.session_id == session_id)
    if session == None:
        titulo = llm.chain_titulo(pergunta)
        session = ChatSession(session_id=session_id, titulo=titulo)
        session.save()
    else:
        pass

def delete_sessao(session_id: int)-> str:
    session = ChatSession.select().where(ChatSession.session_id == session_id).first()
    if session == None:
        return "Sessão não encontrada"
    else:
        ChatSession.delete().where(ChatSession.session_id == session_id).execute()
        return "Sessão deletada"

def list_sessao(session_id: int = None)-> List[ChatSession]:
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

    