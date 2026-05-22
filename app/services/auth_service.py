from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.models.user import User
from app.models.login_attempt import LoginAttempt
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password
from app.services.otp_service import OTPService
from app.services.event_publisher import EventPublisher

class AuthService:
    @staticmethod
    async def register_user(db: AsyncSession, user_in: UserCreate) -> dict:
        # Check if user exists
        result = await db.execute(select(User).where(User.email == user_in.email))
        user = result.scalars().first()
        if user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        # Create user
        hashed_password = get_password_hash(user_in.password)
        new_user = User(
            email=user_in.email,
            password_hash=hashed_password,
            is_verified=False,
            status="pending_verification"
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        # Generate OTP and Verification Token
        otp_plain, verification_token = await OTPService.create_otp_verification(db, new_user.id)
        
        # Publish event
        await EventPublisher.publish("otp_requested", {"email": new_user.email, "otp": otp_plain})
        
        return {
            "message": "User registered successfully. Please verify your email.",
            "verification_token": verification_token
        }

    @staticmethod
    async def authenticate_user(db: AsyncSession, email: str, password: str, ip_address: str = None) -> User:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        
        if not user:
            await AuthService.log_attempt(db, email, ip_address, "failed_user_not_found")
            return None
            
        if not verify_password(password, user.password_hash):
            await AuthService.log_attempt(db, email, ip_address, "failed_wrong_password")
            return None
            
        if not user.is_verified:
            await AuthService.log_attempt(db, email, ip_address, "failed_unverified")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email not verified")

        await AuthService.log_attempt(db, email, ip_address, "success")
        return user

    @staticmethod
    async def log_attempt(db: AsyncSession, email: str, ip_address: str, attempt_status: str):
        attempt = LoginAttempt(
            email=email,
            ip_address=ip_address,
            status=attempt_status
        )
        db.add(attempt)
        await db.commit()
