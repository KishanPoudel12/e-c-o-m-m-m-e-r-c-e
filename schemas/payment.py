from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class PaymentBase(BaseModel):
  order_id:int 
  amount: Decimal  
  transaction_id:str

class PaymentCreate(PaymentBase):
  pass

class PaymentUpdate(BaseModel):
  order_id:Optional[int] =None
  amount:Optional[Decimal] =None
  transaction_id:Optional[str]=None 


class PaymentResponse(PaymentBase):
  id:int 
  order_id:int 
  amount:Decimal 
  status:Optional[str]=None
  transaction_id:str
  model_config = {
        "from_attributes": True  
    }