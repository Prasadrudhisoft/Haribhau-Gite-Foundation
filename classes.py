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
    status: str
    id: str

class Gov_schems(BaseModel):
    title: str
    description: str
    start_date: date
    end_date: date

class Update_complain_status(BaseModel):
    comp_id: str
    comp_status: str

class User_complain(BaseModel):
    comp_id: str
    person_name: str
    mobile_no: str