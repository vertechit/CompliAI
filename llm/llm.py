from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from operator import itemgetter
from controllers.ChatHistoryController import getChatMessasgeHistoryBySession, insertHistory
from vectors.vectorStore import getRetriever
from langchain_core.runnables import RunnablePassthrough

model = ChatOpenAI(model="gpt-3.5-turbo")

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
    insertHistory(sessionId=sessionId, mensagem=input, tipo=1)
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
        getChatMessasgeHistoryBySession,
        input_messages_key="question",
        history_messages_key="history",
    )
    ret = with_message_history.invoke({"question":input},config={"configurable": {"session_id": sessionId}})
    insertHistory(sessionId=sessionId, mensagem=ret, tipo=2)
    return ret

def chainRetriever(input: str)->str:
    template = """Responda a pergunta baseado somente no seguinte contexto:
{context}

Pergunta: {question}
"""
    prompt = ChatPromptTemplate.from_template(template)
    chain = (
        {"context": getRetriever(), "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    ret = chain.invoke(input)
    return ret

def chainRetrieverWithHistory(input: str, sessionId: int)-> str:
    insertHistory(sessionId=sessionId, mensagem=input, tipo=1)
    template =[
        (
            "system",
            """Responda a pergunta baseado somente no seguinte contexto
            {context}
            """
        ),
        MessagesPlaceholder(variable_name="history"),
        (
            "human",
            "{question}"
        )
    ]
    prompt = ChatPromptTemplate.from_messages(template)
    contextChain = itemgetter("question") | getRetriever() 
    first_step = RunnablePassthrough.assign(context=contextChain)
    chain = (
        first_step
        | prompt
        | model
        | StrOutputParser()
    )
    with_message_history = RunnableWithMessageHistory(
        chain,
        getChatMessasgeHistoryBySession,
        input_messages_key="question",
        history_messages_key="history",
    )
    ret = with_message_history.invoke(
        {"context": getRetriever(), "question":input},
        config={"configurable": {"session_id": sessionId}},
        )
    insertHistory(sessionId=sessionId, mensagem=ret, tipo=2)
    return ret