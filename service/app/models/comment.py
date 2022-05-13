import pydantic
from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel, Field

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str


class OID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return ObjectId(str(v))
        except InvalidId as e:
            raise ValueError("Not a valid ObjectId") from e


class Comment(BaseModel):
    id: OID = Field(alias="_id")
    address: str
    name: str
    text: str
