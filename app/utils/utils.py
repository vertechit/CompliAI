import mimetypes
import validators
import os
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents.base import Document
from typing import List
from models import ChatHistory, Documentos, User
from vectors import vectorStore
from bs4 import SoupStrainer


def destroyDatabases():
    if os.getenv("RECREATE_DB", '0') == '1':
        vectorStore.dropCollection()
        if Documentos.Chunks.table_exists():
            Documentos.Chunks.drop_table()
        if ChatHistory.ChatHistory.table_exists():
            ChatHistory.ChatHistory.drop_table()
        if ChatHistory.ChatSession.table_exists():
            ChatHistory.ChatSession.drop_table()
        if Documentos.Documentos.table_exists():
            Documentos.Documentos.drop_table()
        if User.User.table_exists():
            User.User.drop_table()

def initDatabases():
    vectorStore.createCollection()
    if not User.User.table_exists():
        User.User.create_table()
    if not ChatHistory.ChatSession.table_exists():
        ChatHistory.ChatSession.create_table()
    if not ChatHistory.ChatHistory.table_exists():
        ChatHistory.ChatHistory.create_table()
    if not Documentos.Documentos.table_exists():
        Documentos.Documentos.create_table()
    if not Documentos.Chunks.table_exists():
        Documentos.Chunks.create_table()

def get_extension(mimetype: str)->str:
    return mimetypes.guess_extension(mimetype)

def getMimetype(filepath: str)->str:
    return mimetypes.guess_type(filepath)

def getDocuments(filepath: str)->List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800,chunk_overlap=100)
    mimetypeP = getMimetype(filepath)
    mimetype = mimetypeP[0]
    document = List[Document]
    if(mimetype==None):
        if(validators.url(filepath)):
            mimetype="url"
    if(mimetype=='application/pdf'):
        document = PyPDFLoader(filepath).load_and_split()
        document = text_splitter.split_documents(document)
    elif(mimetype=='text/csv'):
        document = CSVLoader(file_path=filepath, csv_args={'delimiter': ';','quotechar': '"',}, source_column="Nome").load()
    elif(mimetype=="url"):
        bskwarg = {}
        if filepath.find('documentacao.compliancefiscal.com.br') > 0:
            strainer1 = SoupStrainer(id='post')
            bskwarg = {
                'parse_only': strainer1
            }
        elif filepath.find('docs.compliancecapitalhumano.com.br') > 0:
            strainer2 = SoupStrainer(attrs="post")
            bskwarg = {
                'parse_only': strainer2
            }
        document = WebBaseLoader(filepath, bs_kwargs=bskwarg).load()
        document = text_splitter.split_documents(document)
    
    return(document)