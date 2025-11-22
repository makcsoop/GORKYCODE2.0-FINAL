import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Quest(SqlAlchemyBase):
    __tablename__ = 'quests'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    latitude = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    longitude = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    points = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    status = sqlalchemy.Column(sqlalchemy.String, default='не взята')  # не взята, в исполнении, выполнена
    image_path = sqlalchemy.Column(sqlalchemy.String)  # путь к предзаготовленной картинке
    
    # Связь с отчетами
    reports = orm.relationship("QuestReport", back_populates="quest")
    
    def get_status_display(self):
        """Возвращает читаемый статус"""
        status_map = {
            'не взята': 'Не взята',
            'в исполнении': 'В исполнении',
            'выполнена': 'Выполнена'
        }
        return status_map.get(self.status, self.status)

