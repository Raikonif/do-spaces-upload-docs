from datetime import datetime
from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime


class FileDO(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    url = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.date(datetime.now()))
    updated_at = Column(DateTime, default=datetime.date(datetime.now()))

    def __repr__(self):
        return f"<File {self.name}>"
