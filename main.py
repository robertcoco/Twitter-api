#Python
from uuid import UUID
from typing import Optional
from datetime import date

#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

#FastApi
from fastapi import FastAPI

app = FastAPI()

#Models

class Twitter():
    pass

class UserBase(BaseModel):
    user_id : UUID = Field(...)
    Email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length = 8
        )

class User(UserBase):
    first_name: str = Field(
        ...,
        min_length = 1,
        man_length = 50
    )

    last_name: str = Field(
        ...,
        min_length = 1 ,
        man_length = 50
        )

    birth_date : Optional[date] = Field(default = None)

@app.get(path = "/")
def home():
    return {"Twitter API" : "working"}