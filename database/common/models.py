from datetime import datetime
import peewee as pw


db = pw.SqliteDatabase('loging_base.db')


class ModelBase(pw.Model):
    """Класс для создания модели таблицы в БД"""

    created_at = pw.DateField(default=datetime.now())

    class Meta():
        database = db


class History(ModelBase):
    number = pw.TextField()
    message = pw.TextField()
        