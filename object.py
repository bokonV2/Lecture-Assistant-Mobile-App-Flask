from peewee import *

sqlite_db = SqliteDatabase('app.db', pragmas={'journal_mode': 'wal'})

class BaseModel(Model):
    """A base model that will use our Sqlite database."""
    class Meta:
        database = sqlite_db

class Disciplines(BaseModel):
    id = PrimaryKeyField()
    name = TextField()

class Lectures(BaseModel):
    id = PrimaryKeyField()
    dis_id = IntegerField()
    name = TextField()
    content = TextField()
    file = TextField()

class User(BaseModel):
    id = PrimaryKeyField()
    fio = TextField()
    email = TextField()
    group = TextField()
    spec = TextField()
    password = TextField()
    is_teacher = BooleanField()

if __name__ == '__main__':
    Disciplines.create_table()
    Lectures.create_table()
    User.create_table()