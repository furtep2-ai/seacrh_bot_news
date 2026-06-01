import os
from sqlalchemy import create_engine, BigInteger, String, Boolean
import cryptography
from dotenv import load_dotenv
from sqlalchemy.orm import Session , sessionmaker, DeclarativeBase, Mapped, mapped_column
load_dotenv()

database_url = os.getenv("database_url")

engine = create_engine(database_url)

connection = engine.connect()

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_name: Mapped[str] = mapped_column(String(100),nullable=False)
    is_admin:Mapped[bool] = mapped_column(Boolean,default=False)

if __name__ == "__main__":
    print("Синхронизация с базой данных...")
    
    Base.metadata.create_all(engine)