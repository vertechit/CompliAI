from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

def chain(input: str) -> str:
    prompt = ChatPromptTemplate.from_template("Me conte uma piada sobre {assunto}")
    model = ChatOpenAI(model="gpt-3.5-turbo")
    output_parser = StrOutputParser()
    
    chain = (prompt | model | output_parser)
    return chain.invoke({"assunto":input})