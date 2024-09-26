import os

from botocore.exceptions import NoCredentialsError
from botocore.session import Session
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse

from app.database import get_db
from app.helpers.redirect_path import folder_exists
from app.helpers.s3_client_do import s3_client
from app.helpers.logger_config import logger
from app.models import FileDO

router = APIRouter(prefix="/api/files", tags=["files"])


class FileCreate(BaseModel):
    name: str
    url: str
    size: float
    type: str


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        if file is None:
            raise HTTPException(status_code=400, detail="No file uploaded")

        file_bytes = await file.read()
        if file_bytes is None:
            raise HTTPException(status_code=400, detail="File content is None")

        filename = file.filename
        s3_client.put_object(
            Bucket=os.getenv("DIGITAL_OCEAN_FOLDER"),
            Key=filename,
            Body=file_bytes,
            ACL='public-read',
            ContentType=file.content_type,
        )
        file_url = f"{os.getenv('DIGITAL_OCEAN_ORIGIN')}/{os.getenv('DIGITAL_OCEAN_FOLDER')}/{filename}"
        logger.info(f"File URL: {file_url}")
        return {"file_url": file_url}

    except NoCredentialsError as e:
        logger.error(f"Credentials not provided or incorrect: {e}")


@router.delete("/remove_file_do/{filename}")
async def remove_file_do(filename: str):
    try:
        if filename is None:
            raise HTTPException(status_code=400, detail="No file name provided")

        s3_client.delete_object(
            Bucket=os.getenv("DIGITAL_OCEAN_FOLDER"),
            Key=filename,
        )
        return {"message": f"File {filename} deleted"}

    except NoCredentialsError as e:
        logger.error(f"Credentials not provided or incorrect: {e}")


@router.post("/")
async def create_file(file: FileCreate, db: Session = Depends(get_db)):
    file = FileDO(name=file.name, url=file.url, size=file.size, type=file.type)

    db.add(file)
    db.commit()
    db.refresh(file)
    return file


@router.delete("/{file_id}")
async def delete_file_data(file_id: int, db: Session = Depends(get_db)):
    file = db.query(FileDO).filter(FileDO.id == file_id).first()
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")

    db.delete(file)
    db.commit()
    return {"message": "File deleted"}


@router.get("/{filename}")
async def download_file(filename: str):
    downloads_folder = folder_exists()
    if filename is None:
        raise HTTPException(status_code=400, detail="No file name provided")
    file_path = os.path.join(downloads_folder, filename)
    folder_name = os.getenv("DIGITAL_OCEAN_FOLDER")
    s3_client.download_file(folder_name, filename, file_path)
    logger.info("File downloaded: " + filename)
    return FileResponse(file_path)


@router.get("/")
async def get_files(db: Session = Depends(get_db)):
    return db.query(FileDO).all()
