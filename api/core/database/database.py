from beanie import init_beanie
import motor.motor_asyncio

from config import Settings
from api.jokes.schemas import Joke

conf = Settings()


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        f"mongodb://{conf.mongo_root_username}:{conf.mongo_root_password}@{conf.mongo_db_host}:{conf.mongo_db_port}"
    )

    await init_beanie(database=client[conf.db_name], document_models=[Joke])
