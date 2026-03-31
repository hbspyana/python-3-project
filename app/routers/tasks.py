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
    try:
        return task_service.create_task(db, title)
    finally:
        db.close()

@router.post('/attendance')
def mark_attendance(user_id, task_id, status):
    db = SessionLocal()
    try:
        return task_service.mark_attendance(db, user_id, task_id, status)
    finally:
        db.close()

@router.get('/')
def get_tasks():
    db = SessionLocal()
    try:
        return task_service.get_tasks(db)
    finally:
        db.close()

@router.get('/attendance/{task_id}')
def get_attendance(task_id: int):
    db = SessionLocal()
    try:
        users = db.query(User).all()
        result = []

        for user in users:
            record = db.query(Attendance).filter_by(user_id=user.id, task_id=task_id).first()
            all_records = db.query(Attendance).filter_by(user_id=user.id).all()

            present_count = len([r for r in all_records if r.status == 'present'])
            late_count = len([r for r in all_records if r.status == 'late'])

            result.append({
                'id': user.id,
                'name': user.name,
                'status': record.status if record else 'absent',
                'present_count': present_count,
                'late_count': late_count
            })

        return result
    finally:
        db.close()