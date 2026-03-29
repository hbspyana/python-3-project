from pydantic import BaseModel

class CreateUserREquest(BaseModel):
    name: str

class CreateTaskRequest(BaseModel):
    title: str

class MarkAttendanceRequest(BaseModel):
    user_id: int
    task_id: int
    status: str
