from fastapi import FastAPI, Request, APIRouter,Depends
from connector import get_connection
from decorators import get_current_user
from tokens import create_token
from classes import Register,Logins,Events
import uuid
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

admin = APIRouter(tags=["Admin"])

@admin.post('/register_admin')
def register_admin(register:Register, request:Request):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        pwd = generate_password_hash(register.password)

        cursor.execute("select id from users")
        users = cursor.fetchall()
        if not users:
            id = str(uuid.uuid4())
            cursor.execute("insert into users(id,name,username,password,created_at) values(%s,%s,%s,%s,NOW())",(id, register.name, register.username, pwd))
            conn.commit()

            return{
                'status':'success',
                'message':'Admin Registers Successfully.'
            }
        else:
            return{
                'status':'fail',
                'message':'Admin Already Exists'
            }

    except Exception as e:
        return{
            'status':'error',
            'message':str(e)
        }
    
    finally:
        cursor.close()
        conn.close()


@admin.post('/login')
def login(log:Logins):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("select * from users where username=%s",(log.uname,))
        user = cursor.fetchone()

        if not user:
            return{
                'status':'fail',
                'message':'Invalid Username'
            }
        
        if not check_password_hash(user['password'],log.passw):
            return{
                'status':'fail',
                'message':'Invalid Password'
            }
        
        
        token = create_token({"id":user["id"],"name":user["name"]})
        return{
            'status':'success',
            'message':'Logged in Successfully',
            'user_data':{
                'id':user['id'],
                'name':user['name'],
                'token':token
            }
        }

    except Exception as e:
        return{
            'status':'error',
            'message':str(e)
        }
    
    finally:
        cursor.close()
        conn.close()

@admin.post('/events')
def events(events:Events, user=Depends(get_current_user)):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        event_id = str(uuid.uuid4())
        id = user['id']

        cursor.execute("insert into events(id,event_title,event_description,event_date,event_location,event_type, created_at, created_by) values(%s,%s,%s,%s,%s,%s,NOW(),%s)",(event_id,events.event_title, events.description, events.event_date, events.event_location, events.event_type,id))
        conn.commit()
        return{
            'status':'success',
            'message':'Event Added Successfully.'
        }

    except Exception as e:
        return{
            'status':'error',
            'message':str(e)
        }
    finally:
        cursor.close()
        conn.close()

