from pydantic import BaseModel
from typing import Optional 
from .order import OrderResponse
class  UserBase(BaseModel):
  username:str
  email:str 
  password:str 

class UserCreate(UserBase):
  pass

class UserUpdate(BaseModel):
   username:Optional[str]=None
   email:Optional[str]=None
   password:Optional[str]=None

class UserResponse(BaseModel):
  id:int 
  username:str
  email:str 
  role:str
  disabled:bool
  orders:list[OrderResponse]=[]
  model_config = {
        "from_attributes": True  
    }


#jwt work 
class Token(BaseModel):
  access_token:str 
  token_type:str 

class TokenData(BaseModel):
  user_id:int |None =None
