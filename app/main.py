import logging
import os

import boto3.session
from botocore.exceptions import NoCredentialsError
from fastapi import FastAPI, HTTPException, UploadFile, File
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

session = boto3.session.Session()
s3_client = session.client(
    's3',
    region_name='nyc3',
    endpoint_url=os.getenv("DIGITAL_OCEAN_ORIGIN"),
    aws_access_key_id=os.getenv("DIGITAL_OCEAN_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("DIGITAL_OCEAN_SECRET_KEY")
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
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


@app.post("/delete/")
async def delete_image(file_name: str):
    try:
        if file_name is None:
            raise HTTPException(status_code=400, detail="No file name provided")

        s3_client.delete_object(
            Bucket=os.getenv("DIGITAL_OCEAN_BUCKET"),
            Key=file_name,
        )
        return {"message": f"File {file_name} deleted"}

    except NoCredentialsError as e:
        logger.error(f"Credentials not provided or incorrect: {e}")


if __name__ == '__main__':
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
