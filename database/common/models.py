from datetime import datetime

import peewee as pw

db = pw.SqliteDatabase('loging_base.db')


class ModelBase(pw.Model):
    created_at = pw.DateField(default=datetime.now())

    class Meta():
        database = db


class History(ModelBase):
    temp_now = pw.TextField()
    temp_like_now = pw.TextField()

