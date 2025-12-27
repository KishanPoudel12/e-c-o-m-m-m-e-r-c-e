from schemas.order import OrderCreate, OrderUpdate, OrderResponse
from database import get_db
from sqlalchemy.orm import Session
from models.order import Order
from models.user import User
from crud.product import get_product_by_id
from decimal import Decimal
from fastapi import HTTPException ,Depends
from sqlalchemy.exc import SQLAlchemyError
from models.order_Item import OrderItem
from models.order import OrderStatus
from auth import get_current_active_user,get_current_user


def get_orders(db: Session, current_user: User):
    return db.query(Order).filter(
        Order.is_delete == False,
        Order.owner_id == current_user.id
    ).all()

def get_order_by_id(db: Session, order_id: int, current_user: User):
    return db.query(Order).filter(
        Order.id == order_id,
        Order.is_delete == False,
        Order.owner_id == current_user.id
    ).first()


def calculate_order_total(order:Order):
    if not order:
        raise HTTPException(status_code=400 , detail="No Order Found")
    total_order_price = Decimal("0.00")
    total_order_quantity=0

    for item in order.items:
        total_order_price+=Decimal(item.total_price)
        total_order_quantity+=item.quantity
    
    order.total_order_price=total_order_price
    order.total_order_quantity=total_order_quantity

        
def create_order(db: Session, data: OrderCreate, current_user: User):
    try:
        new_created_order=Order(owner_id=current_user.id, status="pending", total_order_price=Decimal("0.00"))
        db.add(new_created_order)
        db.flush()  #gets order id without commiting 
        # db.refresh(new_created_order)

        for item in data.items:
            product= get_product_by_id(db,item.product_id)
            if not product:
                raise HTTPException(status_code=400, detail=f"{item.product_id}  does not Exist")   
            if product.owner_id==current_user:
                raise HTTPException(status_code=400, detail="Cannot Order Your Own Product ")
            if product.stock < item.quantity:
                raise HTTPException(status_code=400, detail=f" Only {product.stock } unit stocks left , Cant Order {item.quantity } units ")

            item_total = item.quantity*Decimal(product.price)
            product.stock-= item.quantity

            order_item=OrderItem(
                order_id= new_created_order.id,
                product_id = item.product_id,
                product_name= product.product_name,
                quantity=item.quantity,
                unit_price=product.price ,
                total_price=item_total
            )
            new_created_order.items.append(order_item)
            db.add(order_item)

        calculate_order_total(new_created_order)
        db.commit()
        db.refresh(new_created_order)
        return new_created_order
    except SQLAlchemyError as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500,detail="Failed to create Order" )

def update_order(db: Session, order_id: int, data: OrderUpdate,current_user:User):
    try:
        order_to_update= get_order_by_id(db, order_id,current_user)
        if not order_to_update:
            raise HTTPException(status_code=400, detail="Order Not Found")
        if order_to_update.status!= OrderStatus.pending:
            raise HTTPException(status_code=400, detail="Processed Order Cannot be Updated")
        if data.status:
            order_to_update.status = data.status
        if data.items:
            for item in data.items:
                order_item = db.query(OrderItem).filter(OrderItem.order_id == order_id, OrderItem.product_id==item.product_id).first()
                if not order_item:
                    raise HTTPException(status_code=400, detail=f"Product  {item.product_id} Not Found")

                product=order_item.product

                diff_quantity= item.quantity- order_item.quantity
                if diff_quantity > 0 and product.stock < diff_quantity:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Not enough stock for {product.product_name}. Available: {product.stock}"
                    )
                product.stock-= diff_quantity

                order_item.quantity= item.quantity
                order_item.total_price= order_item.quantity*Decimal(order_item.unit_price)
            
        calculate_order_total(order_to_update)
        db.commit()
        db.refresh(order_to_update)
        return order_to_update
    except SQLAlchemyError as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500,detail="Failed to create Order")
        
        
 
def soft_delete_order(db:Session, order_id:int,current_user:User):
    try:
        order_to_delete = get_order_by_id(db, order_id,current_user)
        if not order_to_delete:
            raise HTTPException(status_code=404, detail="Order not found")
        for item in order_to_delete.items:
            item.product.stock+=item.quantity
        
        order_to_delete.is_delete=True
        db.commit()
        return order_to_delete
    except SQLAlchemyError as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500,detail="Failed to SoftDelete Order")


def hard_delete_order(db: Session, order_id: int,current_user:User):
    try:
        order_to_delete = get_order_by_id(db, order_id,current_user)
        if not order_to_delete:
            raise HTTPException(status_code=404, detail="Order not found")

        for item in order_to_delete.items:
            item.product.stock+=item.quantity

        db.delete(order_to_delete)
        db.commit()
        return order_to_delete
    except SQLAlchemyError as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500,detail="Failed to SoftDelete Order")