import os

from fastapi import FastAPI, APIRouter, Response
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import file, authentication, otp

app = FastAPI()
router = APIRouter()

@router.options("/api/files/download/{bucket_name}/{file_name}")
async def preflight_response():
    return Response(
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, PATCH, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://store-all-do.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(file.router)
app.include_router(router)
Base.metadata.create_all(bind=engine)



# app.include_router(authentication.router)
# app.include_router(otp.router)

if __name__ == '__main__':
    import uvicorn

    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
