import qdrant_client
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.qdrant import Qdrant,QdrantException
import os

embeddings_model = OpenAIEmbeddings()
client = qdrant_client.QdrantClient(
    os.environ["QUDRANT_URL"],
    api_key=os.environ["QUDRANT_API_KEY"]
    )
doc_store = Qdrant(
client=client, collection_name="texts", 
embeddings=embeddings_model,
    )

def retRetriever() -> VectorStoreRetriever:
    return doc_store.as_retriever()
    