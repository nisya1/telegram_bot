import sqlalchemy as sqla
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Movies(SqlAlchemyBase):
    __tablename__ = 'Movies'

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String)
    duration = sqla.Column(sqla.String)
    data = sqla.Column(sqla.String)
    price = sqla.Column(sqla.Integer)

    def __repr__(self):
        return f'{self.name}'
