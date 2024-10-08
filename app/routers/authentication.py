# import os
#
# from app.helpers.auth_signal_client import authsignal_client
# from fastapi import HTTPException, Request, APIRouter
# from pydantic import BaseModel
# from fastapi.responses import JSONResponse
# from starlette.responses import RedirectResponse
# import jwt
# import requests
#
# router = APIRouter(prefix="/api/authenticate", tags=["authenticate"])
#
#
# class SignUpRequest(BaseModel):
#     email: str
#
#
# class LoginRequest(BaseModel):
#     token: str
#
#
# @router.post("/signup")
# async def signup(request: SignUpRequest):
#     email = request.email
#     if not email:
#         raise HTTPException(status_code=400, detail="Missing email parameter")
#
#     response = authsignal_client.track(
#         user_id=email,
#         action="signUp",
#         payload={
#             "email": email,
#             "user_id": email,
#             "redirectUrl": "https://localhost:8000/api/authenticate/callback"
#         }
#     )
#
#     return JSONResponse(content=response, status_code=200)
#
#
# @router.post('/login')
# def login(request: SignUpRequest):
#     email = request.email
#     if not email:
#         return HTTPException(status_code=400, detail="Missing email parameter")
#
#     response = authsignal_client.track(
#         user_id=email,
#         action="signIn",
#         payload={
#             "email": email,
#             "user_id": email,
#             "redirectUrl": "http://localhost:8000/api/authenticate/callback"
#         }
#     )
#     return JSONResponse(content=response, status_code=200)
#
#
# @router.post("/magic_link")
# async def magic_link(request: SignUpRequest):
#     email = request.email
#     if not email:
#         raise HTTPException(status_code=400, detail="Missing email parameter")
#
#     response = authsignal_client.track(
#         user_id=email,
#         action="magic_link",
#         payload={
#             "email": email,
#             "user_id": email,
#             "redirectUrl": "http://localhost:8000/api/authenticate/callback"
#         }
#     )
#
#     url = response["url"]
#     print(url)
#     # return RedirectResponse(url)
#     return JSONResponse(content=response, status_code=200)
#
#
# @router.post('/callback')
# def callback(request: LoginRequest):
#     token = request.token
#     if not token:
#         raise HTTPException(status_code=400, detail="Missing token parameter")
#
#     challenge_response = authsignal_client.validate_challenge(token)
#
#     if challenge_response["state"] == 'CHALLENGE_SUCCEEDED':
#         encoded_token = jwt.encode(
#             payload={"username": challenge_response["user_id"]},
#             key=os.getenv("AUTH_SIGNAL_SECRET_KEY"),
#             algorithm="HS256"
#         )
#         response = RedirectResponse('https://store-all-do.vercel.app/storage')
#         response.set_cookie(
#             key='auth-session',
#             value=encoded_token,
#             secure=False,
#             path='/'
#         )
#         return response
#
#     return RedirectResponse("/")
