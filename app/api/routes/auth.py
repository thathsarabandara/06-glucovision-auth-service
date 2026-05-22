from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api.dependencies import get_db, get_current_user
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.schemas.otp import OTPVerificationRequest, OTPResponse
from app.services.auth_service import AuthService
from app.services.otp_service import OTPService
from app.services.event_publisher import EventPublisher
from app.core.security import create_access_token, create_refresh_token
from app.models.user import User
from app.models.otp import OTPVerification

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user."""
    return await AuthService.register_user(db, user_in)

@router.post("/verify-otp", response_model=OTPResponse)
async def verify_otp(request: OTPVerificationRequest, db: AsyncSession = Depends(get_db)):
    """Verify OTP and activate user."""
    # First get the user id associated with the token to update the user
    result = await db.execute(select(OTPVerification).where(OTPVerification.verification_token == request.verification_token))
    otp_record = result.scalars().first()
    
    if not otp_record:
        raise HTTPException(status_code=400, detail="Invalid verification token")
        
    user_id = otp_record.user_id

    is_valid = await OTPService.verify_otp(db, request.verification_token, request.otp)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    # Update user status
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalars().first()
    if user:
        user.is_verified = True
        user.status = "active"
        await db.commit()
        await EventPublisher.publish("user_verified", {"user_id": user.id, "email": user.email})

    return {"verification_token": request.verification_token, "message": "Account verified successfully"}

@router.post("/login", response_model=Token)
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """OAuth2 compatible token login, get an access token for future requests."""
    ip_address = request.client.host if request.client else None
    user = await AuthService.authenticate_user(db, form_data.username, form_data.password, ip_address)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)
    
    # Normally we would save the refresh token to DB here
    
    await EventPublisher.publish("login_success", {"user_id": user.id, "email": user.email})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
