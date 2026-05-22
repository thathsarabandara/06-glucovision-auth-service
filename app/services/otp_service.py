import secrets
import string
import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.otp import OTPVerification
from app.core.config import settings
from app.core.security import get_password_hash, verify_password

class OTPService:
    @staticmethod
    def generate_otp(length: int = 6) -> str:
        """Generate a random numeric OTP."""
        return ''.join(secrets.choice(string.digits) for _ in range(length))

    @staticmethod
    async def create_otp_verification(db: AsyncSession, user_id: int) -> tuple[str, str]:
        """Creates an OTP verification record and returns the plain OTP and verification token."""
        otp_plain = OTPService.generate_otp()
        hashed_otp = get_password_hash(otp_plain)
        verification_token = str(uuid.uuid4())
        
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
        
        # Check if an existing unverified OTP exists and delete it
        result = await db.execute(select(OTPVerification).where(OTPVerification.user_id == user_id))
        existing_otp = result.scalars().first()
        if existing_otp:
            await db.delete(existing_otp)

        otp_record = OTPVerification(
            user_id=user_id,
            verification_token=verification_token,
            hashed_otp=hashed_otp,
            expires_at=expires_at
        )
        db.add(otp_record)
        await db.commit()
        
        return otp_plain, verification_token

    @staticmethod
    async def verify_otp(db: AsyncSession, verification_token: str, otp: str) -> bool:
        """Verifies an OTP against a verification_token."""
        result = await db.execute(select(OTPVerification).where(OTPVerification.verification_token == verification_token))
        otp_record = result.scalars().first()
        
        if not otp_record:
            return False

        if datetime.now(timezone.utc) > otp_record.expires_at.replace(tzinfo=timezone.utc):
            return False
            
        if otp_record.retry_count >= settings.MAX_OTP_RETRIES:
            return False

        is_valid = verify_password(otp, otp_record.hashed_otp)
        
        if not is_valid:
            otp_record.retry_count += 1
            await db.commit()
            return False
            
        # Clean up verified OTP
        await db.delete(otp_record)
        await db.commit()
        
        return True
