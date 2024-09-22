from botocore.session import Session
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.database import get_db
from app.models import FileDO

router = APIRouter(prefix="/api/files", tags=["files"])

class FileCreate(BaseModel):
    name: str
    url: str
    size: float
    type: str


@router.post("/")
async def create_file(file: FileCreate, db: Session = Depends(get_db)):
    file = FileDO(name=file.name, url=file.url, size=file.size, type=file.type)
    db.add(file)
    db.commit()
    db.refresh(file)
    return file


@router.get("/")
async def get_files(db: Session = Depends(get_db)):
    return db.query(FileDO).all()
