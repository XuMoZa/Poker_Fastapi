from gateway_app.core.settings import security
import httpx

async def generate_token(user_id : int):
    token = security.create_access_token(uid=str(user_id))
    return token

async def check_info(user_id : int):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://user_service:8003/user/info", json={
            "user_id": user_id
        })
        if response.status_code == 200:
            data = response.json()
            new_user_id = data["user_id"]
            if new_user_id:
                return True
            else:
                return False
        else:
            return False