# import authsignal
# from fastapi import FastAPI, HTTPException, Depends, APIRouter
# from pydantic import BaseModel
# import httpx
# import os
#
# from app.helpers.auth_signal_client import authsignal_client
#
# router = APIRouter(prefix="/api/otp", tags=["otp"])
#
# # Authsignal API configuration
# AUTHSIGNAL_API_URL = os.getenv("AUTH_SIGNAL_BASE_URL")
# AUTHSIGNAL_CLIENT_SECRET = os.getenv("AUTH_SIGNAL_SECRET_KEY")
#
#
# # Pydantic models for request data
# class OTPRequest(BaseModel):
#     user_id: str
#
#
# class OTPVerification(BaseModel):
#     user_id: str
#     code: str
#
#
# @router.post("/send_otp")
# def send_otp(email: str):
#     response = authsignal_client.track(
#         user_id=email,
#         action="email_otp",
#         payload={
#             "email": email,
#         }
#     )
#     print(response)
#     if response['state'] == "CHANGE_REQUIRED":
#         print("OTP sent to user's email.")
