from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session
from crud.user import (
  get_user_by_id,
  get_user_by_username,
  get_users,
  create_user,
  update_user,delete_user,
  recharge_balance

)
from schemas.user import UserBase, UserCreate, UserUpdate, UserResponse
from database import get_db
from auth import get_current_user,get_current_active_user
from models.user import User

user_router= APIRouter(
  prefix="/user",
  tags=["User"],
)


@user_router.get("/recharge",response_model=dict)
async def recharge_user(amt:int, db:Session=Depends(get_db),current_user:User=Depends(get_current_active_user)
):
  return recharge_balance(db, amt, current_user)


@user_router.get("/",response_model=list[UserResponse])
async def read_users(db:Session=Depends(get_db),current_user:User=Depends(get_current_active_user)):
  users= get_users(db,current_user.id)
  if users is None:
    raise HTTPException(status_code=400, detail="No Users Found")
  return users 


@user_router.get("/{user_id}",response_model=UserResponse)
async def read_single_user( user_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_active_user)):
  user= get_user_by_id(db, user_id,current_user.id)
  if user is None :
    raise HTTPException(status_code=400, detail="User Does Not Exist")
  return user

@user_router.post("/create",response_model=UserResponse)
async def create_new_user( data:UserCreate,db:Session=Depends(get_db) ):
  user_data= create_user(db, data,"user")
  if  user_data is None:
    raise HTTPException(status_code=400, detail="User Creation Failed")
  return user_data


@user_router.post("/admin/create",response_model=UserResponse)
async def create_admin( data:UserCreate,db:Session=Depends(get_db) ):
  user_data= create_user(db, data,"admin")
  if  user_data is None:
    raise HTTPException(status_code=400, detail="User Creation Failed")
  return user_data


@user_router.put("/{user_id}",response_model=UserResponse)
async def update_existing_user(user_id:int,  data:UserUpdate,db:Session=Depends(get_db),current_user:User=Depends(get_current_active_user)):
  updating_user= update_user(db, user_id, data,current_user.id)
  if updating_user is None:
    raise HTTPException(status_code=400, detail="User Not Found")
  return updating_user

@user_router.delete("/{user_id}",response_model=UserResponse)
async def delete_existing_user(user_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_active_user)):
  deleting_user= delete_user(db, user_id,current_user.id)
  if deleting_user is None:
    raise HTTPException(status_code=400, detail="No User to Delete")
  return deleting_user



