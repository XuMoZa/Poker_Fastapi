import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from core.settings import config
from routers import pages

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(SessionMiddleware, secret_key=config.JWT_SECRET_KEY)

app.include_router(pages.router)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)