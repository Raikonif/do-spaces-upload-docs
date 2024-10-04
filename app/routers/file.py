import os
from sys import prefix

from botocore.exceptions import NoCredentialsError, ClientError
from botocore.session import Session
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from pydantic import BaseModel
from fastapi.responses import FileResponse

from app.database import get_db
from app.helpers.redirect_path import folder_exists
from app.helpers.s3_client_do import s3_client, s3
from app.helpers.logger_config import logger
from app.models import FileDO

router = APIRouter(prefix="/api/files", tags=["files"])


class FileCreate(BaseModel):
    name: str
    url: str
    size: float
    type: str


@router.get("/")
async def get_files(db: Session = Depends(get_db)):
    return db.query(FileDO).all()


@router.get("/download/{filename:path}")
async def download_file(filename: str):
    if filename is None:
        raise HTTPException(status_code=400, detail="No file name provided")

    downloads_folder = folder_exists()
    file_path = os.path.join(downloads_folder, filename.split("/")[-1])
    bucket_name = os.getenv("DIGITAL_OCEAN_BUCKET")

    s3.download_file(bucket_name, filename, file_path)
    logger.info("File downloaded: " + filename)

    return FileResponse(file_path)


@router.get("/list_obj")
async def list_folders(prefix_dir: str = os.getenv("DIGITAL_OCEAN_FOLDER") + '/'):
    response = s3.list_objects_v2(
        Bucket=os.getenv("DIGITAL_OCEAN_BUCKET"),
        Prefix=prefix_dir,
        Delimiter='/'  # Delimiter para listar carpetas y archivos directos
    )

    files = response.get('Contents', [])
    subfolders = response.get('CommonPrefixes', [])

    actual_files = [f for f in files if not f['Key'].endswith('/')]
    return {
        "files": actual_files,
        "folders": subfolders
    }


@router.post("/")
async def create_file(file: FileCreate, db: Session = Depends(get_db)):
    file = FileDO(name=file.name, url=file.url, size=file.size, type=file.type)

    db.add(file)
    db.commit()
    db.refresh(file)
    logger.info(f"File created: {file}")
    return file


@router.post("/upload")
async def upload_file(file: UploadFile = File(...), path: str = Form(...)):
    try:
        if file is None:
            raise HTTPException(status_code=400, detail="No file uploaded")

        file_bytes = await file.read()
        if file_bytes is None:
            raise HTTPException(status_code=400, detail="File content is None")

        file_route = path + file.filename
        s3.put_object(
            Bucket=os.getenv("DIGITAL_OCEAN_BUCKET"),
            Key=file_route,
            Body=file_bytes,
            ACL='public-read',
            ContentType=file.content_type,
        )

        response = s3.head_object(Bucket=os.getenv("DIGITAL_OCEAN_BUCKET"), Key=file_route)

        metadata = {
            'Key': file_route,
            'LastModified': response['LastModified'],
            'ETag': response['ETag'],
            'Size': response['ContentLength'],
            'StorageClass': response.get('StorageClass', 'STANDARD')  # Default to 'STANDARD' if not specified
        }

        logger.info(f"File: {metadata}")
        return metadata

    except NoCredentialsError as e:
        logger.error(f"Credentials not provided or incorrect: {e}")


@router.post("/create_folder/{folder:path}")
async def create_folder(folder: str):
    s3.put_object(
        Bucket=os.getenv("DIGITAL_OCEAN_BUCKET"),
        Key=f"{folder}/",
        ACL='public-read',
        ContentType="application/json",
    )
    return {"message": f"Folder {folder} created"}


@router.delete("/{file_id}")
async def delete_file_data(file_id: int, db: Session = Depends(get_db)):
    file = db.query(FileDO).filter(FileDO.id == file_id).first()
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")

    db.delete(file)
    db.commit()
    return {"message": "File deleted"}


@router.delete("/remove_file/{filename:path}")
async def remove_file(filename: str):
    bucket_name = os.getenv("DIGITAL_OCEAN_BUCKET")
    if bucket_name is None:
        print("El nombre del bucket es None")
    else:
        print(f"El nombre del bucket es: {bucket_name}")

    try:
        response = s3.delete_object(Bucket=bucket_name, Key=filename)
        return {"message": "File deleted successfully", "response": response}
    except Exception as e:
        print(f"Error deleting file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/remove_folder/{folder:path}")
async def delete_folder(folder: str):
    logger.info(f"Deleting folder: {folder}")
    objects_to_delete = s3.list_objects_v2(Bucket=os.getenv("DIGITAL_OCEAN_BUCKET"), Prefix=folder)
    if 'Contents' in objects_to_delete:
        for obj in objects_to_delete['Contents']:
            print(f"Deleting {obj['Key']}")
            s3.delete_object(Bucket=os.getenv("DIGITAL_OCEAN_BUCKET"), Key=obj['Key'])

    return {"message": f"Folder {folder} deleted"}
