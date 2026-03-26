from fastapi import FastAPI, Request, APIRouter,Depends
from connector import get_connection
from decorators import get_current_user
from tokens import create_token
from classes import Register,Logins,Events,Works,Update_work_status,Gov_schems
import uuid
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi import UploadFile, File, Form
import os
from datetime import datetime

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

@admin.get('/get_events')
def get_events(user=Depends(get_current_user)):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('select * from events')
        events = cursor.fetchall()
        return{
            'status':'success',
            'message':'Events Fetched Successfully',
            'events':events
        }
    except Exception as e:
        return{
            'status':'error',
            'message':str(e)
        }
    finally:
        cursor.close()
        conn.close()


@admin.post('/works')
def works(works:Works, user=Depends(get_current_user)):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        id = str(uuid.uuid4())

        cursor.execute("INSERT INTO WORKS(id,work_title,work_description,start_date,end_date,status,created_at,created_by) values(%s,%s,%s,%s,%s,%s,NOW(),%s)",(id,works.work_title,works.work_description,works.start_date,works.end_date,works.status,user['id']))
        conn.commit()

        return{
            'status':'success',
            'message':'work added successfully'
        }
    except Exception as e:
        return{
            'status':'error',
            'message':str(e)
        }
    finally:
        cursor.close()
        conn.close()

@admin.get('/get_works')
def get_works(user=Depends(get_current_user)):
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("select * from works where created_by = %s",(user['id']))
        works = cursor.fetchall()

        pragatipathavar = []
        purn = []
        pralambit = []
        manjur = []
        nakarlele = []
        other = []

        for i in works:
            if i['status']=="प्रगतीपथावर":
                pragatipathavar.append(i)
            if i['status']=="पूर्ण झाले":
                purn.append(i)
            if i['status']=="प्रलंबित":
                pralambit.append(i)
            if i['status']=="मंजूर":
                manjur.append(i)
            if i['status']=="नाकारलेले":
                nakarlele.append(i)
            if i['status']=="इतर":
                other.append(i)

        return{
            'status':'success',
            'message':'Development Works Fetched Successfully.',
            'pragatipathavar':pragatipathavar,
            'purn':purn,
            'pralambit':pralambit,
            'manjur':manjur,
            'nakarlele':nakarlele,
            'other':other

        }

    except Exception as e:
        return{
            'status':'error',
            'message':str(e)
        }
    finally:
        cursor.close()
        conn.close()


@admin.post('/update_works_status')
def update_works_status(update_status:Update_work_status,user=Depends(get_current_user)):
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("update works set status=%s where id = %s",(update_status.status,update_status.id))
        conn.commit()
        return{
            'status':'success',
            'message':f'Status Updated To {update_status.status}'
        }
    except Exception as e:
        return{
            'status':'error',
            'message':str(e)
        }
    finally:
        cursor.close()
        conn.close()


UPLOAD_DIR = "static/images"


@admin.post("/upload_image")
async def upload_image(
    description: str = Form(...),
    file: UploadFile = File(...),
    user=Depends(get_current_user),
):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
            return{'status':'fail', 'message':'Only image files allowed'}

    
        file_ext = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        db_path = f"/static/images/{filename}"

        image_id = str(uuid.uuid4())

        cursor.execute(
            """INSERT INTO gallery(
                id, photo_path, description, uploaded_at, uploaded_by
            ) VALUES (%s,%s,%s,NOW(),%s)""",
            (image_id, db_path, description, user["id"])
        )

        conn.commit()

        return {
            "status": "success",
            "message": "Image uploaded successfully",
            "data": {
                "image_url": db_path,
                "description": description
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

@admin.get('/get_gallery')
def get_gallery(user=Depends(get_current_user)):
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT id, photo_path, description, uploaded_at, uploaded_by FROM gallery ORDER BY uploaded_at DESC")
        images = cursor.fetchall()

        return {
            'status': 'success',
            'message': 'Gallery Fetched Successfully',
            'total': len(images),
            'images': images
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }
    finally:
        cursor.close()
        conn.close()


@admin.post('/gov_schems')
def gov_schems(gov_schems:Gov_schems,user=Depends(get_current_user)):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        scm_id = str(uuid.uuid4())

        cursor.execute("insert into gov_schems(id,title,description,start_date,end_date,created_at,created_by) values(%s,%s,%s,%s,%s,NOW(),%s)",(scm_id,gov_schems.title, gov_schems.description,gov_schems.start_date,gov_schems.end_date,user['id']))
        conn.commit()
        return{
            'status':'success',
            'message':'government scheme uploads successfully.'
        }
    except Exception as e:
        return{
            'status':'error',
            'message':str(e)
        }
    finally:
        cursor.close()
        conn.close()

@admin.get('/get_schems')
def get_schems(user=Depends(get_current_user)):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("select * from gov_schems ORDER BY start_date desc")
        schems = cursor.fetchall()
        return{
            'status':'success',
            'message':'Government Schems Fetched Successfully.',
            'schems':schems
        }
    except Exception as e:
        return{
            'status':'error',
            'message':str(e)
        }
    finally:
        cursor.close()
        conn.close()


