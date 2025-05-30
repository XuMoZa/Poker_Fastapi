from fastapi import FastAPI
from routers import user
from models.database import database
from core.settings import config
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
app = FastAPI()


app.include_router(user.router)

app.add_middleware(SessionMiddleware, secret_key=config.JWT_SECRET_KEY)

if __name__ == '__main__':
    uvicorn.run(app, port=8000)