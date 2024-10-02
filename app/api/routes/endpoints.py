from fastapi import APIRouter, HTTPException #Librería para los servicios que necesito en la base de datos (Actualizar, Guardar, etc)
from sqlalchemy.orm import Session #Comunicación con la base de datos.
from typing import List
from fastapi.params import Depends #Utilizar dependencias del api para comunicación interna.
from app.api.DTO.dtos import UsuarioDTOPeticion, UsuarioDTORespuesta
from app.api.models.tablasSQL import Usuario
from app.database.configuration import SessionLocal,engine

rutas = APIRouter()

def conectarConBD():
    try:
        basedatos = SessionLocal()
        yield basedatos #Activar la base de datos
           
    except Exception as error:
        basedatos.rollback()
        raise error
    finally:
        basedatos.close()



#construyendo nuestros servicios.


#cada servivio (operacion o transacion) debe programarse como una funcion

@rutas.post("/usuario", response_model=Usuario, summary="Registrar un usuario en la base de datos") #NOMBRAR DENTRO DEL API UN ENDPOINT que aparece en la url 

def guardarUsuario (datosUsuario:UsuarioDTOPeticion, database:Session=Depends(conectarConBD)): # esto es para pasar y hablar con la base de datos
    try:
        usuario=Usuario(
            nombres=datosUsuario.nombres,
            fechaNacimiento=datosUsuario.fechaNacimiento,
            ubicacion=datosUsuario.ubicacion,
            metaAhorro=datosUsuario.metaAhorro
        )# aqui lo que hace es decirle que si estos datos son iguales al modelo (tablasSQL) entonces que si los guarde

        #ordenarle a la bd
        database.add(usuario) #una vez estan los tipos de datos que se puede guardar entonces aqui guarda en la base de datos
        database.commit() # toma foto para lo que acaba de hacer
        database.refresh()#refresque la base de datos
        return usuario #devuelve el usuario osea la variable


    except Exception as error:
        database.rollback()#si falla digale a la base de datos que no haga nada
        raise HTTPException(status_code=400, detail=f"TENEMOS UN PROBLEMA{error}") #si falla la operacion manda 400


@rutas.get("/usuario", response_model=List[UsuarioDTORespuesta], summary=("buscar una datos en la base de datos"))

def buscarUsuarios(database:Session=Depends(conectarConBD)): #conexion con la base de datos
    try:
        usuarios=database.query().all()#haciendo la consulta en la tabla usuario
        return usuarios

    except Exception as error:
     database.rollback()#si falla digale a la base de datos que no haga nada
     raise HTTPException(status_code=400, detail=f"TENEMOS UN PROBLEMA{error}") #si falla la operacion manda 400