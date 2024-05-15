import peewee
import os

db = peewee.SqliteDatabase('example.db')

if "POSTGRES_HOST" in os.environ:
    db = peewee.PostgresqlDatabase(os.environ['POSTGRES_DATASE'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'], host=os.environ['POSTGRES_HOST'], port=os.environ['POSTGRES_PORT'])
    
class User(peewee.Model):
    """
    Classe que representa os Usuários
    """
    user_id = peewee.AutoField(primary_key=True)
    login = peewee.CharField(unique=True)
    senha = peewee.CharField(null=True)
    tipo = peewee.IntegerField(constraints=[peewee.Check('tipo in (0,1)')]) # 0 = Basico / 1 = SSO
    class Meta:
        database = db