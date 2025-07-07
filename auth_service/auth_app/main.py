from fastapi import FastAPI
from auth_app.routers import auth
from auth_app.models.database import init_db, new_session
from auth_app.core.settings import config
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
import uvicorn
app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
        await init_db()
        yield
app.include_router(auth.router)

app.add_middleware(SessionMiddleware, secret_key=config.JWT_SECRET_KEY)

if __name__ == '__main__':
        uvicorn.run(app, port=8000)
