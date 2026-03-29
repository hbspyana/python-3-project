from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.services import task_service

router = APIRouter()

engine = create_engine('sqlite:///./attendance.db')
SessionLocal = sessionmaker(bind=engine)

@router.post('/')
def create_user(name: str):
    db = SessionLocal()
    return task_service.create_user(db, name)

@router.post('attendance')
def mark_attendance(user_id, task_id, status):
    db = SessionLocal()
    result = task_service.mark_attendance(db, user_id, task_id, status)
    if not result:
        return {'error': 'Already marked'}
    return {'message': 'Attendance marked'}