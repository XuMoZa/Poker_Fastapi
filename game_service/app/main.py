from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
from routers import table_router
from core.settings import config

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=config.JWT_SECRET_KEY)
app.include_router(table_router.router)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
