from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, HTTPException
from cassandra.cqlengine.management import sync_table

from models import Post
from database import get_session

sample_posts = [
    {
        "title": "First post",
        "body": "This is the first post.",
        "created_at": datetime(2022, 12, 25, 12, 30)
    },
    {
        "title": "Second post",
        "body": "This is the second post.",
    }
]

    
@asynccontextmanager
async def lifespan(app: FastAPI):
    global DB_SEESSION
    DB_SEESSION = get_session()
    sync_table(Post)
    yield
    
app = FastAPI(lifespan=lifespan)

@app.get("/")
def homepage():
    return {"meaasage": "Rugged man FastAPI featuring clergey man ASTRA DB"}

@app.post("/posts")
def create_post():
    for post in sample_posts:
        post_data = Post.create(**post)
        
    return "Posts created successfully!"

@app.get("/posts")
def get_posts():
    posts = [dict(x) for x in Post.objects.all()]
    return posts

@app.put("/posts/{post_id}")
def update_post(post_id: str, title: str, body: str):
    try:
        post = Post.objects(post_id=post_id).get()
        post.title = title
        post.body = body
        post.save()
        return "Post updated successfully!"
    except:
        raise HTTPException(status_code=404, detail="Post not found")
    

@app.delete("/posts/{post_id}")
def delete_post(post_id: str):
    try:
        post = Post.objects(post_id=post_id).get()
        post.delete()
        return "Post deleted successfully!"
    except:
        raise HTTPException(status_code=404, detail="Post not found")