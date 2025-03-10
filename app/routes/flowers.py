import os
from fastapi import APIRouter, Form, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from ..repositories.flowers import FlowersRepository

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = "static/uploads/flowers"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- СТРАНИЦА С ЦВЕТАМИ ---

@router.get("/flowers")
async def flowers_page(request: Request):
    flowers = FlowersRepository.get_flowers()
    return templates.TemplateResponse("flowers.html", {"request": request, "flowers": flowers})

# --- ДОБАВЛЕНИЕ ЦВЕТКА ---

@router.post("/flowers")
async def add_flower(
    request: Request,
    name: str = Form(...),
    quantity: int = Form(...),
    price: float = Form(...),
    photo: UploadFile = File(None)
):
    photo_path = None
    if photo:
        photo_path = f"{UPLOAD_DIR}/{name}.jpg"
        with open(photo_path, "wb") as buffer:
            buffer.write(photo.file.read())

    FlowersRepository.add_flower(name, quantity, price, photo_path)
    return RedirectResponse(url="/flowers", status_code=303)
