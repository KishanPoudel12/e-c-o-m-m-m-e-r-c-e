from schemas.user import UserCreate, UserUpdate, UserResponse 
from database import get_db
from sqlalchemy.orm import Session
from models.user import User
from utils import hash_password
def get_user_by_id(db:Session,user_id:int):
  return db.query(User).filter(User.id ==user_id).first()

def get_user_by_username(db:Session,username:str):
  return db.query(User).filter(User.username == username).all()

def get_users(db:Session):
  return db.query(User).all()

def create_user(db:Session ,data:UserCreate):
  plain_password= data.password
  hashed_password= hash_password(plain_password)
  user_data= User(**data.model_dump(exclude={"password"}),hashed_password=hashed_password)
  db.add(user_data)
  db.commit()
  db.refresh(user_data)
  return user_data


def update_user(db:Session,user_id:int, data:UserUpdate):
  user_to_update= get_user_by_id(db, user_id)
  if not user_to_update:
    return None 
  update_user= data.model_dump(exclude_unset=True)
  if "password" in update_user:
    updated_password= update_user.pop("password")
    hashed_updated_password= hash_password(updated_password)
    setattr(user_to_update, "hashed_password",hashed_updated_password )

  for key, value in update_user.items():
    setattr(user_to_update,key ,value)
  db.commit()
  db.refresh(user_to_update)
  return user_to_update


def delete_user(db:Session, user_id:int):
  user_to_delete= get_user_by_id(db, user_id)
  if not user_to_delete:
    return None 
  db.delete(user_to_delete)
  db.commit()
  return user_to_delete

