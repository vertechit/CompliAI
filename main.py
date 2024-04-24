from fastapi import Body, FastAPI
from pydantic import BaseModel, Field
from genie.genie import main
from llm.llm import chain, chainWithHistory, chainPiada

app = FastAPI()

class InputChat(BaseModel):
    SystemMessage: str | None = Field(default=None, examples=["Responde de forma educada"])
    HumamMessage: str = Field(examples=["Quem é o presidente do Brasil?"])
    
class ResponseChat(BaseModel):
    AiMessage: str = Field(examples=["Presidente do brasil é o Lula"])

@app.post("/piada")
def retornaMensagem(mensagem=Body()):
    return {"retorno": chainPiada(mensagem)}

@app.post("/chain")
def retornaMensagem(chat: InputChat)-> ResponseChat:
    ret = chain(chat.HumamMessage)
    response = ResponseChat(AiMessage=ret)
    return response

@app.post("/chainHistory/{sessionId}")
def retornaMensagem(sessionId: int, chat: InputChat)-> ResponseChat:
    ret = chainWithHistory(chat.HumamMessage, sessionId)
    response = ResponseChat(AiMessage=ret)
    return response

if __name__ == "__main__":
    main()