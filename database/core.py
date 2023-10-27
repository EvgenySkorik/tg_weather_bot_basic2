from database.utils.CRUD import CRUDInterface
from database.common.models import db, History

"""Подсоединяемся к базе, создаём структуру таблицы, подгружая её интерфейс"""
db.connect()
db.create_tables([History])

crud = CRUDInterface()


if __name__ == '__main__':
    crud()
