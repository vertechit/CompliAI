from langchain_core.tools import tool
from typing import Annotated


@tool
def get_bases(codigo: Annotated[int, "Código da base de cálculo informada pelo usuário"],
           descricao: Annotated[str, "Descrição ou parte da descrição da base de cálculo informada pelo usuário"]
              ) -> tuple:
    """
    Ferramenta responsável por selecionar as bases de cálculo do sistema e retornar uma lista de bases ou apenas uma base para 
    montar as fórmulas de cálculo
    """
    print('------------ BASES ---------------')
    print(codigo, descricao)
    
    bases = {411: (411, 'MÉDIA PRODUÇÃO 6 DIAS ANT. AO FERIADO', 'MED PR.FERIAD.6'),
             414: (414, 'NÚMERO DE DIAS DE AVISO PREVIO', 'NRO.DIAS.AVISO'), 
             416: (416, 'NUMERO DE AVOS INDENIZADO FERIAS', 'NRO.AVOS.FE.IND')
    }
    
    return bases[codigo]
    
@tool
def get_rubricas(codigo: Annotated[int | None, "Código da rubrica informada pelo usuário, pode ser nulo caso o usuário não tenha deixado o código explicito"],
              descricao: Annotated[str | None, "Descrição ou parte da descrição da rubrica informada pelo usuário, pode ser nulo caso o usuário não tenha deixado a descrição explicita"]) -> tuple:
    """
    Ferramenta responsável por selecionar as bases de cálculo do sistema e retornar uma lista de bases ou apenas uma base para 
    montar as fórmulas de cálculo
    """
    
    print('------------ RUBRICAS ---------------')
    print(codigo, descricao)
    
    rubricas = {1: (1, 'SALÁRIO MENSALISTA', 'VALOR'),
             340: (340, 'HORAS EXTRAS', 'HORAS'), 
             416: (416, 'SALDO DE FÉRIAS', 'QUANTIDADE')
    }
    
    return rubricas[codigo]

tools = [get_bases, get_rubricas]