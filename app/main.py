from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()  #app is my fastapi instance



class Post(BaseModel):       #This code is for creating and updating posts. Class Post inherits class BaseModel
    title: str   #attribute title would only hold string (type hinting class attribute)
    content: str
    published: bool = True    #if the user doesn't give any value then the boolean value would be True
    rating: Optional[int] = None    #Using Optional[int] instead of just int will let the editor help you detecting errors where you could be assuming that a value is always a str, when it could actually be None too. This is a type hinting.




my_posts = [{"title":"title of post 1", "content":"content of post 1", "id":1}, {"title":"cool cars", "content":"m4k and outlander are cool cars", "id":2}]


def find_post(id):   # a function to retrieve posts using id
    for x in my_posts:
        if x["id"] == id:
            return x

def find_index_post(id):  #a function to retrieve an id's index
    for x, j in enumerate(my_posts):  #enumerate returns enumerate object(use list() to return a tuple)
        if j["id"] == id:
            return x
        


#routes are order dependent
#entering an url/route will check the first decorator then so on and so forth


@app.get("/") #@app is called a decorator 
def root():
    return {"message": "Welcome to my API!!!"}


@app.get("/posts")  #Retrieve all the posts from the database using get method (CRUD operation)
def get_posts():
    return {"data" : my_posts} #fastapi will convert the array into a json 


@app.post("/posts", status_code=status.HTTP_201_CREATED)  #Create a post using post method (CRUD operation), Status code 201 is given as a default as posting should giver 201 as the status code
def create_posts(post: Post):   #post would only hold new datatype created by class Post (type hinting function attribute)
    print(post)    #the datatype post is holding is a pydantic model
    print(post.title)
    print(post.content)
    print(post.published)
    print(post.rating)
    print(post.dict())      #dict() converts the post's data which is a pydantic model to a dictionary
    post_dict=post.dict()
    post_dict["id"] = randrange(0,1000000000) 
    my_posts.append(post_dict)
    return{"data" : post_dict}


@app.get("/posts/{id}")     #Retrieve a particular post 
def get_post(id: int, response_msg: Response):   #int type hint so that fastapi gives error msg id string is given, response_msg will have the Response object
    post= find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")   #Status code 404 given, detail="" msg will be returned to the frontend as fastapi does that automatically 
        #he upper code is the alternative of the code given below in the comments
        #response_msg.status_code = status.HTTP_404_NOT_FOUND  #it will set the Status to 404 if post is empty
        #return{"message":f"post with id: {id} was not found"}
    return{"post_detail" : post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)  #Delete a particular post, 204 given as a status code
def delete_post(id: int):
    index= find_index_post(id)
    #If the id does not exists, find_index_post would return None and pop(None) would not work. So we raise an HTTP exception
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#The PUT operation is a replace operation—not an update operation—because the resource instance in the request body replaces every changeable configuration attribute of the existing resource. To update specific fields, use the PATCH operation
#Here in the code below, I have given the updated data in the frontend(All required fields).Then, I took the post of the id that I want top update and check if it exists. If it does, the post of that id gets replaced in the same index and get the same id.
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    print(post)
    #code for if the id does not exists for put method, throw a 404
    index= find_index_post(id)  
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    #if the id exits, we'll update it
    post_dict=post.dict()
    print(post_dict)
    post_dict["id"]=id    #we put same id in the dict
    my_posts[index]= post_dict   
    return{"data": post_dict}

