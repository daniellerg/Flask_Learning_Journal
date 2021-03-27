import datetime

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

from peewee import *


db = SqliteDatabase('journal.db')


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = db
        order_by = ('-joined_at',)
    
    def get_entries(self):
        return Entry.select().where(Entry.user == self)
        
    @classmethod
    def create_user(cls, username, email, password, admin=False):
        try:
            with models.db.transaction():
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
    entry_date = DateTimeField(default=datetime.date.today)
    time_spent = IntegerField(null=False)
    learned = TextField()
    resources = TextField()
    user = ForeignKeyField(User, related_name='entries')
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        order_by = ('-entry_date',)

    @classmethod
    def create_entry(cls, title, entry_date, time_spent, learned, resources, user,):
        try:
            cls.create(
                title=title, 
                entry_date=date,
                time_spent=time_spent,
                learned=learned,
                resources=resources, 
                user=user
                )
        except IntegrityError:
            raise ValueError('Entry already exists')


class JournalList(Model):
    title = CharField(max_length=250)
    date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        order_by = ('-timestamp',)


class Tag(Model):
    one = ForeignKeyField(User, related_name='relationships')
    many = ForeignKeyField(User, related_name='related_to')

    class Meta:
        database = db
        indexes = (
            (('one', 'many'), True),
        )
    

def initialize():
    db.connect()
    db.create_tables([User, Entry, JournalList, Tag], safe=True)
    db.close()
