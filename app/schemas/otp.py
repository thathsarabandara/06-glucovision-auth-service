from pydantic import BaseModel

class OTPVerificationRequest(BaseModel):
    verification_token: str
    otp: str

class OTPResendRequest(BaseModel):
    verification_token: str

class OTPResponse(BaseModel):
    verification_token: str
    message: str
