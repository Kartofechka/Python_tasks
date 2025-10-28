import uuid
import pandas as pd
from datetime import datetime, timedelta
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
from functools import wraps
import inspect
import hashlib
import asyncio
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(session_cleaner())
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")
USERS = "users.csv"
SESSION_TTL = timedelta(1)
sessions = {}
white_urls = ["/", "/login", "/logout"]


logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s",
    filename="logs.log", filemode="a", encoding="utf-8"
)

logger = logging.getLogger(__name__)

def log(func):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        request: Request = kwargs.get("request") or (args[0] if args else None)
        client_ip = request.client.host if request else "неизвестно"
        path = request.url.path if request else "неизвестно"

        logger.info(f"Вызов: {func.__name__} | Путь: {path} | IP: {client_ip}")
        try:
            result = await func(*args, **kwargs)
            logger.info(f"Завершено: {func.__name__} | Путь: {path} | IP: {client_ip}")
            return result
        except Exception as e:
            logger.error(f"Ошибка в {func.__name__} | Путь: {path} | IP: {client_ip} | Ошибка: {e}")
            raise

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        request: Request = kwargs.get("request") or (args[0] if args else None)
        client_ip = request.client.host if request else "неизвестно"
        path = request.url.path if request else "неизвестно"

        logger.info(f"Вызов: {func.__name__} | Путь: {path} | IP: {client_ip}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"Завершено: {func.__name__} | Путь: {path} | IP: {client_ip}")
            return result
        except Exception as e:
            logger.error(f"Ошибка в {func.__name__} | Путь: {path} | IP: {client_ip} | Ошибка: {e}")
            raise

    return async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper


#Контролоь авторизации и сессии
@app.middleware("http")
@log 
async def check_session(request: Request, call_next):
    path = request.url.path
    if path.startswith("/static") or path.startswith("/assets") or path in white_urls:
        return await call_next(request)
    session_id = request.cookies.get("session_id")

    if not session_id or session_id not in sessions:
         return RedirectResponse(url="/login") 
    last_active = sessions[session_id]

    if datetime.now() - last_active > SESSION_TTL:
         del sessions[session_id]
         return RedirectResponse(url="/login")
    
    sessions[session_id] = datetime.now()
    return await call_next(request)


async def session_cleaner():
    while True:
        expired = [session_id for session_id, last in sessions.items() if datetime.now() - last > SESSION_TTL]
        for session_id in expired:
            logger.info(f"Очистка истекшей сессии: {session_id}")
            del sessions[session_id]
        await asyncio.sleep(60)


@app.get("/", response_class=HTMLResponse)
@app.get("/login", response_class=HTMLResponse)
@log
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
@log
def login(request: Request,
            username: str = Form(...),
            password: str = Form(...)):
    users = pd.read_csv(USERS)
    if username in users['user'].values:
        logger.info(f"Попытка входа: {username}")
        session_id = request.cookies.get("session_id")
        if session_id in sessions:
            del sessions[session_id]
            return templates.TemplateResponse("login.html", {
                "request": request,
                "message": "Глупец, ты уже был авторизован"
            }) 
        if str(users[users['user'] == username].values[0][1]) == hashlib.sha256(password.encode()).hexdigest():
            session_id = str(uuid.uuid4())
            sessions[session_id] = datetime.now()
            response = RedirectResponse(url=f"/home/{username}", status_code=302)
            response.set_cookie(key="session_id", value=session_id)
            response.set_cookie(key="user_name", value=username)
            response.set_cookie(key="role", value = str(users[users['user'] == username].values[0][2]))
            print(request.cookies.get("session_id"), request.cookies.get("user_name"), request.cookies.get("role"))
            logger.info(f"Успешный вход: {username} | session_id: {session_id}")
            return response
        logger.warning(f"Неверный пароль для: {username}")
        return templates.TemplateResponse("login.html",
                                       {"request": request,
                                        "error": "Глупец, введи правильный пароль"})
    logger.warning(f"Логин не найден: {username}")
    return templates.TemplateResponse("login.html",
                                       {"request": request,
                                        "error": "Глупец, введи правильный логин"})


@app.get("/logout", response_class=HTMLResponse)
@log
def logout(request: Request):
    user_name = request.cookies.get("user_name")
    session_id = request.cookies.get("session_id")
    logger.info(f"Выход пользователя: {user_name} | {session_id}")
    if session_id in sessions:
        del sessions[session_id]
    return templates.TemplateResponse("login.html", {
        "request": request,
        "message": "Вы вышли из системы"
    })


@app.get("/home/admin", response_class=HTMLResponse)
@log
def login_page(request: Request):
    user_name = request.cookies.get("user_name")
    logger.info(f"Админ {user_name} перешел в main")
    return templates.TemplateResponse("main.html", {"request": request})


@app.get("/to_login", response_class=HTMLResponse)
@log
def to_login(request: Request):
    user_name = request.cookies.get("user_name")
    session_id = request.cookies.get("session_id")
    logger.info(f"Переход на страницу авторизации: {user_name} | {session_id}")
    return RedirectResponse(url="/login", status_code=302)


@app.exception_handler(StarletteHTTPException)
@log
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        user_name = request.cookies.get("user_name")
        session_id = request.cookies.get("session_id")
        logger.info(f"Попытка найти вход там, где его нет: {user_name} | {session_id}")
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return await http_exception_handler(request, exc)


@app.get("/register", response_class=HTMLResponse)
@log
def get_register_page(request: Request):
    user_name = request.cookies.get("user_name")
    session_id = request.cookies.get("session_id")
    if user_name == "admin":
        logger.info(f"Переход на страницу регистрации: {user_name} | {session_id}")
        return templates.TemplateResponse("registration.html", {"request": request})
    logger.info(f"Попытка перейти без прав доступа: {user_name} | {session_id}")
    return templates.TemplateResponse("403.html", {"request": request})


@app.post("/register")
@log
def register(request: Request,
            reg_name: str = Form(...),
            reg_password: str = Form(...)):
    users = pd.read_csv(USERS)
    if reg_name in users['user'].values:
        return templates.TemplateResponse("registration.html", {
                "request": request,
                "message": "Имя уже занято"
            })
    new_user = pd.DataFrame([{"user": reg_name, "pass":  hashlib.sha256(reg_password.encode()).hexdigest(), "role": "hamster"}])
    users = pd.concat([users, new_user], ignore_index=True)
    users.to_csv(USERS, index=False)
    logger.info(f"Регистрация нового хомячка: {reg_name}")
    return templates.TemplateResponse("main.html", {
        "request": request,
        "message": "Регистрация нового пользователя успешна."
    })


@app.get("/home/{username}", response_class=HTMLResponse)
@log
def login_page(request: Request):
    user_name = request.cookies.get("user_name")
    session_id = request.cookies.get("session_id")
    logger.info(f"Хомячок: {user_name} | {session_id}")
    return templates.TemplateResponse("hamster.html", {"request": request})


