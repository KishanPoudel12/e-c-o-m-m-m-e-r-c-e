from fastapi import FastAPI
from database import create_db
from auth import auth_router
from routers.user import user_router
from routers.product import product_router
from routers.order import order_router
from routers.payment import payment_router
from crud.otp import otp_router

import models  # load all models before creating tables

app = FastAPI(title="Emart")

@app.on_event("startup")
def startup():
    return create_db()

app.include_router(user_router)
app.include_router(product_router)
app.include_router(payment_router)
app.include_router(order_router)
app.include_router(otp_router)
app.include_router(auth_router)

