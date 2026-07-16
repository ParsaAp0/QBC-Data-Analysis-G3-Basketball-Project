from sqlalchemy import and_, Column, Integer
from sqlalchemy.orm import relationship

from db_connection import base


class Player(base):
    __tablename__ = "players"
    __table_args__ = {'keep_existing': True}

    id = Column(Integer, primary_key=True)
    