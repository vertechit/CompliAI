from qdrant_client import QdrantClient, models
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.qdrant import Qdrant, QdrantException
import os
import uuid
from langchain_core.documents.base import Document
from typing import List

_url = os.getenv("QDRANT_URL")
_api_key = os.getenv("QDRANT_API_KEY")
_collectionName='compliAI'

_embeddings_model = OpenAIEmbeddings()
_client = QdrantClient(_url,api_key=_api_key)
_doc_store = Qdrant(client=_client, collection_name=_collectionName, embeddings=_embeddings_model)

def createCollection():
    if not _client.collection_exists(_collectionName):
        _client.create_collection(collection_name=_collectionName,vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE))

def dropCollection():
    if _client.collection_exists(_collectionName):
        _client.delete_collection(_collectionName)

def loadDocuments(documents: List[Document])-> List[str]:
    ids = [str(uuid.uuid1()) for i in range(1, len(documents) + 1)]
    _doc_store.add_documents(documents=documents, ids=ids)
    return ids

def deleteDocument(ids: List[str]):
    _doc_store.delete(ids=ids)

def getVectoreStore()-> Qdrant:
    return _doc_store

def getRetriever():
    return _doc_store.as_retriever()
