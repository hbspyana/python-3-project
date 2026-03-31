from app.models.models import Task, Attendance, User

def create_task(db, title):
    task = Task(title=title)
    db.add(task)
    db.commit()
    db.refresh(task)
    users = db.query(User).all()
    
    for user in users:
        record = Attendance(user_id=user.id, task_id=task.id, status='absent')
        db.add(record)
    
    db.commit()
    return task

# def mark_attendance(db, user_id, task_id, status):
#     record = db.query(Attendance).filter_by(user_id=user_id, task_id=task_id).first()
    
#     if record:
#         record.status = status
#     else:
#         record = Attendance(user_id=user_id, task_id=task_id, status=status)
#         db.add(record)
    
#     db.commit()
#     return record
def mark_attendance(db, user_id, task_id, status):
    record = db.query(Attendance).filter_by(user_id=user_id, task_id=task_id).first()
    if record:
        record.status = status
    else:
        record = Attendance(user_id=user_id, task_id=task_id, status=status)
        db.add(record)
    db.commit()
    return {
        'user_id': record.user_id,
        'task_id': record.task_id,
        'status': record.status,
        'message': 'Attendance updated'
    }

# def get_tasks(db):
#     return db.query(Task).all()
def get_tasks(db):
    tasks = db.query(Task).all()
    return [{"id": t.id, "title": t.title} for t in db.query(Task).all()]

def get_attendance_for_task(db, task_id):
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