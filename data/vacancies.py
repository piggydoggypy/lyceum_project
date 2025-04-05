import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Vacancy(SqlAlchemyBase):
    __tablename__ = 'vacancies'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    company_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')

    # def __repr__(self):
    #     return f'<Vacancy> id:{self.id} title:{self.title} content:{self.content}'
