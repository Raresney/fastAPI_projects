from fastapi import FastAPI
from app.routers import users

app = FastAPI()

app.include_router(users.router)

@app.get("/")
def home():
    return {"message": "Backend is running"}



