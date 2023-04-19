# Reto Backend - Fast API
## Autor: Mario Castro <mariocastro.pva@gmail.com>

La prueba consiste en crear un API Rest en el framework Fast API utilizando
los siguientes repositorios como base de datos:
<br>
- https://api.chucknorris.io/
- https://icanhazdadjoke.com/api

Crear el API REST con los siguientes endpoints:
<br>
<br>
### ENDPOINT DE CHISTES

- GET: Se devolverá un chiste aleatorio si no se pasa ningún path param.<br>
    - Si se envía el path param habrá que comprobar si tiene el valor “Chuck” o el valor “Dad”
        - Si tiene el valor “Chuck” se conseguirá el chiste de este API https://api.chucknorris.io
        - Si tiene el valor “Dad” se conseguirá del API https://icanhazdadjoke.com/api+
    - En caso de que el valor no sea ninguno de esos dos se devolverá el error correspondiente.

- POST: guardará en una base de datos el chiste (texto pasado por parámetro)

- UPDATE: actualiza el chiste con el nuevo texto sustituyendo al chiste indicado en el parámetro “number”

- DELETE: elimina el chiste indicado en el parametro number.

### ENDPOINT MATEMÁTICO
- GET: Endpoint al que se le pasará un query param llamado “numbers” con una lista de números enteros. La respuesta de este
endpoint debe ser el mínimo común múltiplo de ellos
- GET: Endpoint al que se le pasará un query param llamado “number” con un número entero. La respuesta será ese número + 1.

## ¿Qué repositorio / Base de datos fue utilizada?
Se empleó MongoDB, ya que para almacenar una gran cantidad de chistes, MongoDB podría ser una buena opción debido a su flexibilidad, escalabilidad, velocidad y facilidad de uso. Además, si los chistes no tienen una estructura predefinida, MongoDB podría ser aún más adecuada debido a su capacidad para manejar datos no estructurados o semiestructurados.

## Sentencia para crear la BBDD y el modelo de datos requerido
Al momento de iniciarse el servidor, se ejecuta la siguiente intruccion "on startup"
```python
@app.on_event("startup")
async def start_db():
    await init_db()
```
Lo que llama al core del sistema y hace la coneccion a la base de datos mediante el driver "motor" y el ODM "Beanie":

```python
async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        f"mongodb://{conf.mongo_root_username}:{conf.mongo_root_password}@{conf.mongo_db_host}:{conf.mongo_db_port}"
    )

    await init_beanie(database=client.db_name, document_models=[Joke])
```

## EJECUCION
- renombrar el archivo `.env.example` a `.env` y modificar las variables a conveniencia.

- Levantar el servidor:
    - Ejecutando directamente `python main.py`, pero se debe tener un servicio Mongo corriendo en el equipo
    - con la instruccion `docker compose up --build` (se incluyen los archivos `docker-compose.yml` y `Dockerfile` necesarios), que se encarga de crear los contenedores para MongoDB y la API respectivanmente, junto con los volumenes necesarios tanto para la base de datos como para la API, de manera que funcione el "Live Reloading" de FastAPI, ademas de la red interna que los interconecta, esta es la forma mas rapida ya que solo hay que indicar un USERNAME y PASSWORD para el contenedor mongo.  