from fastapi import HTTPException,APIRouter,Depends
import random, smtplib , os
from schemas.otp import OTPRequest, OTPVerify
from datetime import datetime, timedelta
from models.otp import OTP
from sqlalchemy.orm import Session 
from utils import hash_password, verify_password
from database import get_db
from models.user import User
from dotenv import load_dotenv
from auth import create_access_token
load_dotenv()



SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

print(SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD)

otp_router=APIRouter(
  prefix="/otp",
  tags=["OTP"]
)

def generate_otp():
  return f"{random.randint(100000,999999)}"

def send_otp(email:str, otp:str):
  subject="Your OTP Code"
  body=f"Your OTP is :{otp} , It will Expire in 5 minutes"
  message=f"Subject :{subject}\n\n{body} "
  
  server =smtplib.SMTP(SMTP_HOST,SMTP_PORT)
  server.starttls()
  server.ehlo()                  # sometimes needed after starttls
  server.login(SMTP_USER,SMTP_PASSWORD)
  server.sendmail(SMTP_USER, email, message)
  server.quit()

def create_new_otp(db:Session, current_user:User):
  otp= generate_otp()
  hashed_otp=hash_password(otp)
  expires_time= datetime.utcnow()+timedelta(minutes=5)

  new_otp=OTP(user_id=current_user.id, otp_hash=hashed_otp, expires_at=expires_time )
  db.add(new_otp)
  db.commit()
  db.refresh(new_otp)
  return otp
  
@otp_router.post("/request")
def request_otp(data:OTPRequest,db:Session=Depends(get_db)):
  user= db.query(User).filter(User.email==data.email).first()
  if not user:
    raise HTTPException(status_code=403, detail="No User Found with this email")
  
  otp= create_new_otp(db, user)

  send_otp(data.email, otp)
  return {"message":f"OTP Sent to {data.email}"}



@otp_router.post("/verify")
def verify_otp(data:OTPVerify,db:Session=Depends(get_db)):
  user= db.query(User).filter(User.email== data.email).first()

  otp_in_db= db.query(OTP).filter(
    OTP.user_id==user.id
  ).order_by(OTP.created_at.desc()).first()

  if not otp_in_db:
    raise HTTPException(status_code=400, detail="OTP Not Found")
  
  if otp_in_db.expires_at<datetime.utcnow():
    raise HTTPException(status_code=400, detail="OTP Not Found")
  if not verify_password(data.otp, otp_in_db.otp_hash):
    raise HTTPException(status_code=400, detail="Invalid OTP")
  db.delete(otp_in_db)
  db.commit()
  access_token=create_access_token({"user_id":user.id})
  return {"token":access_token}

