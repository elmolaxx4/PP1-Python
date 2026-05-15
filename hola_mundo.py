"""
from fastapi import FastAPI

app = FastAPI()

app.title = "Mi primera API"

@app.get("/saludo")  
async def saludo():
    return {"hola": "mundo"}


@app.put("/saludo/put")
async def actualizar_saludo():
    return {"mensaje": "put"}


@app.post("/saludo/post")
async def agregar_saludo():
    return {"mensaje": "post"}


@app.delete("/saludo/delete")
async def delete_saludo():
    return {"mensaje": "delete"}
"""
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Path
from typing import Annotated

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.title = "Mi primera API"
app.version = "0.1"

# Request -> Middleware -> Path Operation -> Middleware -> Response

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["https...", 
    "https://dominio.com"
    '*',
    ],
    allow_credent = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# =========================
# RESPUESTA 404
# =========================

dict_not_found = {
    404: {
        "description": "Si el videojuego no se encuentra en la lista",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Videojuego no encontrado"
                }
            }
        },
    }
}


# =========================
# TIPOS PERSONALIZADOS
# =========================

INT_POSITIVO = Annotated[int, Field(gt=0)]

STR_CORTITO = Annotated[str, Field(max_length=30)]

FLOAT_PRECIO = Annotated[float, Field(gt=1000, lt=999999)]

BOOL_ACTIVO = Annotated[
    bool,
    Field(description="Sigue disponible")
]


# =========================
# ESQUEMAS
# =========================

class VideojuegoSchema(BaseModel):
    id: INT_POSITIVO
    nombre: STR_CORTITO
    precio: FLOAT_PRECIO = 1000
    activo: BOOL_ACTIVO = True


class VideojuegoUpdateSchema(BaseModel):
    nombre: STR_CORTITO
    precio: FLOAT_PRECIO = 1000
    activo: BOOL_ACTIVO = True


# =========================
# BASE DE DATOS
# =========================

videojuegos = [
    {"id": 1, "nombre": "Minecraft", "precio": 15000, "activo": True},
    {"id": 2, "nombre": "GTA V", "precio": 25000, "activo": True},
    {"id": 3, "nombre": "FIFA 25", "precio": 30000, "activo": True}
]


# =========================
# GET - TODOS LOS JUEGOS
# =========================

@app.get(
    "/videojuegos",
    response_model=list[VideojuegoSchema]
)
async def get_videojuegos():
    return videojuegos


# =========================
# GET - JUEGO POR ID
# =========================

@app.get(
    "/videojuegos/{id}",
    responses=dict_not_found,
    response_model=VideojuegoSchema,
)
async def get_videojuego_id(
    id: Annotated[
        int,
        Path(gt=0, description="ID del videojuego")
    ],
):

    for videojuego in videojuegos:

        if videojuego["id"] == id:
            return videojuego

    raise HTTPException(
        status_code=404,
        detail="Videojuego no encontrado"
    )


# =========================
# POST - CREAR JUEGO
# =========================

@app.post(
    "/videojuegos",
    response_model=VideojuegoSchema,
)
async def crear_videojuego(videojuego: VideojuegoSchema):

    videojuegos.append(videojuego.model_dump())

    return videojuego


# =========================
# PUT - EDITAR JUEGO
# =========================

@app.put(
    "/videojuegos/{id}",
    responses=dict_not_found,
    response_model=VideojuegoSchema,
)
async def editar_videojuego(
    id: int,
    videojuego_editado: VideojuegoUpdateSchema
):

    for videojuego in videojuegos:

        if videojuego["id"] == id:

            videojuego["nombre"] = videojuego_editado.nombre
            videojuego["precio"] = videojuego_editado.precio
            videojuego["activo"] = videojuego_editado.activo

            return videojuego

    raise HTTPException(
        status_code=404,
        detail="Videojuego no encontrado"
    )


# =========================
# DELETE - ELIMINAR JUEGO
# =========================

@app.delete(
    "/videojuegos/{id}",
    responses=dict_not_found,
    response_model=dict
)
async def delete_videojuego(id: int):

    for videojuego in videojuegos:

        if videojuego["id"] == id:

            videojuegos.remove(videojuego)

            return {
                "mensaje": "Videojuego eliminado"
            }

    raise HTTPException(
        status_code=404,
        detail="Videojuego no encontrado"
    )