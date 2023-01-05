#Python
from uuid import UUID
from typing import Optional, List
from datetime import date, datetime


#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

#FastApi
from fastapi import FastAPI
from fastapi import status

app = FastAPI()

#Models

class Tweet(BaseModel):
    tweet_id : UUID = Field(...)
    content : str = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(default = datetime.now())

class UserBase(BaseModel):
    user_id : UUID = Field(...)
    Email: EmailStr = Field(...)

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
        man_length = 50
    )

    last_name: str = Field(
        ...,
        min_length = 1 ,
        man_length = 50
        )

    birth_date : Optional[date] = Field(default = None)



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

def register():
    pass

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