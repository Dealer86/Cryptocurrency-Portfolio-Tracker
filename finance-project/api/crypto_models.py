from pydantic import BaseModel, Field


class CryptoSchema(BaseModel):
    name: str = Field(description="Name of cryptocurrency")
    symbol: str = Field(description="Symbol of cryptocurrency")
    price: float = Field(description="Price of cryptocurrency")
    last_updated: str = Field(description="Date of last update")
    units: float = Field(description="Number of cryptocurrency")

    class Config:
        from_attributes = True


class CryptoAdd(BaseModel):
    name: str = Field(description="Name of cryptocurrency", default="bitcoin")
