from sqlalchemy import Column, Integer, String
from database import Base

class services(Base):
    # Nombre de la tabla
    __tablename__ = "Servicios"

    # Columnas de la tabla
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String(250), nullable=False)