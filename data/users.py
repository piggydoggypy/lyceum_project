import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    telephone = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    is_employer = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    profile_image = sqlalchemy.Column(sqlalchemy.String, default='/static/img/default_image.png')
    responded_vacancies = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    vacancy = orm.relationship("Vacancy", back_populates='user')

    def __repr__(self):
        return f'<Company> id:{self.id} login:{self.login} name:{self.name} email:{self.email} is_employer:{self.is_employer}>'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)