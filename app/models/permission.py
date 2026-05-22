from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False) # e.g., view_analytics, manage_users
    description = Column(String(255))
