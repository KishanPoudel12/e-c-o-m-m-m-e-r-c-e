from pydantic import BaseModel,Field,validator
from typing import Optional
from decimal import Decimal

class ProductBase(BaseModel):
  product_name:str 
  product_description:Optional[str]=None
  price:Decimal = Field(None,gt=0) 
  image_path:Optional[str]=None
  stock:int =Field(ge=0)
  
  @validator("price",pre=True)
  def format_price(cls,v):
    return round(Decimal(v),2)

class ProductCreate(ProductBase):
  pass 

class ProductUpdate(BaseModel):
  product_name: Optional[str] = None
  product_description: Optional[str] = None
  price: Optional[Decimal] = Field(None,gt=0)
  image_path: Optional[str] = None
  stock:  Optional[int] = Field(None,gt=0)

class ProductResponse(ProductBase):
  id:int
  owner_id:int
  model_config = {
        "from_attributes": True  
    }


class UserProductResponse(ProductBase):
  id:int
  model_config = {
        "from_attributes": True  
    }
