from fastapi import APIRouter, HTTPException,Depends,UploadFile,Form
from sqlalchemy.orm import Session
from crud.product import (
  get_product_by_id,
  get_products,
  create_product,
  update_product,
  delete_product
)

from schemas.product import ProductBase, ProductCreate, ProductUpdate, ProductResponse
from database import get_db
from auth import get_current_user,get_current_active_user, require_role
from models.user import User
from models.product import Product
from cloudinary_utils import upload_image
from utils import pagination

product_router=APIRouter(
  prefix="/product",
  tags=["Products"]
#   dependencies=[Depends(get_current_active_user)] => could have done this too but currently require in individual route
)


@product_router.get("/",response_model=list[ProductResponse])
async def list_product(
    db:Session=Depends(get_db),
    current_user=Depends(get_current_active_user),
    skip:int =0,
    limit:int=0
):
    query= db.query(Product).filter(Product.is_delete!=True,Product.owner_id!= current_user.id)
    return pagination(query,skip, limit )

@product_router.get("/{product_id}",response_model=ProductResponse)
async def list_product_by_id(
    product_id:int,
    db:Session=Depends(get_db)
):
  return db.query(Product).filter(Product.id==product_id,Product.is_delete!=True).first()


@product_router.get("/admin/", response_model=list[ProductResponse])
async def read_my_products(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    admin:User=Depends(require_role("admin")),
    skip:int =0,
    limit:int=0
):
    query = db.query(Product).filter(Product.is_delete==False,
        Product.owner_id==current_user.id
    )
    return pagination(query,skip, limit )



@product_router.get("/{product_id}/admin/", response_model=ProductResponse)
async def read_my_single_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    admin:User=Depends(require_role("admin"))

):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not Your Product")
    return product


@product_router.post("/create", response_model=ProductResponse)
async def create_my_new_product(
    product_name:str =Form(...),
    product_description:str=Form(...),
    price:float=Form(...),
    stock:int =Form(...),
    image:UploadFile=None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    admin:User=Depends(require_role("admin"))
):
    try:
        image_url = await upload_image(image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    product_create=ProductCreate(
        product_name=product_name,
        product_description=product_description,
        price=price,
        stock=stock
    )

    if not product_create:
        raise HTTPException(status_code=400, detail="Product creation failed")

    product = create_product(
        db=db,
        data=product_create,
        current_user=current_user,
        image_path=image_url
    )
    return product


@product_router.put("/{product_id}", response_model=ProductResponse)
async def update_my_existing_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    admin:User=Depends(require_role("admin"))

):
    updated_product = update_product(db, product_id, data,current_user.id)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@product_router.delete("/{product_id}", response_model=ProductResponse)
async def delete_my_existing_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    admin:User=Depends(require_role("admin"))

):
    deleted_product = delete_product(db, product_id,current_user.id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return deleted_product