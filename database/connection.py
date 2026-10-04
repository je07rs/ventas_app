from sqlalchemy import create_engine
from database.models import Base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    echo=True
)

Base.metadata.create_all(engine)

print("Tablas creadas correctamente")