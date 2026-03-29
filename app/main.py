from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.routers import users, tasks
from app.models.models import Base
from sqlalchemy import create_engine

engine = create_engine('sqlite:///./attendance.db')
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router, prefix='/users')
app.include_router(tasks.router, prefix='/tasks')
app.mount('/static', StaticFiles(directory='.'), name='static')

@app.get('/')
def root():
    return {'message': 'Attendance API running'}

@app.get('/dashboard')
def dashboard():
    return FileResponse('index.html')