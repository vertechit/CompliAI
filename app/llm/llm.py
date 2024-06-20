from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from operator import itemgetter
from controllers.ChatHistoryController import get_chat_messasge_history_by_session, insert_history
from controllers.ChatSessionController import save_sessao
from vectors.vectorStore import getRetriever
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.runnables.utils import ConfigurableFieldSpec

model = ChatOpenAI(model="gpt-3.5-turbo")

PROMPT_RESP_BASEADO_CONTEXTO = "Responda a pergunta baseado somente no seguinte contexto\n{context}"
QUESTION_MARK = "{question}"

__template_history_question_and_context =[
    (
        "system",
        PROMPT_RESP_BASEADO_CONTEXTO
    ),
    MessagesPlaceholder(variable_name="history"),
    (
        "human",
        QUESTION_MARK
    )
]

_template_context =[
    (
        "system",
        PROMPT_RESP_BASEADO_CONTEXTO
    ),
    (
        "human",
        QUESTION_MARK
    )
]

_template_history_question =[
    (
        "system",
        "Responda a pergunta de forma resumida"
    ),
    MessagesPlaceholder(variable_name="history"),
    (
        "human",
        QUESTION_MARK
    )
]

_output_parser = StrOutputParser()

def chain_piada(input: str) -> str:
    prompt = ChatPromptTemplate.from_template("Me conte uma piada sobre {assunto}")
    chain = (prompt | model | _output_parser)
    return chain.invoke({"assunto":input})

def chain_titulo(input: str) -> str:
    template =[
        (
            "system",
            "Baseado na mensagem a seguir monte um titulo bem simplificado sobre a intenção da mensagem, mostre apenas o titulo, sem aspas"
        ),
        (
            "human",
            "{assunto}"
        )
    ]
    prompt = ChatPromptTemplate.from_messages(template)
    chain = (prompt | model | _output_parser)
    return chain.invoke({"assunto":input})

def chain(input: str) -> str:
    prompt = ChatPromptTemplate.from_template("{assunto}")
    chain_run = (prompt | model | _output_parser)
    return chain_run.invoke({"assunto":input})


def chain_with_history(input: str, session_id: int, user_id: int) -> str:
    insert_history(session_id=session_id, mensagem=input, tipo=1)
    prompt = ChatPromptTemplate.from_messages(_template_history_question)
    chain = ( 
            prompt
            | model
            | _output_parser
    )

    with_message_history = RunnableWithMessageHistory(
        chain,
        get_chat_messasge_history_by_session,
        input_messages_key="question",
        history_messages_key="history",
        history_factory_config=[
                ConfigurableFieldSpec(
                    id="session_id",
                    annotation=str,
                    name="Session ID",
                    description="Unique identifier for a session.",
                    default="",
                    is_shared=True,
                ),
                ConfigurableFieldSpec(
                    id="user_id",
                    annotation=str,
                    name="User ID",
                    description="Unique identifier for a user.",
                    default="",
                    is_shared=True,
                )
            ]
    )
    ret = with_message_history.invoke(
        {"question":input},
        config={"configurable": {
            "session_id": session_id,
            "user_id": user_id
            }})
    insert_history(session_id=session_id, mensagem=ret, tipo=2)
    return ret

def chain_retriever(input: str)->str:
    template = PROMPT_RESP_BASEADO_CONTEXTO+"\n\nPergunta: {question}"
    prompt = ChatPromptTemplate.from_template(template)
    chain = (
        {"context": getRetriever(), "question": RunnablePassthrough()}
        | prompt
        | model
        | _output_parser
    )
    ret = chain.invoke(input)
    return ret

def chain_retriever_with_history(input: str, session_id: int)-> str:
    insert_history(session_id=session_id, mensagem=input, tipo=1)
    prompt = ChatPromptTemplate.from_messages(__template_history_question_and_context)
    context_chain = itemgetter("question") | getRetriever() 
    first_step = RunnablePassthrough.assign(context=context_chain)
    chain = (
        first_step
        | prompt
        | model
        | _output_parser
    )
    with_message_history = RunnableWithMessageHistory(
        chain,
        get_chat_messasge_history_by_session,
        input_messages_key="question",
        history_messages_key="history",
    )
    ret = with_message_history.invoke(
        {"context": getRetriever(), "question":input},
        config={"configurable": {"session_id": session_id}},
        )
    insert_history(session_id=session_id, mensagem=ret, tipo=2)
    return ret

def chain_retriever_with_sources(input: str)-> dict:
    prompt = ChatPromptTemplate.from_messages(_template_context)

    chain = (
        RunnablePassthrough.assign(context=itemgetter("documentos"), question=itemgetter("pergunta"))
        | prompt
        | model
        | _output_parser
    )

    abc = RunnableParallel(
        {"documentos": getRetriever(), "pergunta": RunnablePassthrough()}
    ).assign(resposta=chain)

    ret = abc.invoke(input)
    return ret

def chain_retriever_with_history_title(input: str, session_id: int, user_id: int)-> str:
    save_sessao(pergunta=input, session_id=session_id, user_id=user_id)
    return chain_retriever_with_history(input, session_id)