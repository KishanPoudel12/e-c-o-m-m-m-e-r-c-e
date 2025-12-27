from schemas.product import ProductCreate, ProductUpdate, ProductResponse 
from database import get_db
from sqlalchemy.orm import Session
from models.product import Product
from models.user import User

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

def update_product(db:Session , product_id:int , data:ProductUpdate):
  product_to_update=get_product_by_id(db, product_id)
  if not product_to_update:
    return None
  updated_product = data.model_dump(exclude_unset=True)
  for key , value in updated_product.items():
    setattr(product_to_update, key , value)
  db.commit()
  db.refresh(product_to_update)
  return product_to_update

def soft_delete_products(db:Session , product_id:int):
  product_to_delete = get_product_by_id(db, product_id)
  if not product_to_delete:
    return None 
  product_to_delete.is_delete=True
  db.commit()
  return product_to_delete


def delete_product(db:Session , product_id:int ):
  product_to_delete= get_product_by_id(db, product_id)
  if not product_to_delete:
    return None 
  db.delete(product_to_delete)
  db.commit()
  return product_to_delete



  

  