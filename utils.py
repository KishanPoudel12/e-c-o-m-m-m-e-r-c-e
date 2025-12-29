from passlib.context import CryptContext
from fastapi import Query


pwd_context= CryptContext(schemes=["bcrypt"],deprecated="auto")
def hash_password(plain_password:str):
    return pwd_context.hash(plain_password)

def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)



#pagination 

def pagination(query, skip:int=Query(0,ge=0) , limit:int=Query(0,ge=1)):
    return query.offset(skip).limit(limit).all()

