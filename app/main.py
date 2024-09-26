import os

from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.helpers.redirect_path import folder_exists
from app.helpers.s3_client_do import s3_client
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

Base.metadata.create_all(bind=engine)


@app.get("/test")
async def test_route():
    bucket_name = "ncp-files"  # e.g., 'ncp-files'
    folder_name = "nandy-files"  # e.g., 'nandy-files'
    filename = "reportMatriculaPregrado.pdf"
    # Construct the full object path within the bucket
    file_path = f"{folder_name}/reportMatriculaPregrado.pdf"
    path = folder_exists()
    s3_client.download_file(folder_name, filename, f"{path}/{filename}")
    return "cors test"


app.include_router(file.router)

if __name__ == '__main__':
    import uvicorn

    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
