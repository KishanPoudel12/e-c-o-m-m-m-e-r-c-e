from pydantic import BaseModel
from typing import Optional

class PaymentBase(BaseModel):
  order_id:int 
  amount:int 
  status:Optional[str]=None
  stripe_session_id:str


class PaymentCreate(PaymentBase):
  pass

class PaymentUpdate(BaseModel):
  order_id:Optional[int] =None
  amount:Optional[int] =None
  status:Optional[str]=None
  stripe_session_id:Optional[str]=None 

  
class PaymentResponse(PaymentBase):
  id:int 
  order_id:int 
  amount:int 
  status:Optional[str]=None
  stripe_session_id:str
  model_config = {
        "from_attributes": True  
    }