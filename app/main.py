from fastapi import FastAPI
from . import models
from .database import engine, get_db
from .routers import post, user, auth, votes
from fastapi.middleware.cors import CORSMiddleware





models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)






my_posts=[{'title':'title of post 1','content':'content of post 1','id':1},{'title':'favorite foods','content':'i like pizza','id':2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
def home():
    return {'hello':'world'}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail":post}






















