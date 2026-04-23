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