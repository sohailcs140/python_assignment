from fastapi import FastAPI

from app.routes import user as user_routers, candidate
from fastapi_pagination import add_pagination

app = FastAPI()
add_pagination(app)
app.include_router(user_routers.router)
app.include_router(candidate.router)
