from starlette.templating import Jinja2Templates
from authx import AuthX, AuthXConfig
from pathlib import Path
config = AuthXConfig()
config.JWT_SECRET_KEY =  "string" #os.getenv("JWT_SECRET_KEY")
config.JWT_ALGORITHM = "HS256"
config.JWT_ACCESS_COOKIE_NAME = "access"
config.JWT_REFRESH_COOKIE_NAME = "refresh"
config.JWT_TOKEN_LOCATION = ["cookies"]
template_path = "gateway_app/templates"
templates = Jinja2Templates(directory=template_path)
security = AuthX(config)
