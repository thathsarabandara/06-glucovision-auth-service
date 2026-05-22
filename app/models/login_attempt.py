from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.database import Base

class LoginAttempt(Base):
    __tablename__ = "login_attempts"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), index=True, nullable=False)
    ip_address = Column(String(50))
    status = Column(String(20), nullable=False) # e.g., "success", "failed"
    attempted_at = Column(DateTime(timezone=True), server_default=func.now())
