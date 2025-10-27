import uuid
import pandas as pd
from datetime import datetime, timedelta
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")
USERS = "users.csv"
SESSION_TTL = timedelta(10)
sessions = {}
white_urls = ["/", "/login", "/logout"]

#Контролоь авторизации и сессии
@app.middleware("http")
async def check_session(request: Request, call_next):
    path = request.url.path
    if path.startswith("/static") or path.startswith("/assets") or path in white_urls:
        return await call_next(request)

    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in sessions:
        return RedirectResponse(url="/login")

    created_session = sessions[session_id]
    if datetime.now() - created_session > SESSION_TTL:
        del sessions[session_id]
        return RedirectResponse(url="/login")

    return await call_next(request)



@app.get("/", response_class=HTMLResponse)
@app.get("/login", response_class=HTMLResponse)
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(request: Request,
            username: str = Form(...),
            password: str = Form(...)):
    users = pd.read_csv(USERS)
    if username in users['user'].values:
        session_id = request.cookies.get("session_id")
        if session_id in sessions:
            del sessions[session_id]
            return templates.TemplateResponse("login.html", {
                "request": request,
                "message": "Глупец, ты уже был авторизован"
            }) 
        if str(users[users['user'] == username].values[0][1]) == password:
            session_id = str(uuid.uuid4())
            sessions[session_id] = datetime.now()
            response = RedirectResponse(url=f"/home/{username}", status_code=302)
            response.set_cookie(key="session_id", value=session_id)
            return response
        return templates.TemplateResponse("login.html",
                                       {"request": request,
                                        "error": "Глупец, введи правильный пароль"})
    return templates.TemplateResponse("login.html",
                                       {"request": request,
                                        "error": "Глупец, введи правильный логин"})


@app.get("/logout", response_class=HTMLResponse)
def logout(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id in sessions:
        del sessions[session_id]
    return templates.TemplateResponse("login.html", {
        "request": request,
        "message": "Вы вышли из системы"
    })


@app.get("/home/admin", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@app.get("/to_login")
def to_login():
    return RedirectResponse(url="/login", status_code=302)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return await http_exception_handler(request, exc)


@app.get("/login", response_class=HTMLResponse)
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})