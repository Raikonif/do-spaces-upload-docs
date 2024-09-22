# import os
#
# from botocore.exceptions import NoCredentialsError
# from sqlalchemy.orm import Session
#
# from app.models import FileDO
# from main import app, s3_client, logger
# from database import get_db
# from fastapi import Depends, UploadFile, HTTPException, File
#
#
# @app.get("/files/")
# async def read_files(db: Session = Depends(get_db)):
#     files = db.query(FileDO).all()
#     return files | []
#
#
# @app.post("/files/")
# async def create_file(file_name: str, file_url: str, db: Session = Depends(get_db)):
#     file = FileDO(name=file_name, url=file_url)
#     db.add(file)
#     db.commit()
#     db.refresh(file)
#     return file
#
#
# @app.post("/upload/")
# async def upload_image(file: UploadFile = File(...)):
#     try:
#         if file is None:
#             raise HTTPException(status_code=400, detail="No file uploaded")
#
#         file_bytes = await file.read()
#         if file_bytes is None:
#             raise HTTPException(status_code=400, detail="File content is None")
#
#         filename = file.filename
#         s3_client.put_object(
#             Bucket=os.getenv("DIGITAL_OCEAN_BUCKET"),
#             Key=filename,
#             Body=file_bytes,
#             ACL='public-read',
#             ContentType=file.content_type,
#         )
#         file_url = f"{os.getenv('DIGITAL_OCEAN_ORIGIN')}/{os.getenv('DIGITAL_OCEAN_BUCKET')}/{filename}"
#         logger.info(f"File URL: {file_url}")
#         return {"imageUrl": file_url}
#
#     except NoCredentialsError as e:
#         logger.error(f"Credentials not provided or incorrect: {e}")
#
#
# @app.post("/delete/")
# async def delete_image(file_name: str):
#     try:
#         if file_name is None:
#             raise HTTPException(status_code=400, detail="No file name provided")
#
#         s3_client.delete_object(
#             Bucket=os.getenv("DIGITAL_OCEAN_BUCKET"),
#             Key=file_name,
#         )
#         return {"message": f"File {file_name} deleted"}
#
#     except NoCredentialsError as e:
#         logger.error(f"Credentials not provided or incorrect: {e}")
