#Python
from uuid import UUID
from typing import Optional, List
from datetime import date, datetime
import json

#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

#FastApi
from fastapi import FastAPI
from fastapi import status
from fastapi import Body

app = FastAPI()

#Models

class Tweet(BaseModel):
    tweet_id : UUID = Field(...)
    content : str = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(default = datetime.now())

class UserBase(BaseModel):
    user_id : UUID = Field(...)
    Email: EmailStr = Field (
        ...,
        example = "roberto@example.com"
    )

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length = 8,
        max_length = 64
        )

class User(UserBase):
    first_name: str = Field(
        ...,
        min_length = 1,
        man_length = 50,
        example = "Roberto Ángel"
    )

    last_name: str = Field(
        ...,
        min_length = 1 ,
        man_length = 50,
        example = "Abad De Los santos"
        )

    birth_date : Optional[date] = Field(
        default = None,
        example = datetime(2003, 9, 10)
        )

class UserRegister(User):
    password: str = Field(
        ...,
        min_length = 8,
        max_length = 64,
        example = "angeleselmejor10"
        )



# Path operations

## Users

### Register a user
@app.post(
    path = "/signup",
    response_model = User,
    status_code= status.HTTP_201_CREATED,
    summary = "Register the user",
    tags = ["Users"]
    )

def register(user: UserRegister = Body(...)):
    """
    Signup

    This function register a user in the app

    Paremeters:

        - Request body paremeter:

            - UserRegister
    
    Returns a json with the basic user information

        - user_id : UUID
        - first_name: str
        - last_name: str
        - Email: EmailStr
        - Birth_date: datetime

    """

    with open ("users.json", "r+", encoding = "utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user

### Login a user
@app.post(
    path = "/login",
    response_model = User,
    status_code= status.HTTP_200_OK,
    summary = "Log the user",
    tags = ["Users"]
    )

def login():
    pass

### Show all users
@app.get(
    path = "/users",
    response_model = List[User],
    status_code= status.HTTP_201_CREATED,
    summary = "Show all the users",
    tags = ["Users"]
    )

def show_all_users():
    pass

### Show a user
@app.get(
    path = "/user/{user_id}",
    response_model = User,
    status_code= status.HTTP_201_CREATED,
    summary = "Show the user",
    tags = ["Users"]
    )

def show_user():
    pass

### Delete a user
@app.delete(
    path = "/user/{user_id}/delete",
    response_model = User,
    status_code= status.HTTP_201_CREATED,
    summary = "Delete the user",
    tags = ["Users"]
    )

def delete_user():
    pass

### Update a user
@app.put(
    path = "/user/{user_id}/put",
    response_model = User,
    status_code= status.HTTP_201_CREATED,
    summary = "Update the user",
    tags = ["Users"]
    )

def update_user():
    pass

## Tweets

### Show all tweets
@app.get(
    path = "/",
    status_code = status.HTTP_200_OK,
    summary = "Show all tweets",
    tags = ["Tweets"]
    )

def home():
    return {"Twitter API" : "working"}

### Show a tweet
@app.get(
    path = "tweets/{tweet_id}",
    response_model = Tweet,
    status_code = status.HTTP_200_OK,
    summary  = "Show a tweet",
    tags = ["Tweets"]
    )

def show_a_tweet():
    pass

### Post a tweet
@app.post(
    path = "/post",
    response_model = Tweet,
    status_code= status.HTTP_201_CREATED,
    summary = "Post a tweet",
    tags = ["Tweets"]
    )

def post():
    pass

### Delete a tweet
@app.delete(
    path = "tweets/{tweet_id}/delete",
    response_model = Tweet,
    status_code = status.HTTP_200_OK,
    summary = "Delete a tweet",
    tags = ["Tweets"]
    )

def delete_a_tweet():
    pass

### Update a tweet
@app.put(
    path = "tweets/{tweet_id}/update",
    response_model = Tweet,
    status_code = status.HTTP_200_OK,
    summary = "Update a tweet",
    tags = ["Tweets"]
)

def update_a_tweet():
    pass