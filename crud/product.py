from schemas.product import ProductCreate, ProductUpdate, ProductResponse 
from database import get_db
from sqlalchemy.orm import Session
from models.product import Product
from models.user import User
from fastapi import HTTPException

def get_product_by_id(db:Session , product_id:int):
  return db.query(Product).filter(Product.id==product_id,Product.is_delete!=True).first()

def get_products(db:Session ):
  return db.query(Product).filter(Product.is_delete!=True).all()

def create_product(db:Session , data:ProductCreate,current_user:User):
  product_data= Product(**data.model_dump(),owner_id=current_user.id)
  db.add(product_data)
  db.commit()
  db.refresh(product_data)
  return product_data

def update_product(db:Session , product_id:int , data:ProductUpdate,current_user_id:int):
  product_to_update = db.query(Product).filter(
        Product.id == product_id,
        Product.owner_id == current_user_id
    ).first()
  if not product_to_update:
    raise HTTPException(status_code=404, detail="Product not found or not yours")


  updated_product = data.model_dump(exclude_unset=True)
  for key , value in updated_product.items():
    setattr(product_to_update, key , value)
  db.commit()
  db.refresh(product_to_update)
  return product_to_update

def soft_delete_products(db:Session , product_id:int,current_user_id:int):
  product_to_delete = db.query(Product).filter(
        Product.id == product_id,
        Product.owner_id == current_user_id
    ).first()
    
  if not product_to_delete:
    raise HTTPException(status_code=404, detail="Product not found or not yours")

  product_to_delete.is_delete=True
  db.commit()
  return product_to_delete


def delete_product(db:Session , product_id:int,current_user_id:int ):
  product_to_delete = db.query(Product).filter(
        Product.id == product_id,
        Product.owner_id == current_user_id
    ).first()
    
  if not product_to_delete:
    raise HTTPException(status_code=404, detail="Product not found or not yours")
  db.delete(product_to_delete)
  db.commit()
  return product_to_delete



  

  