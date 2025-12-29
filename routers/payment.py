from fastapi import APIRouter, HTTPException,Depends,UploadFile,Form
from schemas.payment import PaymentCreate, PaymentUpdate, PaymentResponse 
from auth import get_current_user,get_current_active_user, require_role
from sqlalchemy.orm import Session
from database import get_db
from crud.payment import create_payment , delete_payment
from models.payment import Payment 
from models.user import User

payment_router=APIRouter(
  prefix="/payment",
  tags=["Payment"]
)

@payment_router.get("/",response_model=list[PaymentResponse])
async def payment_list(db:Session=Depends(get_db),current_user:User=Depends(get_current_active_user)):
  return db.query(Payment).filter(Payment.payer==current_user.id).all()


@payment_router.post("/", response_model=PaymentResponse)
async def payment_create(
   data:PaymentCreate, 
   db:Session=Depends(get_db), 
   current_user:User=Depends(get_current_active_user),
 ):
    return create_payment(db, data, current_user)

@payment_router.delete("/{payment_id}",response_model=PaymentResponse)
async def payment_delete(
  payment_id:int,
  current_user:User=Depends(get_current_active_user),
  db:Session=Depends(get_db)
):
  return delete_payment(db,payment_id, current_user)