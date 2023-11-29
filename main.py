from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app= FastAPI()



class Post(BaseModel):       #class Post inherits class BaseModel
    title: str   #attribute title would only hold string (type hinting class attribute)
    content: str
    published: bool = True    #if the user doesn't give any value then the boolean value would be True
    rating: Optional[int] = None    #Using Optional[int] instead of just int will let the editor help you detecting errors where you could be assuming that a value is always a str, when it could actually be None too. This is a type hinting.

@app.get("/")
def root():
    return {"message": "Welcome to my API!!!"}

@app.get("/posts")
def get_posts():
    return {"data":"This is your posts"}

@app.post("/createposts")
def create_posts(post: Post):  #post would only hold new datatype created by class Post (type hinting function attribute)
    print(post)
    print(post.title)
    print(post.content)
    print(post.published)
    print(post.rating)
    print(post.dict())  #post saves the data as a pydantic model and we can use .dict() in a pydantic model
    return{"data": post}


