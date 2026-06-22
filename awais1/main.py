
from fastapi import FastAPI

from fastapi.responses import HTMLResponse

app = FastAPI()

posts: list[dict] = [
    {
        "id": 1,
        "author": "Awais Rasool",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast."
    },
      {
        "id": 1,
        "author": "Awais Rasool",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast."
    }
]

@app.get("/" , response_class=HTMLResponse, include_in_schema=False)

@app.get("/post", response_class=HTMLResponse, include_in_schema=False)
def home():
    return f"<h1>Awais Rasool</h1>"

@app.get("/api/posts")
def get_posts():
    return posts