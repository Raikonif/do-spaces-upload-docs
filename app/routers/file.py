import os

from botocore.exceptions import NoCredentialsError
from botocore.session import Session
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from pydantic import BaseModel

from app.database import get_db
from app.helpers.s3_client_do import s3_client
from app.helpers.logger_config import logger
from app.models import FileDO

router = APIRouter(prefix="/api/files", tags=["files"])


class FileCreate(BaseModel):
    name: str
    url: str
    size: float
    type: str


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        if file is None:
            raise HTTPException(status_code=400, detail="No file uploaded")

        file_bytes = await file.read()
        if file_bytes is None:
            raise HTTPException(status_code=400, detail="File content is None")

        filename = file.filename
        s3_client.put_object(

            Bucket=os.getenv("DIGITAL_OCEAN_BUCKET"),
            Key=filename,
            Body=file_bytes,
            ACL='public-read',
            ContentType=file.content_type,
        )
        file_url = f"{os.getenv('DIGITAL_OCEAN_ORIGIN')}/{os.getenv('DIGITAL_OCEAN_BUCKET')}/{filename}"
        logger.info(f"File URL: {file_url}")
        return {"imageUrl": file_url}

    except NoCredentialsError as e:
        logger.error(f"Credentials not provided or incorrect: {e}")


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
