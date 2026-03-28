from fastapi import FastAPI, Request, APIRouter
from connector import get_connection
import uuid
from fastapi import UploadFile, File, Form
import os
from datetime import datetime



user = APIRouter(tags=["user"])

@user.get('/user_get_events')
def user_get_events():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("select event_title,event_description,event_date, event_location, event_type from events")
        events = cursor.fetchall()

        return{
            'status':'success',
            'message':'Events Fetched Successfully.',
            'events':events
        }
    except Exception as e:
        return{
            'status':'error',
            'message':str(e)
        }
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@user.get('/user_get_works')
def user_works():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("select work_title, work_description, start_date, end_date, status from works")
        works = cursor.fetchall()

        if not works:
            return{
                'status':'fail',
                'message':'Developments Works Are Not Uploaded Yet'
            }

        pragatipathavar = []
        purn = []
        pralambit = []
        manjur = []
        nakarlele = []
        other = []

        for i in works:
            if i['status'] =="प्रगतीपथावर":
                pragatipathavar.append(i)
            if i['status'] == "पूर्ण झाले":
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
            'message':'Development Works Fetched Successfully',
            'pragatipathavr':pragatipathavar,
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
        if cursor:
            cursor.close()
        if conn:
            cursor.close()


@user.get('/user_get_gallery')
def user_get_gallery():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

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
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@user.get('/user_gov_schem')
def user_gov_schem():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("select title,description,start_date,end_date from gov_schems")
        gov_schem = cursor.fetchall()

        return{
            'status':'success',
            'message':'Government Schems Fetched Successfully',
            'gov_scheme':gov_schem
        }
    except Exception as e:
        return{
            'status':'error',
            'message':str(e)
        }
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


UPLOAD_DIR = "static/images"

@user.post('/register_complain')
async def register_complain(
    name: str = Form(...),
    mobile_number: str = Form(...),
    Address: str = Form(...),
    complain_type: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...)
):
    conn = None
    cursor = None

    try:

        os.makedirs(UPLOAD_DIR, exist_ok=True)

        conn = get_connection()
        cursor = conn.cursor()


        if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
            return {
                'status': 'fail',
                'message': 'Only jpg, jpeg, png image files allowed'
            }

        file_ext = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        photo_path = f"/static/images/{filename}"
        status = "Not Accepted Yet"

        id = str(uuid.uuid4())

      
        cursor.execute("""
            SELECT complain_reg_no 
            FROM complains 
            ORDER BY created_at DESC 
            LIMIT 1
        """)
        last_record = cursor.fetchone()

        if last_record and last_record.get('complain_reg_no'):
            last_no = last_record['complain_reg_no'].strip()
            try:
                number = int(last_no.split('-')[-1]) + 1
            except:
                number = 1
        else:
            number = 1

        complain_no = f"HGF-{number:04d}"

        cursor.execute("""
            INSERT INTO complains(
                id, person_name, complain_reg_no, mobile_no, address, 
                complain_type, description, photo_path, created_at, status
            ) 
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,NOW(),%s)
        """, (
            id,
            name,
            complain_no,
            mobile_number,
            Address,
            complain_type,
            description,
            photo_path,
            status
        ))

        conn.commit()

        return {
            'status': 'success',
            'message': 'Complain Registered Successfully.',
            'complain_no': complain_no
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()