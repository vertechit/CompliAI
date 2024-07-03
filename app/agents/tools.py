from langchain.tools.retriever import create_retriever_tool
from vectors.vectorStore import getRetriever

retriever_tool = create_retriever_tool(
    getRetriever(),
    "retrieve_documents",
    "Retorna informações de documentos sobre assuntos Fiscais e de Folha de pagamento, ou sobre a empresa Comvert"
)

tools = [retriever_tool]