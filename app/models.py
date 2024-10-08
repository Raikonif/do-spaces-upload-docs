from datetime import datetime
from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Float


class FileDO(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    url = Column(String, index=True)
    size = Column(Float, index=True)
    type = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.date(datetime.now()))
    updated_at = Column(DateTime, default=datetime.date(datetime.now()))

    def __repr__(self):
        return f"<File {self.name}>"
