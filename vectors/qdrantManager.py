from qdrant_client import QdrantClient, models
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.qdrant import Qdrant,QdrantException
from langchain_community.document_loaders.csv_loader import CSVLoader
import os

embeddings_model = OpenAIEmbeddings()
url = os.environ["QUDRANT_URL"]
api_key = os.environ["QUDRANT_API_KEY"]
collection='compliAI'

salarioCSV = CSVLoader(file_path='./CSVs/salarios.csv', csv_args={
    'delimiter': ';',
    'quotechar': '"',
}, source_column="Nome")

salarios = salarioCSV.load()

client = QdrantClient(
    url,
    api_key=api_key
)

print(salarios)

client.create_collection(
    collection_name=collection,
    vectors_config=models.VectorParams(size=100, distance=models.Distance.COSINE)
)

doc_store = Qdrant(client=client, collection_name=collection, embeddings=embeddings_model)
doc_store.add_documents(salarios)

print(doc_store.similarity_search(query="Lucas"))

#qdrant = Qdrant.from_documents(
#    salarios,
#    embeddings_model,
#    url=url,
#    prefer_grpc=True,
#    api_key=api_key,
#    collection_name="my_documents"
#)
