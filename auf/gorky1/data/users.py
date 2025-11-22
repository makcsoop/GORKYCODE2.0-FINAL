import sqlalchemy
from sqlalchemy import orm, ForeignKey
import datetime
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, unique=True)
    password = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)
    tg_name = sqlalchemy.Column(sqlalchemy.String)
    balance = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    
    # Связь с отчетами о квестах
    quest_reports = orm.relationship("QuestReport", back_populates="user")









