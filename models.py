from sqlalchemy import Column, Integer, String, BigInteger, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    username = Column(String, nullable=True)
    panel_type = Column(String, default="lucxui")
    subscription_url = Column(String, nullable=True)
    data_limit_gb = Column(Integer, default=0)
    expire_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
