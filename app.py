from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

from admin.admin import admin


app.include_router(admin)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")

@app.get("/upload_file", response_class=HTMLResponse)
def gallery(request: Request):
    return templates.TemplateResponse(request=request, name="gallery.html")