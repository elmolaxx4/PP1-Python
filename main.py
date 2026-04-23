"""
from fastapi import FastAPI

app = FastAPI()

app.title = "Mi primera API"

# METODOS: GET POST PUT DELETE

articulos = [
    {"id":1, "nombre":"Serrucho", "precio":1000},
    {"id":2, "nombre":"Martillo", "precio":2000},
    {"id":3, "nombre":"Taladroo", "precio":3000}
]

@app.get("/articulos")
async def get_articulos():
    return articulos

@app.get("/articulos/{id}")
async def get_articulo_id(id:int):
    for articulo in articulos:
        if articulo["id"] == id:
            return articulo
    return {"error": "wachin"}

@app.delete("/articulos/{id}")
async def delete_articulo(id: int):
    for articulo in articulos:
        if articulo["id"] == id:
            articulos.remove(articulo)
            return {"mensaje": "articulo eliminado"}
    return {"mensaje": "error wachin"}
    
@app.post("/articulos")
async def crear_articulo(id: int, nombre:str, precio:int):
    nuevo_art = {
        "id": id,
        "nombre": nombre,
        "precio": precio
    }
    articulos.append(nuevo_art)
    return nuevo_art

@app.put("/articulos/{id}")
async def editar_articulos(id: int, nombre: str, precio: int):
    for articulo in articulos:
        if articulo["id"] == id:
            articulo["nombre"] = nombre
            articulo["precio"] = precio
            return articulo
        return {"error pa"}
"""

from fastapi import FastAPI, HTTPException

app = FastAPI()

# "Base de datos" simulada
peliculas = [
    {"id": 1, "titulo": "Rapidos y Furiosos", "director": "Christopher Magallanes", "anio": 2010},
    {"id": 2, "titulo": "La bala que doblo a la esquina", "director": "Christopher Cobos", "anio": 2014},
    {"id": 3, "titulo": "El asesinato del muerto", "director": "Chirstopher ", "anio": 2019}
]

# GET - obtener todas las peliculas
@app.get("/peliculas")
def obtener_peliculas():
    return peliculas

# GET - obtener una pelicula por id
@app.get("/peliculas/{id}")
def obtener_pelicula(id: int):
    for pelicula in peliculas:
        if pelicula["id"] == id:
            return pelicula
    raise HTTPException(status_code=404, detail="Pelicula no encontrada")

# POST - agregar una nueva pelicula
@app.post("/peliculas")
def agregar_pelicula(pelicula: dict):
    peliculas.append(pelicula)
    return {"mensaje": "Pelicula agregada correctamente"}

# PUT - actualizar una pelicula
@app.put("/peliculas/{id}")
def actualizar_pelicula(id: int, datos: dict):
    for pelicula in peliculas:
        if pelicula["id"] == id:
            pelicula.update(datos)
            return {"mensaje": "Pelicula actualizada"}
    raise HTTPException(status_code=404, detail="Pelicula no encontrada")

# DELETE - eliminar una pelicula
@app.delete("/peliculas/{id}")
def eliminar_pelicula(id: int):
    for pelicula in peliculas:
        if pelicula["id"] == id:
            peliculas.remove(pelicula)
            return {"mensaje": "Pelicula eliminada"}
    raise HTTPException(status_code=404, detail="Pelicula no encontrada")