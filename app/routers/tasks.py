from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.services import task_service
from app.models.models import Task, User, Attendance

router = APIRouter()

engine = create_engine('sqlite:///./attendance.db')
SessionLocal = sessionmaker(bind=engine)

@router.post('/')
def create_task(title: str):
    db = SessionLocal()
    return task_service.create_task(db, title)

@router.delete('/{task_id}')
def delete_task(task_id: int):
    db = SessionLocal()
    return task_service.delete_task(db, task_id)

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
    users = db.query(User).all()
    result = []

    for user in users:
        record = db.query(Attendance).filter_by(user_id=user.id, task_id=task_id).first()
        result.append({
            'id': user.id,
            'name': user.name,
            'status': record.status if record else 'absent',
            'present_count': len([r for r in db.query(Attendance).filter_by(user_id=user.id).all() if r.status=='present']),
            'late_count': len([r for r in db.query(Attendance).filter_by(user_id=user.id).all() if r.status=='late'])
        })

    return result