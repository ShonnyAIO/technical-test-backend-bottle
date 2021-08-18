from peewee import (SqliteDatabase, Model, CharField,
                    ForeignKeyField, DateField, DoesNotExist, PrimaryKeyField)

from dotenv import load_dotenv
from passlib.hash import pbkdf2_sha512 as hsh
from hashlib import md5
import sqlite3

load_dotenv()

SECRET_KEY = 'This is a secret'
rutas = 'datos.db'
db = SqliteDatabase(rutas)


class Users(Model):

    id = PrimaryKeyField(null=False)
    name = CharField(max_length=30, unique=True)
    password = CharField(max_length=20)

    @staticmethod
    def gen_hash(password):
        _secret = md5(SECRET_KEY.encode()).hexdigest()
        _password = md5(password.encode()).hexdigest()
        return hsh.hash(_secret + _password)

    def verify(self, password):
        _secret = md5(SECRET_KEY.encode()).hexdigest()
        _password = md5(password.encode()).hexdigest()
        return hsh.verify(_secret+_password, self.password)

    class Meta:
        database = db


class Todo(Model):

    id = PrimaryKeyField(null=False)
    user_id = ForeignKeyField(Users, backref="todos")
    titulo = CharField()
    descripcion = CharField()

    class Meta:
        database = db
        db_table = "todos"

    @staticmethod
    def create(**args):
        query = "INSERT INTO todos ('user_id','titulo','descripcion')VALUES ({user_id},'{titulo}','{descripcion}')".format(
            **args)
        conn = sqlite3.connect(rutas)

        c = conn.cursor()
        c.execute(query)

        conn.commit()
        conn.close()

    def getById(user_id):
        query = ("SELECT * FROM todos WHERE user_id = '%d'" % user_id)
        conn = sqlite3.connect(rutas)

        c = conn.cursor()
        c.execute(query)

        rows = c.fetchall()

        conn.commit()
        conn.close()

        return rows


db.create_tables([Todo, Users])
