from schemas.payment import PaymentCreate , PaymentUpdate, PaymentResponse 
from database import get_db
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.order import PaymentStatus
from models.order import Order
from models.payment import Payment
from models.user import User
from decimal import Decimal
from sqlalchemy import Enum


"""
order_id
pay_amount 
transaction_id

"""

def create_payment(db:Session , data:PaymentCreate,current_user:User):
  order_to_pay = db.query(Order).filter(Order.id==data.order_id,Order.owner_id==current_user.id).first()
  if not order_to_pay:
    raise HTTPException(status_code=400, detail="No Order to Pay For")
  
  if order_to_pay.payment_status==PaymentStatus.paid:
    raise HTTPException(status_code=400, detail="Payment already done ")

  if Decimal(current_user.balance) < Decimal(data.amount):
    raise HTTPException(status_code=400, detail="Insufficient amount")

  if Decimal(order_to_pay.total_order_price) != Decimal(data.amount):
    raise HTTPException(status_code=400, detail="Paying amount not equal to the payable amount")
  try:
    payment=Payment(
            order_id=order_to_pay.id, 
            amount= Decimal(data.amount), 
            status=PaymentStatus.paid,
            transaction_id=data.transaction_id,
            payer=current_user.id,
    )
    db.add(payment)
    current_user.balance-=order_to_pay.total_order_price
    order_to_pay.payment_status=PaymentStatus.paid
    db.commit()
    db.refresh(payment)
    return payment
  except Exception as e:
    print(e)
    db.rollback()
    raise HTTPException(
            status_code=500,
            detail="Payment processing failed"
        )


def delete_payment(db:Session , payment_id:int, current_user:User):
  try:
    payment_to_delete= db.query(Payment).filter(Payment.id==payment_id).first()
    if not payment_to_delete:
      raise HTTPException(status_code=400, detail="Payment does not Exist")
    
    if payment_to_delete.status != PaymentStatus.paid:
      raise HTTPException(status_code=400, detail="Only paid payments can be refunded")
    
    if payment_to_delete.status == PaymentStatus.withdrawn:
      raise HTTPException(status_code=400, detail="Payment already Withdrawn")
    
    order_of_payment= db.query(Order).filter(Order.id==payment_to_delete.order_id).first()
    if not order_of_payment:
      raise HTTPException(status_code=400, detail="Order does not Exist")
    
    payer= db.query(User).filter(User.id==payment_to_delete.payer).first()
    if not payer:
      raise HTTPException(status_code=400, detail="Payer not Found")
    if  (payer.id != current_user.id):
      raise HTTPException(status_code=400, detail="Unauthorized to cancel the payment")
    
    # db.delete(payment_to_delete)
    payment_to_delete.status=PaymentStatus.withdrawn
    order_of_payment.payment_status=PaymentStatus.withdrawn
    payer.balance+=payment_to_delete.amount

    db.commit()
    db.refresh(payment_to_delete)
    db.refresh(order_of_payment)
    db.refresh(payer)
    return payment_to_delete
  except Exception as e:
    print(e)
    db.rollback()
    raise HTTPException(
            status_code=500,
            detail="Payment processing failed"
        )

  

    