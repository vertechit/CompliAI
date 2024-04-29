import mimetypes
import validators
import os
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents.base import Document
from typing import List


def getMimetype(filepath: str)->str:
    return mimetypes.guess_type(filepath)

def getDocuments(filepath: str)->List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300,chunk_overlap=20)
    mimetypeP = getMimetype(filepath)
    mimetype = mimetypeP[0]
    document = List[Document]
    if(mimetype==None):
        if(validators.url(filepath)):
            mimetype="url"
        elif(os.path.isdir(filepath)):
            mimetype = "dir"
    if(mimetype=='application/pdf'):
        document = PyPDFLoader(filepath).load_and_split()
        document = text_splitter.split_documents(document)
    elif(mimetype=='text/csv'):
        document = CSVLoader(file_path=filepath, csv_args={'delimiter': ';','quotechar': '"',}, source_column="Nome").load()
    elif(mimetype=="url"):
        document = WebBaseLoader(filepath).load()
        document = text_splitter.split_documents(document)
    elif(mimetype=="dir"):
        document = []
        for arquivo in os.listdir(filepath):
            if arquivo != None:
                for doc in getDocuments(filepath+arquivo):
                    document.append(Document(page_content=doc.page_content,metadata=doc.metadata))
    
    return(document)