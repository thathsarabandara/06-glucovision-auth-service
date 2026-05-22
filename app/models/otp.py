from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.database import Base

class OTPVerification(Base):
    __tablename__ = "otp_verifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    verification_token = Column(String(255), unique=True, index=True, nullable=False)
    hashed_otp = Column(String(255), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    retry_count = Column(Integer, default=0)
    resend_count = Column(Integer, default=0)
