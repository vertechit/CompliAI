import json
from langchain_core.messages import ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from agents.formulas.tools import tools


_output_parser = StrOutputParser()

def start_agent(state):
    """
    Chama um agente para identificar os atributos necessários para gerar uma fórmula de cálculo de folha de pagamento.
    Os atributos podem ser uma Rubrica ou uma Base de cálculo

    Args:
        state (messages): O estado atual

    Returns:
        dict: O estado atualizado com os atributos recuperados
    """
    print("---CALL AGENT---")
    
    model = ChatOpenAI(temperature=0, streaming=True, model="gpt-4-turbo")
    chain = model.bind_tools(tools)
    messages = state["messages"]
    response = chain.invoke(messages)
    # We return a list, because this will get added to the existing list
    print('--- SAIDA AGENT ---')
    # print(response)
    return {"messages": [response]}

def organiza_atributos(state):
    mesages = state["messages"]
    # print(mesages)
    bases = []
    rubricas = []
    for message in mesages:
        print(message)
        if isinstance(message, ToolMessage):
            if message.name == 'get_bases':
                bases.append(message.content)
            if message.name == 'get_rubricas':
                rubricas.append(message.content)
                
    bases = [json.loads(base) for base in bases]
    rubricas = [json.loads(rubrica) for rubrica in rubricas]
     
    print(bases)
    print(rubricas)
    # Construir a string das bases
    bases_str_list = []
    for base in bases:
        codigo, descricao = base[0], base[1]
        bases_str_list.append(f"**Código:** {codigo}, **Descrição:** {descricao}  ")
    
    bases_str = "\n".join(bases_str_list)
    
    # Construir a string das rubricas (assumindo a mesma estrutura)
    rubricas_str_list = []
    for rubrica in rubricas:
        codigo, descricao = rubrica[0], rubrica[1]
        rubricas_str_list.append(f"**Código:** {codigo}, **Descrição:** {descricao}  ")
    
    rubricas_str = "\n".join(rubricas_str_list)
                
    mensagem = f"**Bases para considerar no cálculo**  \n{bases_str}\n___\n**Rubricas para considerar na fórmula**  \n{rubricas_str}"
    print(mensagem)
    return {"messages": [mensagem]}

def generate_formula(state):
    """
    Irá criar uma expressão de cálculo como se fosse uma coluna SQL conforme o exemplo utilizando os atributos necessários e irá retornar a expressão deo cálculo

    Args:
        state (messages): O estado atual

    Returns:
        dict: O estado atualizado com a fórmula gerada
    """
    print("---CALL GENERATE---")
    mesages = state["messages"]
    atributos = mesages[-1].content
    pergunta = mesages[0].content
    
    template =[
        (
            "system",
            """Você é um especialista em criação de fórmulas para Cálculos de folha de pagamento, utilize os atributos abaixo para gerar uma fórmula seguindo as seguintes regas
            1. Para utilizar o valor de uma rubrica coloque a letra "R:" e depois do código da rubrica, para utilizar a rubrica 41 por exemplo: R:41
            2. Para utilizar a quantidade de uma rubrica coloque a letra "Q:" e depois do código da rubrica, no caso da rubrica 38 por exemplo: Q:38
            3. Para utilizar uma base na fórmula coloque a letra "B:" e depois do código da base, para utilizar a base 414 por exemplo: B:414
            4. Para utilizar um valor fixo coloque a letra "V:" e depois o valor fixo, por exemplo para utilizar o valor 10, ficaria assim: V:10
            5. As fórmulas podem utilizar as expresões CASE WHEN THEN do SQL caso tenha senha necessário adicionar alguma condição
            6. Responda apenas a fórmula criada em formato de código do markdown da linguagem SQL, sem nenhuma outra mensagem
            Exemplos Fórmulas
            Exemplo 1: ( ( B:3 ) / V:30 ) * B:42 * ( B:38 / V:100 )
            Exemplo 2: CASE WHEN B:341 = V:0 THEN R:340 + R:450 ELSE R:230 - R:300 END
            Atributos:
            {atributos}
            """
        ),
        (
            "human",
            "{pergunta}"
        )
    ]
    prompt = ChatPromptTemplate.from_messages(template)
    model = ChatOpenAI(temperature=0, streaming=True, model="gpt-4-turbo")
    chain = (prompt | model | _output_parser)
    resposta = chain.invoke({"pergunta":pergunta, "atributos": atributos})
    print(resposta)
    return {"messages": [resposta]}