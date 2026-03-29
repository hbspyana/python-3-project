from app.models.models import User

def create_user(db, name):
    user = User(name=name)
    db.add(user)
    db.commit()
    return user

def get_users(db):
    return db.query(User).all()