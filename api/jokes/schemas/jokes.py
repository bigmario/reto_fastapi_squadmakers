from pydantic import Field, BaseModel
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
