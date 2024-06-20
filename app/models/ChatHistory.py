import peewee
import os
from datetime import datetime
from models.User import User

db = peewee.SqliteDatabase('example.db')

if "POSTGRES_HOST" in os.environ:
    db = peewee.PostgresqlDatabase(os.environ['POSTGRES_DATASE'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'], host=os.environ['POSTGRES_HOST'], port=os.environ['POSTGRES_PORT'])

class ChatSession(peewee.Model):
    """
    Classe que representa o id das sessões
    """
    session_id = peewee.AutoField(primary_key=True)
    titulo = peewee.CharField(max_length=3000, null=True)
    criado = peewee.DateTimeField(default= datetime.now)
    user_id = peewee.ForeignKeyField(User, backref='user')
    class Meta:
        database = db

class ChatHistory(peewee.Model):
    """
    Classe que representa o historico das mensagens
    """
    chathistory_id = peewee.AutoField(primary_key=True)
    session_id = peewee.ForeignKeyField(ChatSession, backref='history')
    mensagem = peewee.CharField()
    tipo = peewee.IntegerField(constraints=[peewee.Check('tipo in (0,1,2)')]) # 0 = SystemMessage / 1 = HumamMessage / 2 = AiMessage
    criado = peewee.DateTimeField(default= datetime.now)
    class Meta:
        database = db