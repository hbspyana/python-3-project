from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.services import user_service

router = APIRouter()

engine = create_engine('sqlite:///./attendance.db')
SessionLocal = sessionmaker(bind=engine)

@router.post('/')
def create_user(name: str):
    db = SessionLocal()
    return user_service.create_user(db, name)

@router.get('/')
def get_users():
    db = SessionLocal()
    return user_service.get_users_stats(db)

@router.delete('/{user_id}')
def delete_user(user_id: int):
    db = SessionLocal()
    return user_service.delete_user(db, user_id)