from pydantic import BaseModel
from typing import Optional
from decimal import Decimal 
from sqlalchemy import Numeric
'''
user_id
order_id
product_id
quantity
status

'''

#order Item 
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(BaseModel):
    product_id: int
    unit_price: Decimal
    quantity: int
    product_name:str
    total_price: Decimal
    model_config = {"from_attributes": True}

#order

class OrderCreate(BaseModel):
  items:list[OrderItemCreate]

class OrderUpdate(BaseModel):
  status:Optional[str]=None
  items:Optional[list[OrderItemCreate]]


class OrderResponse(BaseModel):
  id:int
  owner_id:int
  total_order_quantity:Optional[int]=None 
  status:str
  total_order_price:Optional[Decimal]=Numeric(10,2)
  items:list[OrderItemResponse]
  model_config = {
        "from_attributes": True  
    }





