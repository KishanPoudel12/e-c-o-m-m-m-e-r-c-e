from database import Base
from sqlalchemy import Integer, String, DateTime, ForeignKey,Enum,Numeric,Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class OTP(Base):
  __tablename__="otps"
  id:Mapped[int]=mapped_column(primary_key=True)
  user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),index=True)
  otp_hash:Mapped[str]
  expires_at:Mapped[datetime]
  created_at:Mapped[datetime]= mapped_column(default=datetime.utcnow)