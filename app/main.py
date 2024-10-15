from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.routes import user as user_routers, candidate
from app.routes.skill import skill_router

app:FastAPI = FastAPI()
add_pagination(app)
app.include_router(user_routers.router)
app.include_router(candidate.router)
app.include_router(skill_router)
