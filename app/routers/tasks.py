from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.services import task_service

router = APIRouter()

engine = create_engine('sqlite:///./attendance.db')
SessionLocal = sessionmaker(bind=engine)

@router.post('/')
def create_task(title: str):
    db = SessionLocal()
    return task_service.create_task(db, title)

@router.post('/attendance')
def mark_attendance(user_id, task_id, status):
    db = SessionLocal()
    result = task_service.mark_attendance(db, user_id, task_id, status)
    if not result:
        return {'error': 'Already marked'}
    return {'message': 'Attendance marked'}

@router.get('/')
def get_tasks():
    db = SessionLocal()
    return task_service.get_tasks(db)

@router.get('/attendance/{task_id}')
def get_attendance(task_id: int):
    db = SessionLocal()
    return task_service.get_attendance_for_task(db, task_id)