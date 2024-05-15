from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from models.ChatHistory import ChatHistory

def insertHistory(sessionId: int, mensagem: str, tipo: int):
    hist = ChatHistory(session_id=sessionId, mensagem=mensagem, tipo=tipo)
    hist.save()

def getChatMessasgeHistoryBySession(sessionId: int)->BaseChatMessageHistory:
    ret = []
    for message in ChatHistory.select().where(ChatHistory.session_id==sessionId).order_by(ChatHistory.chathistory_id.asc()):
        if(message.tipo==0):
            ret.append(SystemMessage(content=message.mensagem))
        elif(message.tipo==1):
            ret.append(HumanMessage(content=message.mensagem))
        else:
            ret.append(AIMessage(content=message.mensagem))
    return ChatMessageHistory(messages=ret)
