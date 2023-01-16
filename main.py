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
from fastapi import Body, Path
from fastapi import HTTPException

app = FastAPI()

#Models


class UserBase(BaseModel):
    user_id : UUID = Field(...)
    Email: EmailStr = Field (
        ...,
        example = "roberto@example.com"
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

class UserUpadte(BaseModel):
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

    Email: EmailStr = Field (
        ...,
        example = "roberto@example.com"
    )

    password: str = Field(
        ...,
        min_length = 8,
        max_length = 64,
        example = "angeleselmejor10"
        )

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length = 8,
        max_length = 64,
        example = "angeleselmejor10"
        )

class UserRegister(User):
    password: str = Field(
        ...,
        min_length = 8,
        max_length = 64,
        example = "angeleselmejor10"
        )

class Tweet(BaseModel):
    tweet_id : UUID = Field(...)
    content : str = Field(
        ...,
        min_length=1,
        max_length=250
        )
    created_at: datetime = Field(...)
    updated_at: Optional[datetime]= Field(default = datetime.now())
    by: User = Field(...)

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
    status_code= status.HTTP_200_OK,
    response_model= User,
    summary = "Log the user",
    tags = ["Users"]
    )

def login(user_login: UserLogin = Body(...)):    
    """
    - login user

    - Login user in the app

    - Parameters: 

        - Request body parameters:

            - user_id : UUID
            - Email : EmailStr
            - password : str

    - Returns a json with basic user information:

        - user_id : UUID
        - first_name: str
        - last_name: str
        - Email: EmailStr
        - Birth_date: datetime

    """

    with open ("users.json", "r", encoding = "utf-8") as f:

        results = json.loads(f.read())
        user_dict = user_login.dict()
        
        password_array  = []
        user_id_array  = []
        email_array  = []

        for result in results: 

            user_id_array.append(result["user_id"])
            email_array.append(result["Email"])
            password_array.append(result["password"])

            if str(result["user_id"]) == str(user_dict["user_id"]) :
                usuario = result

        if str(user_dict["user_id"]) not in user_id_array:

            raise HTTPException (
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "the user_id is not correct."
            )

        if user_dict["Email"] not in email_array:

            raise HTTPException (
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "the email is not correct."
            )

        if user_dict["password"] not in password_array:

            raise HTTPException (
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "the password is not correct."
            )

        return usuario
            
### Show all users
@app.get(
    path = "/users",
    response_model = List[User],
    status_code= status.HTTP_200_OK,
    summary = "Show all the users",
    tags = ["Users"]
    )

def show_all_users():
    """
    - Show users

    - This function shows all users

    - Parameters:

        -

    Returns a json  with these users keys:

        - user_id : UUID
        - first_name: str
        - last_name: str
        - Email: EmailStr
        - Birth_date: datetime

    """
    with open ("users.json", "r", encoding = "utf-8") as f :
        results = json.loads(f.read())
        return results

### Show a user
@app.get(
    path = "/user/{user_id}",
    response_model = User,
    status_code= status.HTTP_200_OK,
    summary = "Show the user",
    tags = ["Users"]
    )

def show_user(user_id: str = Path(...)):
    """
    - Show user

    - Show the basic information of a user

    - Parameters:

        - path parameter:

            - user_id : UUID
    
    - Returs a json with the user information:

        - user_id : UUID
        - first_name: str
        - last_name: str
        - Email: EmailStr
        - Birth_date: datetime

    """
    with open ("users.json", "r", encoding = "utf-8") as f:

        results = json.loads(f.read())
        user_id_array = []

        for result in results: 

            user_id_array.append(result["user_id"])

            if result["user_id"] == str(user_id) :
                usuario = result

        if str(user_id) not in user_id_array:

            raise HTTPException (
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "the user_id is not correct."
            )

        return usuario

### Delete a user
@app.delete(
    path = "/user/{user_id}/delete",
    response_model = User,
    status_code= status.HTTP_201_CREATED,
    summary = "Delete the user",
    tags = ["Users"]
    )

def delete_user(user_id : str = Path(...)):
    """
    - Delete a user

    - This function deletes a user

    - Parameters:

        - path parameters: 

            - user_id : UUID
    
    - Returns a json with the deleted user:

        - user_id : UUID
        - first_name: str
        - last_name: str
        - Email: EmailStr
        - Birth_date: datetime

    """

    with open ("users.json", "r+", encoding = "utf-8") as f:
        results = json.loads(f.read())

        user_id_array = []

        for result in results:

            user_id_array.append(result["user_id"])

            if str(user_id) == result["user_id"]:

                results.remove(result)
                usuario = result
            
        f.seek(0)
        f.write(json.dumps(results))
        f.truncate()
        return usuario

### Update a user
@app.put(
    path = "/user/{user_id}/put",
    response_model = UserUpadte,
    status_code= status.HTTP_200_OK,
    summary = "Update the user",
    tags = ["Users"]
    )

def update_user(
    user_id: str = Path(
        ...,
        example = "3fa85f64-5717-4562-b3fc-2c963f66afa2"
        ),
    user: UserUpadte = Body(...)
):
    """
    - Update user

    - This function updates a user

    - Parameters:

        - Request body parameters:

            - User object with the following keys:

                - user_id : UUID
                - first_name: str
                - last_name: str
                - Email: EmailStr
                - Birth_date: datetime

        - Path parameters:

            - user_id : UUID

        - Returns a json with updated user:

            - user_id : UUID
            - first_name: str
            - last_name: str
            - Email: EmailStr
            - Birth_date: datetime

    """

    with open("users.json", "r+", encoding = "utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_id_array = []

        for index, result in enumerate(results) :

            user_id_array.append(result["user_id"])    

            if str(user_id) == result["user_id"]:
                user_dict["birth_date"] = str(user_dict["birth_date"])
                user_dict["user_id"] = str(user_id)
                usuario = user_dict
                results[index] = usuario

        if str(user_id) not in user_id_array :

            raise HTTPException (
                status_code = status.HTTP_404_NOT_FOUND,
                detail =  "The user id is not valid."
            )
        
        f.seek(0)
        f.write(json.dumps(results))
        f.truncate()
        return usuario
## Tweets

### Show all tweets
@app.get(
    path = "/",
    status_code = status.HTTP_200_OK,
    summary = "Show all tweets",
    tags = ["Tweets"]
    )

def home():
    """
    - Show tweets 

    - Show all tweets in the app

    Returns a list of json with the following keys: 

        - tweet_id : UUID 
        - content : str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """
    with open ("tweets.json", "r", encoding= "utf-8") as f:
        results = json.loads(f.read())
        return results
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

def post(tweet: Tweet = Body(...)):
    """
    - Post a tweet

    - This function post a tweet 

    - Parameters: 

        - Request body parameters:

            - tweet: Tweet
    
    - Returns a json with the basic tweet information

        - tweet_id : UUID 
        - content : str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User

    """
    with open ("tweets.json", "r+", encoding = "utf-8") as f:
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])   
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        tweet_dict["by"]["user_id"]  = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])
        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet


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