import peewee
import os
from datetime import datetime
from models.User import User

db = peewee.SqliteDatabase('example.db')

if "POSTGRES_HOST" in os.environ:
    db = peewee.PostgresqlDatabase(os.environ['POSTGRES_DATASE'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'], host=os.environ['POSTGRES_HOST'], port=os.environ['POSTGRES_PORT'])

class Folders(peewee.Model):
    """
    Classe que representa as pastas do sistema
    """
    folder_id     = peewee.AutoField(primary_key=True)
    path          = peewee.CharField(max_length=30)
    descr         = peewee.CharField(max_length=100)
    user_id       = peewee.ForeignKeyField(User, backref='user')
    created       = peewee.DateTimeField(default=datetime.now())
    ar_folder_id  = peewee.IntegerField(null=True)
    class Meta:
        database = db

class FolderPermissions(peewee.Model):
    """
    Classe que representa as permissões das pastas
    """
    folderperm_id = peewee.AutoField(primary_key=True)
    user_id = peewee.ForeignKeyField(User, backref='user')
    role  = peewee.IntegerField(default= 2)
    folder_id = peewee.ForeignKeyField(Folders, backref='permissions')
    created = peewee.DateField(default=datetime.now())
    class Meta:
        database = db