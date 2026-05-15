from fastapi import FastAPI, HTTPException, Body, Path, Query

app = FastAPI()

# ==============================
# BASE DE DATOS 
# ==============================
peliculas = [
    {"id": 1, "titulo": "Rapidos y Furiosos", "director": "Christopher Magallanes", "anio": 2010},
    {"id": 2, "titulo": "La bala que doblo a la esquina", "director": "Christopher Cobos", "anio": 2014},
    {"id": 3, "titulo": "El asesinato del muerto", "director": "Christopher", "anio": 2019}
]

# ==============================
# GET - OBTENER TODAS LAS PELICULAS
# ==============================
@app.get("/peliculas")
def obtener_peliculas(
    anio: int = Query(None, ge=1900, le=2100, description="Filtrar por anio")
):
    if anio:
        return [p for p in peliculas if p["anio"] == anio]
    return peliculas

# ==============================
# GET - OBTENER PELICULA POR ID
# ==============================
@app.get("/peliculas/{id}")
def obtener_pelicula(
    id: int = Path(..., gt=0, description="ID de la pelicula")
):
    for pelicula in peliculas:
        if pelicula["id"] == id:
            return pelicula

    raise HTTPException(
        status_code=404,
        detail="Pelicula no encontrada"
    )

# ==============================
# POST - AGREGAR PELICULA
# ==============================
@app.post("/peliculas")
def agregar_pelicula(
    pelicula: dict = Body(
        ...,
        example={
            "id": 4,
            "titulo": "Nueva Pelicula",
            "director": "Director X",
            "anio": 2025
        }
    )
):
    # Validacion basica
    if "id" not in pelicula or "titulo" not in pelicula:
        raise HTTPException(
            status_code=400,
            detail="Faltan datos obligatorios"
        )

    # Evitar ID duplicado
    for p in peliculas:
        if p["id"] == pelicula["id"]:
            raise HTTPException(
                status_code=400,
                detail="El ID ya existe"
            )

    peliculas.append(pelicula)

    return {
        "mensaje": "Pelicula agregada correctamente"
    }

# ==============================
# PUT - ACTUALIZAR PELICULA
# ==============================
@app.put("/peliculas/{id}")
def actualizar_pelicula(
    id: int = Path(..., gt=0),
    datos: dict = Body(
        ...,
        example={"titulo": "Titulo actualizado"}
    )
):
    for pelicula in peliculas:
        if pelicula["id"] == id:
            pelicula.update(datos)

            return {
                "mensaje": "Pelicula actualizada correctamente"
            }

    raise HTTPException(
        status_code=404,
        detail="Pelicula no encontrada"
    )

# ==============================
# DELETE - ELIMINAR PELICULA
# ==============================
@app.delete("/peliculas/{id}")
def eliminar_pelicula(
    id: int = Path(..., gt=0)
):
    for pelicula in peliculas:
        if pelicula["id"] == id:
            peliculas.remove(pelicula)

            return {
                "mensaje": "Pelicula eliminada correctamente"
            }

    raise HTTPException(
        status_code=404,
        detail="Pelicula no encontrada"
    )