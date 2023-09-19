from pydantic import BaseModel, Field
from uuid import UUID

from api.models.crypto_models import CryptoSchema


class OrmSchema(BaseModel):
    class Config:
        from_attributes = True


class UserSchema(OrmSchema):
    id: UUID = Field(description="User's unique identifier")
    username: str = Field(description="Name of the user")
    crypto: list[CryptoSchema] = Field(
        description="List of cryptocurrency related to the user"
    )


class UserAddSchema(BaseModel):
    username: str = Field(
        description="Username must be alpha-numeric, between 4 and 20 chars and cannot contain prohibited words."
    )
