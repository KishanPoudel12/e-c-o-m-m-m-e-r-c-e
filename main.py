from fastapi import FastAPI
from database import create_db
from auth import auth_router
from routers.user import user_router
from routers.product import product_router
from routers.order import order_router
import models  # load all models before creating tables

app = FastAPI(title="Emart")


@app.on_event("startup")
def startup():
    return create_db()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(auth_router)
