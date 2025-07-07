from gateway_app.core.settings import security

async def generate_token(user_id : int):
    token = security.create_access_token(uid=str(user_id))
    return token