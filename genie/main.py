from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)

def simpleChain(input: str) -> str:
    prompt = ChatPromptTemplate.from_template("{assunto}")
    output_parser = StrOutputParser()
    
    chain = (
        {"assunto": RunnablePassthrough()}
        | prompt
        | model
        | output_parser
    )
    return chain.invoke(input)