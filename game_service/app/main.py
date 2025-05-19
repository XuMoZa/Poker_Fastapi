from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
from routers import table_router

app = FastAPI()

app.add_middleware(SessionMiddleware, session_key="session")
app.include_router(table_router.router)


