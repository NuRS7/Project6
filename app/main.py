from fastapi import FastAPI
from .routes.auth import router as auth_router
from .routes.flowers import router as flowers_router
from fastapi.staticfiles import StaticFiles
from .routes.cart import router as cart_router
app = FastAPI()

app.include_router(auth_router)
app.include_router(flowers_router)
app.include_router(cart_router)

app.mount("/static", StaticFiles(directory="static"), name="static")