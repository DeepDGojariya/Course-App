from fastapi import FastAPI
from routers import course_router

app = FastAPI()

app.include_router(course_router.router)

