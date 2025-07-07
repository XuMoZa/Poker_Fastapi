import uvicorn
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from gateway_app.core.settings import config
from gateway_app.routers import pages

app = FastAPI()
static_path = Path(__file__).parent / "static"

app.mount("/gateway_app/static", StaticFiles(directory=static_path), name="static")

app.add_middleware(SessionMiddleware, secret_key=config.JWT_SECRET_KEY)

app.include_router(pages.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)