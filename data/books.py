import sqlalchemy
from sqlalchemy import orm, Integer, String, Boolean, DateTime, ForeignKey
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class Books(SqlAlchemyBase, UserMixin):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    img = sqlalchemy.Column(sqlalchemy.String)

