from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from app.scraper import news_scraper

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    # 10 List article order by ASC or random
    
    return templates.TemplateResponse("item_list.html", {"request": request})


@app.get("/posts/{slug}")
def single_post():
    # Get post from database
    # Return html template response
    return 


@app.post("/generate")
def generate_content(request: Request):
    # Action to create content base on keyword
    # Use try catch
    kw = request["keyword"]

    config = {
        "keyword": kw,
        "pretty_url": True,
        "get_content": True
    }
    results = news_scraper(config)
    # response = {"message": "success"}
    return JSONResponse(results)
