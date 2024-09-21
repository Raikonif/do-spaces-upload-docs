import logging
import os

import boto3.session
from botocore.exceptions import NoCredentialsError
from fastapi import FastAPI, HTTPException, UploadFile, File
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import file

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(file.router)

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
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "https://store-all-do.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == '__main__':
    import uvicorn

    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
