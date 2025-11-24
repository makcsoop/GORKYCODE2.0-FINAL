import sqlalchemy
from sqlalchemy import orm
import datetime
from .db_session import SqlAlchemyBase


class Tickets(SqlAlchemyBase):
    __tablename__ = 'tickets'
    # complaint_id, status, created_at, description, distric, resolution, execution_date, executor_id, final_status_at, address
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    address = sqlalchemy.Column(sqlalchemy.String)
    status = sqlalchemy.Column(sqlalchemy.String)
    created_at = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    distric = sqlalchemy.Column(sqlalchemy.Integer)
    resolution = sqlalchemy.Column(sqlalchemy.String)
    execution_date = sqlalchemy.Column(sqlalchemy.String)
    executor_id = sqlalchemy.Column(sqlalchemy.Integer)
    final_status_at = sqlalchemy.Column(sqlalchemy.String)
    complaint_id = sqlalchemy.Column(sqlalchemy.String)


class PlanTime(SqlAlchemyBase):
    __tablename__ = "plan_time"
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_ticket = sqlalchemy.Column(sqlalchemy.Integer)
    check_data = sqlalchemy.Column(sqlalchemy.DateTime)
    end_data = sqlalchemy.Column(sqlalchemy.DateTime)
    status = sqlalchemy.Column(sqlalchemy.String)


class Ranks(SqlAlchemyBase):
    __tablename__ = "ranks"
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_executor = sqlalchemy.Column(sqlalchemy.Integer)
    value = sqlalchemy.Column(sqlalchemy.Integer)

class Executor(SqlAlchemyBase):
    __tablename__ = "executor"
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)

class HistoryRanks(SqlAlchemyBase):
    __tablename__ = "history_ranks"
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    notes = sqlalchemy.Column(sqlalchemy.String)



    









