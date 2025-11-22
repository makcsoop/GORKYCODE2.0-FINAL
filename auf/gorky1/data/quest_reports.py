import sqlalchemy
from sqlalchemy import orm, ForeignKey
import datetime
from .db_session import SqlAlchemyBase


class QuestReport(SqlAlchemyBase):
    __tablename__ = 'quest_reports'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    quest_id = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey('quests.id'), nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey('users.id'), nullable=False)
    is_completed = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    photo_path = sqlalchemy.Column(sqlalchemy.String)  # путь к загруженному фото
    comment = sqlalchemy.Column(sqlalchemy.Text)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    
    # Связи
    quest = orm.relationship("Quest", back_populates="reports")
    user = orm.relationship("User", back_populates="quest_reports")


