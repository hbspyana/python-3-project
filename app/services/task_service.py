from app.models.models import Task, Attendance

def create_task(db, title):
    task = Task(title=title)
    db.add(task)
    db.commit()
    return task

def mark_attendance(db, user_id, task_id, status):
    existing = db.query(Attendance).filter_by(user_id=user_id, task_id=task_id).first()
    if existing:
        return None
    record = Attendance(user_id=user_id, task_id=task_id, status=status)
    db.add(record)
    db.commit()
    return record