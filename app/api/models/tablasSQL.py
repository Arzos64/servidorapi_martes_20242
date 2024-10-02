#Modelos

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base 

#Llamado a la base para crear tablas

Base = declarative_base ()

#Definición de las tablas de mi modelo

#usuario
class Usuario(Base):
    __tablename__= 'usuarios'
    id = Column(Integer,primary_key = True, autoincrement = True)
    nombres = Column(String(50))
    fechaNacimiento = Column(Date)
    ubicacion = Column(String(100))
    metaAhorro = Column(Float)
    

