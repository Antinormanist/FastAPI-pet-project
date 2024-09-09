from fastapi import FastAPI

from .routers import user, auth, banana, cart, purchase

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(banana.router)
app.include_router(cart.router)
app.include_router(purchase.router)
