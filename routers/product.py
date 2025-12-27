from fastapi import APIRouter, HTTPException,Depends
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
from auth import get_current_user,get_current_active_user

product_router=APIRouter(
  prefix="/product",
  tags=["Products"]
#   dependencies=[Depends(get_current_active_user)] => could have done this too but currently require in individual route
)


@product_router.get("/", response_model=list[ProductResponse])
async def read_products(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    products = get_products(db)
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products


@product_router.get("/{product_id}", response_model=ProductResponse)
async def read_single_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@product_router.post("/create", response_model=ProductResponse)
async def create_new_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    product = create_product(db, data,current_user)
    if not product:
        raise HTTPException(status_code=400, detail="Product creation failed")
    return product


@product_router.put("/{product_id}", response_model=ProductResponse)
async def update_existing_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    updated_product = update_product(db, product_id, data)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@product_router.delete("/{product_id}", response_model=ProductResponse)
async def delete_existing_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    deleted_product = delete_product(db, product_id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return deleted_product