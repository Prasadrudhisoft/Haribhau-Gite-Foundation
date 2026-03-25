from fastapi import FastAPI, Request


app = FastAPI()

from admin.admin import admin


app.include_router(admin)