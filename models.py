import datetime

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

from peewee import *


DATABASE = SqliteDatabase('journal.db')


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)
        
    @classmethod
    def create_user(cls, username, email, password, admin=False):
        try:
            with DATABASE.transaction():
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=admin 
                    )
        except IntegrityError:
            raise ValueError('User already exists.')


class Entry(Model):
    title = CharField(max_length=225)
    entry_date = DateField(default=datetime.date.today)
    time_spent = IntegerField(null=False)
    learned = TextField()
    resources = TextField()
    user = ForeignKeyField(User, related_name='entries')
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
        order_by = ('-entry_date',)

    @classmethod
    def create_entry(cls, title, entry_date, 
                    time_spent, learned, resources, user):
        cls.create(
            title=title, 
            entry_date=entry_date,
            time_spent=time_spent,
            learned=learned,
            resources=resources, 
            user=user
            )
    

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Entry], safe=True)
    DATABASE.close()
