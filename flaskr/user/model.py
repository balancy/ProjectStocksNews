from sqlalchemy import Column, Integer, String
from flaskr.db import Base


class BotUser(Base):
    __tablename__ = "bot_user"

    id = Column(Integer, primary_key=True)
    username = Column(String(50))

    def __repr__(self):
        return f'<BotUser {self.id} {self.username}>'
