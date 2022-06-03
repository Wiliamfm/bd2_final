from django.db import router
from fastapi import FastAPI
from .routers import users, vendors

app = FastAPI()

app.include_router(users.router)
app.include_router(vendors.router)