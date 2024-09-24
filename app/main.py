import logging
import os

import boto3.session
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from app.database import Base, engine
from app.routers import file

app = FastAPI()

load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

# app.add_middleware(HTTPSRedirectMiddleware)

Base.metadata.create_all(bind=engine)


@app.get("/test")
async def test_route():
    return {f"{os.getenv("DIGITAL_OCEAN_BUCKET")}/{os.getenv("DIGITAL_OCEAN_FOLDER")}",}


app.include_router(file.router)

if __name__ == '__main__':
    import uvicorn

    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
