from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from crud.order import (
    get_order_by_id,
    get_orders,
    create_order,
    update_order,
    hard_delete_order,
    soft_delete_order
)
from schemas.order import OrderCreate, OrderUpdate, OrderResponse
from database import get_db
from auth import get_current_active_user
from models.user import User

order_router = APIRouter(
    prefix="/orders",
    tags=["My Orders"],
)

# Get all orders
@order_router.get("/", response_model=list[OrderResponse])
async def read_orders(
    db: Session = Depends(get_db),
    current_user:User=Depends(get_current_active_user)
):
    orders = get_orders(db,current_user)
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")
    return orders

# Get single order by ID
@order_router.get("/{order_id}", response_model=OrderResponse)
async def read_single_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    order = get_order_by_id(db, order_id,current_user)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Cannot Read Other's Order")
    return order

# Create new order
@order_router.post("/create", response_model=OrderResponse)
async def create_new_order(
    data: OrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    order = create_order(db, data, current_user)
    if not order:
        raise HTTPException(status_code=400, detail="Order creation failed")
    return order

# Update existing order
@order_router.put("/{order_id}", response_model=OrderResponse)
async def update_existing_order(
    order_id: int,
    data: OrderUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    updated_order = update_order(db, order_id, data,current_user)

    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")

    if updated_order.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Cannot Update Other's Order")

    return updated_order

# Delete order
@order_router.delete("/{order_id}", response_model=OrderResponse)
async def delete_existing_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    deleted_order = hard_delete_order(db, order_id,current_user)
    if not deleted_order:
        raise HTTPException(status_code=404, detail="Order not found")
    if deleted_order.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Cannot Delete Other's Order")
    return deleted_order
