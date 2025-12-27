from jose import jwt, JWTError
from fastapi import Depends, FastAPI, HTTPException, status,APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from utils  import verify_password,hash_password
from datetime import datetime, timedelta, timezone
from crud.user import get_user_by_username
from schemas.user import  UserResponse , Token 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import get_db
import os 
from models.user import User

from crud.user import (
  get_user_by_id,
)
auth_router= APIRouter(
  prefix = "/auth",
  tags=["Auth"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM","HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",30))


def authenticate_user(db:Session , username:str, password:str):
  users = get_user_by_username(db, username)
  for user in users:
    if  verify_password(password, user.hashed_password):
      return user
  return False

def create_access_token(data:dict,expires_delta:timedelta|None =None ):
  to_encode= data.copy()
  if expires_delta:
    expire= datetime.utcnow()+expires_delta
  else :
    expire= datetime.utcnow()+timedelta(minutes=15)
  to_encode.update({"exp":expire})
  encoded_jwt=jwt.encode(to_encode , SECRET_KEY, algorithm=ALGORITHM )
  return encoded_jwt

def get_current_user(token : Annotated[str,Depends(oauth2_scheme)],db:Session=Depends(get_db)):
  credential_exception= HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )
  try :
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id= payload.get("user_id")
    if user_id is None:
      raise credential_exception
  except JWTError:
    raise credential_exception
  user= get_user_by_id(db,user_id)
  if not user:
    raise credential_exception
  return user


def get_current_active_user(current_user:Annotated[User, Depends(get_current_user)]):
  if getattr(current_user,"disabled",False):
    raise HTTPException(status_code=400, detail="Not Authorized")
  return current_user


@auth_router.post("/token")
async def login_for_access_token(
  form_data:Annotated[OAuth2PasswordRequestForm,Depends()],
  db:Session=Depends(get_db)
):
  user= authenticate_user(db,form_data.username, form_data.password)
  if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
  access_token_expires=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token= create_access_token(data={"user_id":user.id},
  expires_delta=access_token_expires
  )
  return Token(access_token=access_token, token_type="bearer")



@auth_router.get("/me")
async def get_me(current_user:Annotated[User,Depends(get_current_active_user)]):
  return current_user

@auth_router.get("/debug-token")
async def get_token(token:Annotated[str | None ,Depends(oauth2_scheme)]):
  return {"token":token}

