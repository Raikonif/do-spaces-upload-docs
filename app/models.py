from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime


class FileDO(BaseModel):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    url = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<File {self.name}>"
