from fastapi import FastAPI, request, APIRouter
from connector import get_connection


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