from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from fastapi_pagination import add_pagination


from api.core.database import init_db
from api.jokes.controller import jokes_router
from api.math.controller import math_router


app = FastAPI()


def __custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="SquadMakers Challenge",
        version="0.0.1",
        description="Reto Backend - Fast API",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = __custom_openapi

origins = [
    "*",
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jokes_router)
app.include_router(math_router)


@app.on_event("startup")
async def start_db():
    await init_db()


@app.get(path="/", summary="Index", tags=["Index"])
async def index():
    return JSONResponse(
        {
            "Framework": "FastAPI",
            "Message": "Hello Human, welcome to the FastAPI Squadmakers Challenge",
        }
    )


add_pagination(app)
