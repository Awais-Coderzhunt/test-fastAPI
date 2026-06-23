from datetime import datetime

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..schemas import PostCreate, PostResponse

router = APIRouter(tags=["posts"])
templates = Jinja2Templates(directory="awais1/templates")
posts: list[dict] = [
    {
        "id": 1,
        "author": "Awais Rasool",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": 2026/3/23,
    },
    {
        "id": 2,
        "author": "Awais Rasool",
        "title": "Learning Routing",
        "content": "Routing files keep the main app simple and easy to read.",
        "date_posted": 2026/3/23,
    },
]


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
@router.get("/posts", response_class=HTMLResponse, include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", {"posts": posts, "title": "Awais Rasool"})


@router.get("/posts/{post_id}", response_class=HTMLResponse, include_in_schema=False)
def get_post_page(request: Request, post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return templates.TemplateResponse(request, "post.html", {"post": post, "title": post["title"][:50]})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")


@router.get("/api/posts", response_model=list[PostResponse])
def get_posts():
    return posts


@router.post("/api/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate):
    new_id = max(item["id"] for item in posts) + 1 if posts else 1
    new_post = {
        "id": new_id,
        "author": post.author,
        "title": post.title,
        "content": post.content,
        "date_posted": datetime.now(),
    }
    posts.append(new_post)
    return new_post


@router.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
