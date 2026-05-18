from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from cache import init_cache



app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

from admin.admin import admin
from users.users import user


app.include_router(admin)
app.include_router(user)

@app.on_event("startup")
def startup():
    init_cache()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(name="homes.html", request= request)


@app.get("/admin", response_class=HTMLResponse)
def admin(request: Request):
    return templates.TemplateResponse(name="admin.html", request= request)


@app.get("/apps", response_class=HTMLResponse)
def apps(request: Request):
    return templates.TemplateResponse(name="apps.html", request= request)


@app.get("/complaint-status", response_class=HTMLResponse)
def complaint_status(request: Request):
    return templates.TemplateResponse(name="complaint-status.html", request= request)


@app.get("/contact", response_class=HTMLResponse)
def contact(request: Request):
    return templates.TemplateResponse(name="contact.html", request= request)


@app.get("/emergency", response_class=HTMLResponse)
def emergency(request: Request):
    return templates.TemplateResponse(name="emergency.html", request= request)


@app.get("/events", response_class=HTMLResponse)
def events(request: Request):
    return templates.TemplateResponse(name="events.html", request= request)


@app.get("/foundation", response_class=HTMLResponse)
def foundation(request: Request):
    return templates.TemplateResponse(name="foundation.html", request= request)


@app.get("/gallery", response_class=HTMLResponse)
def gallery(request: Request):
    return templates.TemplateResponse(name="gallery.html", request= request)


@app.get("/grievance", response_class=HTMLResponse)
def grievance(request: Request):
    return templates.TemplateResponse(name="grievance.html", request= request)


# @app.get("/home", response_class=HTMLResponse)
# def home_page(request: Request):
#     return templates.TemplateResponse("home.html", request= request)


# @app.get("/index", response_class=HTMLResponse)
# def index(request: Request):
#     return templates.TemplateResponse("/", request= request)


@app.get("/nagarsevak", response_class=HTMLResponse)
def nagarsevak(request: Request):
    return templates.TemplateResponse(name="nagarsevak.html", request= request)


@app.get("/news", response_class=HTMLResponse)
def news(request: Request):
    return templates.TemplateResponse(name="news.html", request= request)


@app.get("/prabhag", response_class=HTMLResponse)
def prabhag(request: Request):
    return templates.TemplateResponse(name="prabhag.html", request= request)


@app.get("/schemes", response_class=HTMLResponse)
def schemes(request: Request):
    return templates.TemplateResponse(name="schemes.html", request= request)


@app.get("/works", response_class=HTMLResponse)
def works(request: Request):
    return templates.TemplateResponse(name="works.html", request= request)

@app.get("/eservices", response_class=HTMLResponse)
def eservices(request: Request):
    return templates.TemplateResponse(name="eservices.html", request= request)
