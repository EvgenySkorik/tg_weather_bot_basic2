from typing import Dict, List, TypeVar

from peewee import ModelSelect

from database.common.models import ModelBase
from database.common.models import db

T = TypeVar("T")


def _store_date(db: db, model: T, *data: List[Dict]) -> None:
    with db.atomic():
        model.insert_many(*data).execute()


def _retrieve_all_data(db: db, name: str, model: T, *columns: ModelBase) -> ModelSelect:
    with db.atomic():
        response = model.select().where(model.user_name == name)

    return response


class CRUDInterface():
    @staticmethod
    def create():
        return _store_date

    @staticmethod
    def retrieve():
        return _retrieve_all_data


if __name__=='main':
    _store_date()
    _retrieve_all_data()
    CRUDInterface()
