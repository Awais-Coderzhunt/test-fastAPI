from fastapi import APIRouter, HTTPException, Request, status, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..schemas import PostCreate, PostResponse
from ..models import Post
from ..database import get_db


router = APIRouter(tags=["posts"])
templates = Jinja2Templates(directory="awais1/templates")


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
def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).order_by(Post.id.desc()).all()


@router.post("/api/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = Post(
        author=post.author,
        title=post.title,
        content=post.content,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
    return post
