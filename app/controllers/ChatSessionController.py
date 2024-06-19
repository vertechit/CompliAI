#CompliAi - Issue 7
from models.ChatHistory import ChatSession, ChatHistory
from typing import List
from llm import llm
from peewee import fn

def create_sessao(pergunta: str, user_id: int) -> int:
    session = None
    if pergunta != None:
        titulo = llm.chain_titulo(pergunta)
        session = ChatSession(titulo=titulo, user_id=user_id)
        session.save()
        return session.session_id
    else:
        session = ChatSession(user_id=user_id)
        session.save()
        return session.session_id

def save_sessao(pergunta: str, session_id: int, user_id: int):
    session = None
    session = ChatSession.select().where((ChatSession.session_id == session_id) & (ChatSession.user_id == user_id))
    if session == None:
        titulo = llm.chain_titulo(pergunta)
        session = ChatSession(session_id=session_id, titulo=titulo)
        session.save()
    else:
        pass

def delete_sessao(session_id: int, user_id: int)-> str:
    session = ChatSession.select().where((ChatSession.session_id == session_id) & (ChatSession.user_id == user_id)).first()
    if session == None:
        return "Sessão não encontrada"
    else:
        ChatHistory.delete().where(ChatHistory.session_id == session_id).execute()
        ChatSession.delete().where(ChatSession.session_id == session_id).execute()
        return "Sessão deletada"

def list_sessao(session_id: int, user_id: int)-> List[ChatSession]:
    sessions = None
    array = []
    if session_id == 0:
        sessions = ChatSession.select().where(ChatSession.user_id == user_id)
    else:
        sessions = ChatSession.select().where((ChatSession.session_id == session_id) & (ChatSession.user_id == user_id))
    for session in sessions:
        newSession = (session.session_id, session.titulo, session.criado, session.user_id)
        array.append(newSession)
    return array

    