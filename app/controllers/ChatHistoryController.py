from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from models.ChatHistory import ChatHistory, ChatSession
from typing import List

def insert_history(sessionId: int, mensagem: str, tipo: int):
    hist = ChatHistory(session_id=sessionId, mensagem=mensagem, tipo=tipo)
    hist.save()

def get_chat_history_by_session(session_id: int, user_id: int)->List[tuple]:
    ret = []
    for message in ChatHistory.select().join(ChatSession).where((ChatHistory.session_id==session_id) & (ChatSession.user_id==user_id)).order_by(ChatHistory.chathistory_id.desc()):
        ret.append((message.chathistory_id, message.session_id.session_id, message.mensagem, message.tipo, message.criado))
    if len(ret) > 0:
        return ret
    else:
        return None

def get_chat_messasge_history_by_session(session_id: int, user_id: int)->BaseChatMessageHistory:
    ret = []
    for message in ChatHistory.select().join(ChatSession).where((ChatHistory.session_id==session_id) & (ChatSession.user_id==user_id)).order_by(ChatHistory.chathistory_id.desc()):
        if(message.tipo==0):
            ret.append(SystemMessage(content=message.mensagem))
        elif(message.tipo==1):
            ret.append(HumanMessage(content=message.mensagem))
        else:
            ret.append(AIMessage(content=message.mensagem))
    if len(ret) > 0:
        return ChatMessageHistory(messages=ret)
    else:
        return None
