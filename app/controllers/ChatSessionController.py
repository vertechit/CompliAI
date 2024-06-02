from models.ChatHistory import ChatSession
from typing import List
from llm import llm

def save_sessao(pergunta: str, session_id: int):
    session = ChatSession.select().where(ChatSession.session_id == session_id).first()
    if session is None:
        titulo = llm.chain_titulo(pergunta)
        session = ChatSession(session_id=session_id, titulo=titulo)
        session.save()
    else:
        pass

def delete_sessao(session_id: int) -> str:
    session = ChatSession.select().where(ChatSession.session_id == session_id).first()
    if session is None:
        return "Sessão não encontrada"
    else:
        ChatSession.delete().where(ChatSession.session_id == session_id).execute()
        return "Sessão deletada"

def list_sessao(session_id: int = None) -> List[ChatSession]:
    array = []
    if session_id is None:
        sessions = ChatSession.select()
    else:
        sessions = ChatSession.select().where(ChatSession.session_id == session_id)
    
    for session in sessions:
        new_session = (session.session_id, session.titulo, session.criado)
        array.append(new_session)
    
    return array
