from fastapi import FastAPI, Body, Depends
from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer

posts = [
    {
        "id": 1,
        "title": "penguins",
        "text": "Penguins are a group of aquatic flightless bird."
    },
    {
        "id": 2,
        "title": "tiger",
        "text": "Tigers are the largest living cat species and a\
              members of the genus Panther"
    },
    {
        "id": 3,
        "title": "koalas",
        "text": "Koalas is arboral herbivorous marsupial native to Australia."
    },
]

users = []

app = FastAPI()


@app.get('/posts', tags=["posts"])
def get_posts():
    return {"data": posts}


@app.get('/posts/{post_id}', tags=['posts'])
def get_one_post(post_id: int):
    if post_id > len(posts):
        return {
            "error": "Post with this id does not exist!"
        }
    for post in posts:
        if post["id"] == post_id:
            return {
                "data": post
            }


@app.post('/posts', dependencies=[Depends(jwtBearer())], tags=["posts"])
def add_post(post: PostSchema):
    post.id = len(posts)+1
    posts.append(post.dict())
    return {
        "info": "post aadded"
    }


@app.post('/user/signup', tags=["user"])
def user_signup(user: UserSchema = Body(default=None)):
    users.append(user)
    return signJWT(user.email)


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        return False


@app.post('/user/login', tags=["user"])
def user_login(user: UserLoginSchema = Body(default=None)):
    if check_user(user):
        return signJWT(user.email)
    else:
        return {
            "error": "Invalid login details!"
        }
