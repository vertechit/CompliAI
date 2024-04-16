from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from typing import Union
from fastapi import Body, FastAPI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from operator import itemgetter

model = ChatOpenAI(model="gpt-3.5-turbo")
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def chainPiada(input: str) -> str:
    prompt = ChatPromptTemplate.from_template("Me conte uma piada sobre {assunto}")
    output_parser = StrOutputParser()
    
    chain = (prompt | model | output_parser)
    return chain.invoke({"assunto":input})

def chain(input: str) -> str:
    prompt = ChatPromptTemplate.from_template("{assunto}")
    output_parser = StrOutputParser()
    chain = (prompt | model | output_parser)
    return chain.invoke({"assunto":input})


def chainWithHistory(input: str, sessionId: int) -> str:
    template =[
        (
            "system",
            "Responda a pergunta de forma resumida"
        ),
        MessagesPlaceholder(variable_name="history"),
        (
            "human",
            "{question}"
        )
        ]
    prompt = ChatPromptTemplate.from_messages(template)
    chain = ( 
            prompt
            | model
            | StrOutputParser()
    )

    with_message_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="history",
    )
    print(store)
    return with_message_history.invoke({"question":input},
                                       config={"configurable": {"session_id": sessionId}},
    )

app = FastAPI()

@app.post("/piada")
def retornaMensagem(mensagem=Body()):
    print(mensagem)
    return {"retorno": chainPiada(mensagem)}

@app.post("/chain")
def retornaMensagem(mensagem=Body()):
    return {"retorno": chain(mensagem)}

@app.post("/chainHistory/{sessionId}")
def retornaMensagem(sessionId: int, mensagem=Body()):
    return {"retorno": chainWithHistory(mensagem, sessionId)}