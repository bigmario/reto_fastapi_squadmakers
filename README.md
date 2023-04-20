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
Se empleó MongoDB, ya que por la posible gran cantidad de data a almacenar, MongoDB podría ser una buena opción debido a su flexibilidad, escalabilidad, velocidad y facilidad de uso. Además, si la data no tienen una estructura predefinida, MongoDB podría ser aún más adecuada debido a su capacidad para manejar datos no estructurados o semiestructurados.

## Sentencia para crear la BBDD y el modelo de datos requerido
Al momento de iniciarse el servidor, se ejecuta la siguiente intruccion "on startup"
```python
@app.on_event("startup")
async def start_db():
    await init_db()
```
Lo que llama al core del sistema y hace la conección e inicialización de la base de datos mediante el driver "motor" y el ODM "Beanie":

```python
async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        f"mongodb://{conf.mongo_root_username}:{conf.mongo_root_password}@{conf.mongo_db_host}:{conf.mongo_db_port}"
    )

    await init_beanie(database=client[conf.db_name], document_models=[Joke])
```

El modelo de datos se define en `api/jokes/schemas/jokes.py`
```python
from beanie import Document


class Joke(Document):
    joke: str | None = None

    class Settings:
        name = "jokes"

    class Config:
        schema_extra = {
            "example": {
                "joke": "Chuck Norris is so hard he jumped from the effiel tower broke both his legs and walked to the hospital",
            }
        }
```

## PUESTA EN MARCHA
- ejecutar las siguientes instrucciones:
    ```
    python -m venv venv
    pip install -r requirements.txt
    ```
- renombrar el archivo `.env.example` a `.env` y modificar las variables a conveniencia (con modificar las variables MONGO_ROOT_USERNAME y MONGO_ROOT_PASSWORD es suficiente) .

- Levantar el servidor:
    - 1ra. opción: Ejecutando directamente `python main.py`, pero se debe tener un servicio Mongo corriendo en el equipo y modificar las variables MONGO_ROOT_USERNAME, MONGO_ROOT_PASSWORD, MONGO_DB_HOST, MONGO_DB_PORT.
    - 2da. opción: con la instruccion `docker compose up --build` (se incluyen los archivos `docker-compose.yml` y `Dockerfile` necesarios), que se encarga de crear los contenedores para MongoDB y la API respectivanmente, junto con los volumenes necesarios tanto para la base de datos como para la API, de manera que funcione el "Live Reloading" de FastAPI, ademas de la red interna que los interconecta, esta es la forma mas rápida ya que solo hay que indicar un MONGO_ROOT_USERNAME y MONGO_ROOT_PASSWORD para el contenedor mongo (en el archivo `env`).

## Documentación de la API y Swagger UI
Para acceder a a la documentacion de la API mediante Swagger UI, luego de levantar el servidor, se debe acceder a la siguiente URL: <http://localhost:8000/docs>

## TESTING
Para ejecutar los tests solo debe ejecutarse la instruccion `pytest`<br>
Estos tests estan intradocumentados y se encuentran en el archivo `test_main.py` 