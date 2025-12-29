from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(os.getenv("SQLALCHEMY_DATABASE_URL"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_db():
    try:
        import models.user
        import models.product
        import models.order
        import models.order_Item
        import models.payment
        import models.otp
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully (or already exist).")
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")