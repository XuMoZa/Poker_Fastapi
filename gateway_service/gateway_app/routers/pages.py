from fastapi import APIRouter, Request, Form, HTTPException, status, Depends
from starlette.responses import HTMLResponse
from gateway_app.core.settings import templates
import pydantic
import httpx
from datetime import date
from gateway_app.services.service import generate_token
router = APIRouter()

async def get_tables_by_game_type(game_type: str):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://table_service:8002/table/get_tables", json={
            "game_type": game_type
        })
    if response.status_code == 200:
        return response.json().get("tables", [])
    else:
        return None

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
                               password: str = Form(...), nickname: str = Form(...)):
    async with httpx.AsyncClient() as client:
        print("НАЧАЛО КОННЕКТА")
        print("НАЧАЛО КОННЕКТА")
        print("НАЧАЛО КОННЕКТА")
        print("НАЧАЛО КОННЕКТА")
        print("НАЧАЛО КОННЕКТА")
        try:
            response = await client.post("http://auth_service:8001/auth/pre_registrate", json={
                "email": email,
                "password": password,
                "nickname" : nickname
            })
        finally:
            print(response)
    data = response.json()
    if data["status"] == "success":
        return templates.TemplateResponse("registration_info.html", {"request": request})
    else:
        return templates.TemplateResponse("registration.html", {"request": request, "message": data["message"]})

@router.get("/account", response_class=HTMLResponse)
async def account_page(request: Request):
    return templates.TemplateResponse("account.html", {"request": request})
@router.post("/", response_class=HTMLResponse)
async def registration_with_info(request: Request, name: str = Form(...),
                               last_name: str = Form(...), email: str = Form(...), nickname: str = Form(...), birthday: date = Form(...)):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://auth_service:8001/auth/get_id", json={
            "email": email
        })
        print(response)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "success":
            async with httpx.AsyncClient() as client:
                response = await client.post("http://user_service:8003/user/add_info", json={
                    "name": name,
                    "last_name": last_name,
                    "birthday": birthday,
                    "user_id": data["id"]
                })
            if response.status_code == 200:
                data = response.json()
                if data["status"] == "success":
                    return templates.TemplateResponse("base_page.html", {"request": request})
                else: return templates.TemplateResponse("registration.html", {"request": request, "message": data["message"]})
            else:
                return templates.TemplateResponse("registration.html", {"request": request, "message": data["message"]})

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
        print(response)
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
        return templates.TemplateResponse("base_page.html", {"request": request, "message": "Неверное имя или пароль"})

@router.get("/home", response_class=HTMLResponse)
async def get_home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/tables/omaha")
async def omaha_tables(request: Request, tables=Depends(lambda: get_tables_by_game_type("omaha"))):
    if tables is not None:
        return templates.TemplateResponse("tables.html", {"request": request, "tables": tables})
    return templates.TemplateResponse("home.html", {"request": request, "message": "tables failed"})


@router.get("/tables/texas")
async def texas_tables(request: Request, tables=Depends(lambda: get_tables_by_game_type("texas"))):
    if tables is not None:
        return templates.TemplateResponse("tables.html", {"request": request, "tables": tables})
    return templates.TemplateResponse("home.html", {"request": request, "message": "tables failed"})

@router.get("/tables/blackjack")
async def blackjack_tables(request: Request, tables=Depends(lambda: get_tables_by_game_type("blackjack"))):
    if tables is not None:
        return templates.TemplateResponse("tables.html", {"request": request, "tables": tables})
    return templates.TemplateResponse("home.html", {"request": request, "message": "tables failed"})
