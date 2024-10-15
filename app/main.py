from fastapi import FastAPI

from app.routes import candidate as candidate_routers, user as user_routers
from app.routes.skill import skill_router

app: FastAPI = FastAPI()
app.include_router(user_routers.router)
app.include_router(candidate_routers.router)
app.include_router(skill_router)
