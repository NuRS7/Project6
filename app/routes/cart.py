import json
from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from ..repositories.flowers import FlowersRepository

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# --- ДОБАВЛЕНИЕ В КОРЗИНУ ---
@router.post("/cart/items")
async def add_to_cart(request: Request, flower_id: int = Form(...)):
    cart = request.cookies.get("cart")
    cart = json.loads(cart) if cart else {}

    if str(flower_id) in cart:
        cart[str(flower_id)] += 1  # Увеличиваем количество
    else:
        cart[str(flower_id)] = 1  # Добавляем новый товар

    response = RedirectResponse(url="/flowers", status_code=303)
    response.set_cookie(key="cart", value=json.dumps(cart), httponly=True)
    return response


# --- ПРОСМОТР КОРЗИНЫ ---
@router.get("/cart/items")
async def view_cart(request: Request):
    cart = request.cookies.get("cart")
    cart = json.loads(cart) if cart else {}

    flowers_in_cart = []
    total_price = 0

    for flower_id, quantity in cart.items():
        flower = next((f for f in FlowersRepository.get_flowers() if f["id"] == int(flower_id)), None)
        if flower:
            flower["quantity"] = quantity
            flower["total_price"] = flower["price"] * quantity
            flowers_in_cart.append(flower)
            total_price += flower["total_price"]

    return templates.TemplateResponse("cart.html", {
        "request": request,
        "cart": flowers_in_cart,
        "total_price": total_price
    })


# --- УДАЛЕНИЕ ИЛИ УМЕНЬШЕНИЕ КОЛИЧЕСТВА ---
@router.post("/cart/update")
async def update_cart(request: Request, flower_id: int = Form(...), action: str = Form(...)):
    cart = request.cookies.get("cart")
    cart = json.loads(cart) if cart else {}

    if str(flower_id) in cart:
        if action == "increase":
            cart[str(flower_id)] += 1
        elif action == "decrease":
            cart[str(flower_id)] -= 1
            if cart[str(flower_id)] <= 0:
                del cart[str(flower_id)]

    response = RedirectResponse(url="/cart/items", status_code=303)
    response.set_cookie(key="cart", value=json.dumps(cart), httponly=True)
    return response
