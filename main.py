from fastapi import FastAPI
from src.routers.todo import router
app = FastAPI()

app.include_router(router)
