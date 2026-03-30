from app.models.models import User, Attendance, Task

# def create_user(db, name):
#     user = User(name=name)
#     db.add(user)
#     db.commit()
#     return user

def create_user(db, name):
    user = User(name=name)
    db.add(user)
    db.commit()
    db.refresh(user)

    sessions = db.query(Task).all()
    for task in sessions:
        db.add(Attendance(user_id=user.id, task_id=task.id, status='absent'))
    db.commit()

    return user

def get_users(db):
    return db.query(User).all()

def delete_user(db, user_id):
    user = db.query(User).filter_by(id=user_id).first()

    if not user:
        return {'error': 'User not found'}

    db.delete(user)
    db.commit()
    return {'message': 'User deleted'}

def get_user_stats(db):
    users = db.query(User).all()

    result = []

    for user in users:
        records = db.query(Attendance).filter_by(user_id=user.id).all()

        total = len(records)
        present = len([r for r in records if r.status == 'present'])
        late = len([r for r in records if r.status == 'late'])

        result.append({
            'id': user.id,
            'name': user.name,
            'total_sessions': total,
            'present_count': present,
            'late_count': late
        })

    return result