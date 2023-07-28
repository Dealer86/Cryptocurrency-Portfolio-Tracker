from pydantic import BaseModel, Field, field_validator
from uuid import UUID


class OrmSchema(BaseModel):
    class Config:
        from_attributes = True


class UserSchema(OrmSchema):
    id: UUID = Field(description="User's unique identifier")
    username: str = Field(description="Name of the user")
    crypto: list[str] = Field(description="List of cryptocurrency related to the user")


class UserAddSchema(OrmSchema):
    username: str = Field(description="Name of the user between 4 and 20 chars")
