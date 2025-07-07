from authx import AuthX, AuthXConfig

config = AuthXConfig()
config.JWT_SECRET_KEY =  "string" #os.getenv("JWT_SECRET_KEY")
config.JWT_ALGORITHM = "HS256"
config.JWT_ACCESS_COOKIE_NAME = "access"
config.JWT_REFRESH_COOKIE_NAME = "refresh"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config)