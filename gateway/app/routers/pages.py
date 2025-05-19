from fastapi import APIRouter, Request, Form, HTTPException, status
from starlette.responses import HTMLResponse
from main import templates
import pydantic
import httpx
from datetime import date
from services.service import generate_token
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def base_page(request: Request):
    return templates.TemplateResponse("base_page.html", {"request": request})
@router.get("/registration", response_class=HTMLResponse)
async def registration_page(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})
@router.post("/registration", response_class=HTMLResponse)
async def registration(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})

@router.get("/registration/info", response_class=HTMLResponse)
async def registration_info(request: Request):
    return templates.TemplateResponse("registration_info.html", {"request": request})

@router.post("/registration/info", response_class=HTMLResponse)
async def registration_success(request: Request,email: pydantic.EmailStr = Form(...),
                               password: str = Form(...)):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://auth_service:8001/auth/pre_registrate", json={
            "email": email,
            "password": password
        })
    if response.status_code == 200:
        return templates.TemplateResponse("registration_info.html", {"request": request})
    else:
        return templates.TemplateResponse("registration.html", {"request": request, "message": "registration failed"})

@router.post("/", response_class=HTMLResponse)
async def registration_with_info(request: Request, name: str = Form(...),
                               last_name: str = Form(...), email: str = Form(...), nickname: str = Form(...), birthday: date = Form(...)):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://auth_service:8001/auth/registrate", json={
            "email": email,
            "name": name,
            "last_name": last_name,
            "birthday": birthday,
            "nickname": nickname,
        })
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "success":
            return templates.TemplateResponse("base_page.html", {"request": request})
        else:
            return templates.TemplateResponse("registration.html", {"request": request, "message": data["message"]})
    else:
        return templates.TemplateResponse("registration.html", {"request": request, "message": "registration failed"})

@router.post("/home", response_class=HTMLResponse)
async def home_page(request: Request, email: str = Form(...), password: str = Form(...)):
    async with httpx.AsyncClient() as client:

        response = await client.post("http://auth_service:8001/auth/authorization", json={
            "email": email,
            "password": password
        })
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "success":
            user_id = data["user_id"]
            token  = await generate_token(user_id)
            request.session.update({'access_token': token})
            return templates.TemplateResponse("home.html", {"request": request})
        else:
            return templates.TemplateResponse("base_page.html", {"request": request, "message": data["message"]})
    else:
        return templates.TemplateResponse("base_page.html", {"request": request, "message": "authorization failed"})
