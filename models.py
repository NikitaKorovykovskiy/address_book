from pydantic import BaseModel

class Address(BaseModel):
    address: str

class WriteAddress(Address):
    phone: str