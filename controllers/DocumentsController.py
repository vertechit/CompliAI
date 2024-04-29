from models.Documentos import Documentos, Chunks
from vectors.vectorStore import loadDocuments, deleteDocument
from utils.utils import getDocuments
from typing import List
import hashlib

def saveDocument(filepath: str | bytes, filename: str, descr: str)-> str:
    file = None
    fileBytes = None
    md5file = None
    urlParam = None
    if filepath[:4] == 'http':
        urlParam = filepath
        md5file = hashlib.md5(filepath.encode("utf-8")).hexdigest()
    elif isinstance(filepath, str):
        file = open(filepath, 'rb')
        fileBytes = file.read()
        md5file = hashlib.md5(fileBytes).hexdigest()
    elif isinstance(filepath, bytes):
        fileBytes = filepath
        md5file = hashlib.md5(fileBytes).hexdigest()
    docExists = Documentos.select().where(Documentos.md5==md5file).first()
    if docExists==None:
        documento = Documentos(titulo=filename, descricao=descr, arquivo=fileBytes, md5=md5file, url=urlParam)
        documento.save()
        docs = getDocuments(filepath)
        ids = loadDocuments(docs)
        for i, doc in enumerate(docs):
            md5 = hashlib.md5(doc.page_content.encode(encoding="utf-8")).hexdigest()
            chunk = Chunks(id_vector=ids[i], md5=md5, documento_id=documento)
            chunk.save()
        return(f"Documento criado {documento}")
    else:
        return(f"Documento já existe {docExists}")

def deleteDocumento(documento_id: int)-> str:
    doc = Documentos.select().where(Documentos.documento_id==documento_id).first()
    idsVector = []
    if doc == None:
        return "Documento não encontrado"
    else:
        for chunk in doc.chunks:
            idsVector.append(chunk.id_vector)
        deleteDocument(idsVector)
        Chunks.delete().where(Chunks.documento_id==documento_id).execute()
        Documentos.delete().where(Documentos.documento_id==documento_id).execute()
        return "Documento deletado" 

def listDocumentos(documento_id: int = None)-> List[Documentos]:
    docs = None
    array = []
    if documento_id==None:
        docs = Documentos.select()
    else:
        docs = Documentos.select().where(Documentos.documento_id==documento_id)
    for doc in docs:
        newDoc = (doc.documento_id, doc.titulo, doc.descricao, doc.md5, doc.url, [(chunk.chunks_id, chunk.id_vector, chunk.md5) for chunk in doc.chunks])
        array.append(newDoc)
    return array