from models.Folders import Folders, FolderPermissions
from models.Documentos import Documentos
from controllers.DocumentsController import delete_document
from typing import List
import os

def create_folder(path: str, descr: str, user_id: int, ar_folder_id: int) -> str:
    if path == None:
        return 'Erro: Não foi possível realizar a criação da pasta pois o diretório da pasta não foi definido!'
    elif descr == None:
        return 'Erro: Não foi possível realizar a criação da pasta pois o nome da pasta não foi definido!'
    if path.find(' ') != -1:
        return 'Erro: Não é possível criar uma pasta caso o caminho possua um ou mais caractéres "espaço"!'
    if Folders.select().where((Folders.descr == descr) & (Folders.ar_folder_id == ar_folder_id)):
        return 'Erro: Já existe uma pasta com o mesmo nome no diretório informado!'
    else:
        pasta = Folders(path=path, descr=descr, user_id=user_id, ar_folder_id=ar_folder_id )
        pasta.save()
        folder_id = Folders.select(Folders.folder_id).where((Folders.descr == descr) & (Folders.ar_folder_id == ar_folder_id))
        pasta_perm = FolderPermissions(user_id=user_id, role=0, folder_id=folder_id)
        pasta_perm.save()
        return f'Pasta {descr} criada com sucesso!'
    
def delete_folder(p_folder_id: int, user_id: int) -> str:
    if p_folder_id == 1:
        return 'Não é possível realizar a exclusão da pasta Main'
    else:
        folder_id = Folders.select(Folders.folder_id).where((Folders.folder_id == p_folder_id) & (Folders.user_id == user_id)).first()
        if folder_id == None:
            return 'Pasta não localizada!'
        else:
            def get_rowcount(query):
                return query.count()

            def select_ids(en_folder_id, list_ids=None):
                ids = []
                if list_ids is None:
                    query = Folders.select(Folders.folder_id).where(Folders.folder_id == en_folder_id)
                else:
                    print('Entrou no else do select_ids')
                    query = Folders.select(Folders.folder_id).where(Folders.ar_folder_id.in_(tuple(list_ids)))

                for folder in query:
                    ids.append(folder.folder_id)
                rowcount = get_rowcount(query)
                return ids, rowcount

            # Iniciando o processo
            list_ids = []
            x = 1
            rowcount_atu = 0
            rowcount_ant = 0

            while True:
                if x == 1:
                    ids, rowcount_atu = select_ids(en_folder_id= p_folder_id)  
                else:
                    ids, rowcount_atu = select_ids(en_folder_id= p_folder_id, list_ids=list_ids)  

                if rowcount_atu == rowcount_ant:
                    break
                else:
                    list_ids.extend(ids)
                    x += 1
                    rowcount_ant = rowcount_atu

        descr = Folders.select().where(Folders.folder_id == p_folder_id).first()
        lista_sem_duplicatas = list(set(list_ids))

        # Deleta Documentos
        docs = []
        query_doc = Documentos.select(Documentos.documento_id).where(Documentos.folder_id.in_(tuple(lista_sem_duplicatas)))
        for doc in query_doc:
            docs.append(doc.documento_id)
        
        if docs is not None:
            for doc in docs:
                delete_document(doc, user_id)

        # Deleta as pastas
        FolderPermissions.delete().where(FolderPermissions.folder_id.in_(tuple(lista_sem_duplicatas))).execute()
        Folders.delete().where(Folders.folder_id.in_(tuple(lista_sem_duplicatas))).execute()

        if len(lista_sem_duplicatas) == 1:
            return f'Pasta {descr.descr} deletada.'
        elif len(lista_sem_duplicatas) >= 1:
            return f'{len(lista_sem_duplicatas)} pastas foram deletadas.'
        else:
            return 'Erro!'

def rename_folder(folder_id: int, descr: str) -> str:
    if folder_id == 1:
        return 'Não é possível renomear a pasta Main'
    else:
        folder = Folders.select(Folders.folder_id).where((Folders.folder_id == folder_id)).first()
        if folder.get() == None:
            return 'Pasta não localizada!'
        else:
            descr_ant = Folders.select().where((Folders.folder_id == folder_id)).first()
            Folders.update({Folders.descr: descr}).where((Folders.folder_id == folder_id)).execute()
            return f'Nome da pasta alterado de {descr_ant.descr} para {descr}'

def list_folders(folder_id: int, user_id: int = None) -> List[Folders]:
    folderPai = None
    array   = []
    if folder_id == 1:
        folderPai = Folders.select().where((Folders.user_id == user_id) & (Folders.ar_folder_id >> None)).first()
        folderFilho = Folders.select().where((Folders.ar_folder_id == 1))
    else: #Revisar depois uma forma de tratar o erro que ocorre quando o select FolderPai não retornar valor no ELSE
        folderPai = Folders.select().where((Folders.folder_id == folder_id)).first()
        folderFilho = Folders.select().where((Folders.ar_folder_id == folder_id))
    if folderPai is None:
        folderPai = Folders.select().where((Folders.user_id == user_id) & (Folders.ar_folder_id >> None)).first() 
    newFolder = (folderPai.folder_id, folderPai.path, folderPai.descr, folderPai.user_id, folderPai.created, folderPai.ar_folder_id,[(folderfi.folder_id, folderfi.path, folderfi.descr, folderfi.user_id, folderfi.created, folderfi.ar_folder_id) for folderfi in folderFilho], [(doc.documento_id, doc.titulo, doc.descricao, doc.md5, doc.url, doc.user_id, doc.folder_id) for doc in folderPai.folders])
    array.append(newFolder)
    return array

def give_permission(user_id_atu: int, folder_id: int, role: int, user_id: int) -> str:
    permission_id = FolderPermissions.select(FolderPermissions.folderperm_id).where((FolderPermissions.user_id == user_id) & (FolderPermissions.folder_id == folder_id)).first()
    if permission_id == None:
        permission = FolderPermissions(user_id=user_id, role=role, folder_id=folder_id)
        permission.save()
        return 'Permissão concebida com sucesso!'
    else:
        FolderPermissions.update({FolderPermissions.role: role}).where((FolderPermissions.folderperm_id == permission_id)).execute()
        return 'Permissão atualizada com sucesso!'

def delete_permission(user_id: int, folder_id: int) -> str:
    permissao = FolderPermissions.select(FolderPermissions.folderperm_id).where((FolderPermissions.user_id == user_id) & (FolderPermissions.folder_id == folder_id)).first()
    if permissao == None:
        return "Permissão não encontrada!"
    else:
        FolderPermissions.delete().where(FolderPermissions.folderperm_id == permissao).execute()
        return "Permissão deletada!"

def list_permission(folder_id: int) -> List[FolderPermissions]:
    folder = None
    array = []
    folder = Folders.select().where((Folders.folder_id == folder_id)).first()
    newPerm = (folder.folder_id, folder.path, folder.descr, folder.user_id, folder.created, folder.ar_folder_id,[(perm.folderperm_id, perm.user_id, perm.role, perm.folder_id, perm.created) for perm in folder.folders])
    array.append(newPerm)
    return array