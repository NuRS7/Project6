import jwt
import os
from datetime import datetime, timedelta
from fastapi import APIRouter, Form, Request, UploadFile, File, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from ..repositories.users import UsersRepository

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Генерация JWT токена
def create_jwt(email: str):
    expiration = datetime.utcnow() + timedelta(hours=1)
    payload = {"sub": email, "exp": expiration}
    encoded_jwt=jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Проверка JWT
def verify_jwt(request: Request):
    token = request.cookies.get("token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return None

# --- РЕГИСТРАЦИЯ ---

@router.get("/signup")
async def signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/signup")
async def signup(
    request: Request,
    email: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
    photo: UploadFile = File(None)
):
    photo_path = None
    if photo:
        photo_path = f"{UPLOAD_DIR}/{email}.jpg"
        with open(photo_path, "wb") as buffer:
            buffer.write(photo.file.read())

    if not UsersRepository.add_user(email, full_name, password, photo_path):
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Email уже используется"})

    return RedirectResponse(url="/login", status_code=303)

# --- ЛОГИН ---

@router.get("/login")
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = UsersRepository.get_user(email)
    if not user or user["password"] != password:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Неверные учетные данные"})

    token = create_jwt(email)
    response = RedirectResponse(url="/profile", status_code=303)
    response.set_cookie(key="token", value=token)
    return response

# --- ПРОФИЛЬ ---

@router.get("/profile")
async def profile(request: Request):
    email = verify_jwt(request)
    if not email:
        return RedirectResponse(url="/login", status_code=303)

    user_data = UsersRepository.get_user(email)
    return templates.TemplateResponse("profile.html", {"request": request, "user": user_data, "email": email})

# --- ВЫХОД ---

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("token")
    return response
