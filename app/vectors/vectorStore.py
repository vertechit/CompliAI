from qdrant_client import QdrantClient, models
from langchain_chroma import Chroma
import chromadb
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.qdrant import Qdrant, QdrantException
import os
import uuid
from langchain_core.documents.base import Document
from typing import List

_vectordb_type = os.getenv("VECTORDB", 'CHROMA')
_url = os.getenv("QDRANT_URL")
_api_key = os.getenv("QDRANT_API_KEY")
_collectionName='compliAI'

_client = ""
_doc_store = ""

_embeddings_model = OpenAIEmbeddings()
if _vectordb_type == "CHROMA":
    _client = chromadb.PersistentClient()
    _doc_store = Chroma(client=_client,
                     collection_name=_collectionName,
                     embedding_function=_embeddings_model
                )
else:
    _client = QdrantClient(_url,api_key=_api_key)
    _doc_store = Qdrant(client=_client, collection_name=_collectionName, embeddings=_embeddings_model)


def createCollection():
    if _vectordb_type == "CHROMA":
        try:
            _client.get_collection(name=_collectionName)
        except:
            _client.create_collection(name=_collectionName)
    else:
        if not _client.collection_exists(_collectionName):
            _client.create_collection(collection_name=_collectionName,vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE))

def dropCollection():
    if _vectordb_type == "CHROMA":
        if _client.get_collection(name=_collectionName):
            _client.delete_collection(_collectionName)
                
    else:
        if _client.collection_exists(_collectionName):
            _client.delete_collection(_collectionName)

def loadDocuments(documents: List[Document])-> List[str]:
    ids = [str(uuid.uuid1()) for i in range(1, len(documents) + 1)]
    _doc_store.add_documents(documents=documents, ids=ids)
    return ids

def deleteDocument(ids: List[str]):
    if len(ids) > 0:
        _doc_store.delete(ids=ids)

def getVectoreStore()-> Qdrant | Chroma:
    return _doc_store

def getRetriever():
    return _doc_store.as_retriever()
