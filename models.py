import datetime

from peewee import *


db = SqliteDatabase('journal.db')


class Entries(Model):
    title = CharField(max_length=250)
    date = DateTimeField(default=datetime.datetime.now)
    time_spent = IntegerField()
    learned = TextField()
    resources = TextField()

    class Meta:
        database = db
        order_by = ('-joined_at',)

    @classmethod
    def create_entry(cls, title, date, time_spent, learned, resources):

class Tag(Model):
    one = ForeignKeyField()
    many = ForeignKeyField()

    class Meta:
        database = db
        indexes = ()
    


def initialize():
    db.connect()
    db.create_tables([Entries], safe=True)
    db.close()
