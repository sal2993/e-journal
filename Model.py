#!/usr/bin/python

from peewee import *
import datetime

db = SqliteDatabase('/home/sal/bin/entries2.db')

class User(Model):
    username = CharField()
    password = CharField()

    class Meta:
        database = db

class Entry(Model):
    owner = ForeignKeyField(User, related_name='entries')
    body = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


