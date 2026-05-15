from fastapi import APIRouter
from app.schemas.user_schema import UserCreate

router = APIRouter()

@router.post("/users")
def create_user(user: UserCreate):
    return user