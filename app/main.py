from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.routers import users, tasks
from app.models.models import Base
from sqlalchemy import create_engine
import os

engine = create_engine('sqlite:///./attendance.db')
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router, prefix='/users')
app.include_router(tasks.router, prefix='/tasks')
app.mount('/static', StaticFiles(directory='.'), name='static')

@app.get('/')
def root():
    file_path = os.path.join(os.getcwd(), 'index.html')
    return FileResponse(file_path)

@app.get('/dashboard')
def dashboard():
    file_path = os.path.join(os.getcwd(), 'index.html')
    return FileResponse(file_path)
