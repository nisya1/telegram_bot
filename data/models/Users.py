import sqlalchemy as sqla

from data.db_session import SqlAlchemyBase


class Users(SqlAlchemyBase):
    __tablename__ = 'Users'

    id = sqla.Column(sqla.Integerь, primary_key=True)
    tickets = sqla.Column(sqla.String)

    def __repr__(self):
        return f'{self.tickets}'
