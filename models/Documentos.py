import peewee
import os

db = peewee.SqliteDatabase('example.db')

if "POSTGRES_HOST" in os.environ:
    db = peewee.PostgresqlDatabase(os.environ['POSTGRES_DATASE'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'], host=os.environ['POSTGRES_HOST'], port=os.environ['POSTGRES_PORT'])
    

class Documentos(peewee.Model):
    """
    Classe que representa os cadastro de documentos
    """
    documento_id = peewee.AutoField(primary_key=True)
    titulo = peewee.CharField()
    descricao = peewee.CharField()
    md5 = peewee.CharField()
    arquivo = peewee.BlobField(null=True)
    class Meta:
        database = db
        
class Chunks(peewee.Model):
    """
    Classe para armazenar os pedaços dos documentos e seus checksums e IDs
    """
    chunks_id = peewee.AutoField(primary_key=True)
    id_vector = peewee.CharField()
    md5 = peewee.CharField()
    documento_id = peewee.ForeignKeyField(Documentos, backref='chunks')
    class Meta:
        database = db