from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False) # e.g., USER, ADMIN, DOCTOR, RESEARCHER
    description = Column(String(255))
