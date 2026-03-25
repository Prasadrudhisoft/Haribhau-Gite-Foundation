from pydantic import BaseModel
from datetime import date

class Register(BaseModel):
    name :str
    username :str
    password: str

class Logins(BaseModel):
    uname : str
    passw : str

class Events(BaseModel):
    event_title: str
    description: str
    event_date: date
    event_location: str
    event_type: str
    
class Works(BaseModel):
    work_title: str
    work_description: str
    start_date: date
    end_date: date
    status: str

class Update_work_status(BaseModel):
    status = str
    id = str